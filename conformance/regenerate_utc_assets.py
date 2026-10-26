#!/usr/bin/env python3
"""One-time pre-release fixture cutover. Public TEST ONLY key; no product input.

Read the fixed pre-cutover assets from Git, never a user's Package. Keep the
original inventory, expected results, entry order, opaque bytes and ZIP faults.
Re-running this command produces exactly the same assets.
"""
import base64
import copy
import io
import json
import re
import subprocess
import warnings
import zipfile

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from check import ROOT, b64url, canonical, digest, parse, require, subject

SOURCE = '18d11e5c77c7336ac2be5db31a5d05b4e5e1da17'


def source(path):
    return parse(subprocess.check_output(['git', 'show', f'{SOURCE}:{path}'], cwd=ROOT))


def write(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


SCHEMAS = {v['properties']['schema']['const']: v
           for p in (ROOT / 'schemas').glob('*.json')
           for v in [parse(p.read_bytes())]}


def times(value, schema):
    """Only visit schema-declared properties, never opaque data/extensions."""
    if schema.get('format') == 'date-time':
        require(isinstance(value, str) and re.fullmatch(
            r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z', value),
            'unexpected source timestamp')
        return value[:-1] + '+00:00'
    if isinstance(value, dict):
        if value.get('schema') in SCHEMAS:
            schema = SCHEMAS[value['schema']]
        return {k: times(v, schema['properties'][k])
                if k in schema.get('properties', {}) else v for k, v in value.items()}
    if isinstance(value, list) and 'items' in schema:
        return [times(v, schema['items']) for v in value]
    return value


def control(path, raw):
    # Do not interpret payload, HEAD, unknown optional extensions or archive
    # traversal entries, even if their bytes resemble JSON or timestamps.
    relative = next((path.removeprefix(prefix) for prefix in ('.packtell/', 'Demo/.packtell/')
                     if path.startswith(prefix)), None)
    if relative is None or relative.startswith('extensions/'):
        return raw
    if path.endswith('.json'):
        doc = parse(raw)
        return canonical(times(doc, SCHEMAS[doc['schema']]))
    if path.endswith('/history/events.ndjson'):
        return b''.join(canonical(times(parse(line), SCHEMAS['orbifabric.package.event.v1'])) + b'\n'
                        for line in raw.splitlines())
    return raw


def sign(envelope, domain, key):
    require(envelope['public_key'] == vector['public_key_base64url']
            and envelope['fingerprint'] == vector['fingerprint']
            and envelope['key_id'].startswith('test-only-'), 'not a public test-key fixture')
    msg = domain.encode() + b'\n' + canonical({k: v for k, v in envelope.items() if k != 'signature'})
    envelope['signature'] = b64url(key.sign(msg))
    return msg


def rebuild_tree(fixture, key):
    entries = fixture['input']['entries']
    tree = {e['path']: control(e['path'], base64.b64decode(e['bytes_base64'], validate=True))
            for e in entries if e['kind'] == 'file'}
    for path in tree:
        if '/verification/versions/' in path:
            env = parse(tree[path])
            _, env['subject_digest'] = subject(tree, env['package_version_id'])
            sign(env, 'orbifabric.package.version-signature.v2', key)
            if fixture['id'] == 'bad-signature':
                sig = bytearray(base64.urlsafe_b64decode(env['signature'] + '=='))
                sig[0] ^= 1  # Preserve a real corrupt signature, not a stale digest.
                env['signature'] = b64url(sig)
            tree[path] = canonical(env)
    for path in tree:
        if '/evidence/deliveries/' in path:
            delivery = parse(tree[path])
            _, delivery['subject_digest'] = subject(tree, delivery['package_version_id'])
            tree[path] = canonical(delivery)
    for path in tree:
        if '/evidence/objects/' in path:
            env = parse(tree[path]); s = env['subject']
            _, s['version_subject_digest'] = subject(tree, s['package_version_id'])
            if 'delivery_digest' in s:
                delivery = parse(tree[f".packtell/evidence/deliveries/{s['delivery_id']}/delivery.json"])
                s['delivery_digest'] = digest(canonical({k: v for k, v in delivery.items() if k != 'evidence_refs'}))
            if 'event_digest' in s:
                events = [parse(line) for line in tree['.packtell/history/events.ndjson'].splitlines()]
                event, = [e for e in events if e['event_id'] == s['event_id']]
                s['event_digest'] = digest(canonical(event))
            env['subject_digest'] = digest(s['schema'].encode() + b'\n' + canonical(s))
            sign(env, 'orbifabric.package.evidence-envelope.v1', key)
            tree[path] = canonical(env)
    for entry in entries:
        if entry['kind'] == 'file':
            entry['bytes_base64'] = base64.b64encode(tree[entry['path']]).decode()
    return tree


def rebuild_zip(fixture):
    out = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(base64.b64decode(fixture['input']['bytes_base64']))) as old:
        with zipfile.ZipFile(out, 'w') as new:
            new.comment = old.comment
            for info in old.infolist():
                raw = old.read(info)  # ZipInfo preserves duplicate entries.
                # Keep the deliberate duplicate-name fault; never extract paths.
                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore', message='Duplicate name:')
                    new.writestr(copy.copy(info), control(info.filename, raw))
    fixture['input']['bytes_base64'] = base64.b64encode(out.getvalue()).decode()


def main():
    global vector
    vector = source('vectors/crypto.v2.json')
    require(vector['warning'] == 'TEST ONLY — NEVER PRODUCTION', 'test key warning')
    key = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(vector['seed_hex']))
    manifest = source('conformance/manifest.v2.json')
    trees = {}
    for case in manifest['fixtures']:
        path = 'fixtures/' + case['id'] + '.json'
        fixture = source(path)
        if fixture['input']['kind'] == 'tree':
            trees[fixture['id']] = rebuild_tree(fixture, key)
        else:
            rebuild_zip(fixture)
        write(path, fixture)
        case['sha256'] = digest((ROOT / path).read_bytes())
    t = trees['valid-signature']; vid = vector['version']['package_version_id']
    vector['package'] = parse(t['.packtell/package.json'])
    vector['version'] = parse(t[f'.packtell/versions/{vid}/version.json'])
    vector['manifest'] = parse(t[f'.packtell/versions/{vid}/manifest.json'])
    vector['manifest_digest'] = digest(canonical(vector['manifest']))
    vector['subject'], vector['subject_digest'] = subject(t, vid)
    vector['subject_canonical_hex'] = canonical(vector['subject']).hex()
    env = vector['signature_envelope'] = parse(next(raw for path, raw in t.items()
                                                   if '/verification/versions/' in path))
    vector['signing_input_hex'] = sign(env, 'orbifabric.package.version-signature.v2', key).hex()
    for invariant in vector['invariants']:
        invariant['subject_digest'] = vector['subject_digest']
    # Independent, literal expectations, consumed at every schema time field by
    # the checker. These are not inferred from an implementation's parser.
    vector['canonical_timestamps'] = {
        'valid': [
            '0001-01-01T00:00:00.000000+00:00',
            '2024-02-29T23:59:59.123456+00:00',
            '2026-10-25T12:34:56.123456+00:00',
            '9999-12-31T23:59:59.999999+00:00',
        ],
        'invalid': [
            '2026-10-25T12:34:56.123456Z',
            '2026-10-25T12:34:56.123456-04:00',
            '2026-10-25T12:34:56.123456+01:00',
            '2026-10-25T12:34:56.123456-00:00',
            '2026-10-25T12:34:56.123+00:00',
            '2026-10-25T12:34:56+00:00',
            '2026-10-25T12:34:56.123456789+00:00',
            '2026-02-29T12:34:56.123456+00:00',
            '2026-04-31T12:34:56.123456+00:00',
            '2026-10-25T12:34:60.123456+00:00',
            '0000-01-01T00:00:00.000000+00:00',
            '2026-10-25T24:00:00.123456+00:00',
            '2026-10-25T12:34:56.123456+00:00\n',
            '2026-10-25T12:34:56.123456+00:00\r\n',
            '2026-10-25T12:34:56.123456+00:00 ',
        ],
    }
    # Real consumer cases: invalidate only package.created_at in a valid tree.
    # Do not mutate any of the original 30 expected result objects.
    for index, timestamp in enumerate(vector['canonical_timestamps']['invalid'], 1):
        fixture = parse((ROOT / 'fixtures/minimal-valid.json').read_bytes())
        fixture['id'] = f'noncanonical-time-{index:02d}'
        for entry in fixture['input']['entries']:
            if entry['path'] == '.packtell/package.json':
                package = parse(base64.b64decode(entry['bytes_base64']))
                package['created_at'] = timestamp
                entry['bytes_base64'] = base64.b64encode(canonical(package)).decode()
        fixture['expected'].update(structure='INVALID', working_state='NOT_CHECKED',
                                   committed_integrity='NOT_CHECKED', history_completeness='INVALID',
                                   signature='NOT_CHECKED', reason_codes=['INVALID_SCHEMA'])
        path = f'fixtures/{fixture["id"]}.json'
        write(path, fixture)
        manifest['fixtures'].append({
            'id': fixture['id'], 'path': '../' + path,
            'levels': manifest['levels'], 'sha256': digest((ROOT / path).read_bytes()),
        })
    write('vectors/crypto.v2.json', vector)
    write('conformance/manifest.v2.json', manifest)
    print(f'Rebuilt {len(manifest["fixtures"])} fixed-source fixtures and crypto vectors; public TEST ONLY seed.')


if __name__ == '__main__':
    main()
