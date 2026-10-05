#!/usr/bin/env python3
"""Repository asset consistency checks. Not an SDK/conformance implementation."""
from pathlib import Path
import base64
import hashlib
import json
import re
import sys
import zipfile
import io
from collections import Counter
from urllib.parse import unquote
import jsonschema
from referencing import Registry, Resource
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

ROOT = Path(__file__).resolve().parents[1]

def require(ok, message):
    if not ok:
        raise AssertionError(message)

def pairs(values):
    result = {}
    for key, value in values:
        require(key not in result, f'duplicate JSON key: {key}')
        result[key] = value
    return result

def integer(s):
    require(s != '-0' and abs(int(s)) <= 9007199254740991, 'noncanonical integer domain')
    return int(s)

def forbidden(s):
    raise ValueError('non-integer number: ' + s)

def parse(raw):
    value = json.loads(raw.decode('utf-8') if isinstance(raw, bytes) else raw,
                       object_pairs_hook=pairs, parse_int=integer,
                       parse_float=forbidden, parse_constant=forbidden)
    # UTF-8 encoding rejects isolated surrogate code points.
    canonical(value)
    return value

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def digest(raw):
    return 'sha256:' + hashlib.sha256(raw).hexdigest()

def b64url(raw):
    return base64.urlsafe_b64encode(raw).decode().rstrip('=')

def decode_url(s):
    b = base64.urlsafe_b64decode(s + '=' * (-len(s) % 4))
    require(b64url(b) == s, 'noncanonical base64url')
    return b

def relative(base, name):
    p = (base / name).resolve()
    require(p.is_relative_to(ROOT) and p.exists(), f'missing/outside reference {name}')
    return p

def tree(fixture):
    inp = fixture['input']
    if inp['kind'] == 'tree':
        return {e['path']: None if e['kind'] == 'directory' else base64.b64decode(e['bytes_base64'], validate=True)
                for e in inp['entries']}
    with zipfile.ZipFile(io.BytesIO(base64.b64decode(inp['bytes_base64'], validate=True))) as archive:
        return {e.filename: None if e.is_dir() else archive.read(e) for e in archive.infolist()}

def subject(t, version_id):
    v = parse(t[f'.packtell/versions/{version_id}/version.json'])
    m = parse(t[f'.packtell/versions/{version_id}/manifest.json'])
    content = sorted({(e['content_id'], e['size']) for e in m['entries'] if e['kind'] == 'file'})
    keys = ['package_id', 'package_version_id', 'parent_version_id', 'ordinal', 'created_at',
            'protocol', 'protocol_version', 'tree_profile', 'profiles', 'required_capabilities', 'optional_capabilities']
    s = {'schema': 'orbifabric.package.version-subject.v2', 'domain': 'orbifabric.package.version-subject.v2',
         **{k: v[k] for k in keys}, 'package_digest': digest(canonical(parse(t['.packtell/package.json']))),
         'version_digest': digest(canonical(v)), 'manifest_digest': digest(canonical(m)),
         'sealed_metadata_digest': digest(canonical(v['sealed_metadata'])),
         'content_commitment': digest(b'orbifabric.package.content-set.v1\n' + canonical([
             {'content_id': a, 'size': b} for a, b in content]))}
    return s, digest(b'orbifabric.package.version-subject.v2\n' + canonical(s))

def verify_envelope(e, domain):
    pub = decode_url(e['public_key'])
    require(len(pub) == 32 and digest(pub) == e['fingerprint'], 'public key fingerprint')
    sig = decode_url(e['signature'])
    require(len(sig) == 64, 'signature length')
    msg = domain.encode() + b'\n' + canonical({k: v for k, v in e.items() if k != 'signature'})
    Ed25519PublicKey.from_public_bytes(pub).verify(sig, msg)
    return msg

def main():
    assets = {p: parse(p.read_bytes()) for directory in ['schemas', 'profiles', 'vocabularies', 'fixtures', 'vectors', 'conformance']
              for p in (ROOT / directory).glob('*.json')}
    schemas = {v['$id']: v for p, v in assets.items() if p.parent.name == 'schemas'}
    require(len(schemas) == len(list((ROOT / 'schemas').glob('*.json'))), 'duplicate schema ID')
    registry = Registry().with_resources((k, Resource.from_contents(v)) for k, v in schemas.items())
    for schema in schemas.values():
        jsonschema.Draft202012Validator.check_schema(schema)
        def refs(v):
            if isinstance(v, dict):
                if '$ref' in v:
                    require(v['$ref'].split('#')[0] in schemas, 'missing schema reference')
                for x in v.values(): refs(x)
            elif isinstance(v, list):
                for x in v: refs(x)
        refs(schema)
    def validate(doc):
        key = 'https://orbifabric.org/package/schemas/' + doc['schema'].removeprefix('orbifabric.package.') + '.schema.json'
        require(key in schemas, 'missing schema: ' + key)
        jsonschema.Draft202012Validator(schemas[key], registry=registry,
                                       format_checker=jsonschema.FormatChecker()).validate(doc)
    # All paired normative clauses, not merely the new chapter.
    clause = re.compile(r'`(PKG-[A-Z]+-\d+)`\s*[:：]')
    strength = re.compile(r'\b(MUST NOT|SHOULD NOT|MUST|SHOULD|MAY)\b')
    all_ids = []
    for zh in sorted((ROOT / 'specification/zh-CN').glob('*.md')):
        en = ROOT / 'specification/en' / zh.name
        require(en.exists(), 'missing English counterpart')
        a, b = zh.read_text(), en.read_text()
        require(clause.findall(a) == clause.findall(b), 'Clause parity: ' + zh.name)
        all_ids.extend(clause.findall(a))
        if zh.name.startswith('10-'):
            require(re.findall(r'^## .*', a, re.M) == re.findall(r'^## .*', b, re.M), 'section parity')
        for ca, cb in zip(clause.split(a)[2::2], clause.split(b)[2::2]):
            require(Counter(strength.findall(ca)) == Counter(strength.findall(cb)), 'strength parity: ' + zh.name)
    require(len(all_ids) == len(set(all_ids)), 'duplicate normative clause ID')
    # Local Markdown targets; fragments are document navigation, not filesystem names.
    for p in ROOT.rglob('*.md'):
        if '.git' in p.parts: continue
        for link in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            link = link.split('#', 1)[0]
            if not link or re.match(r'[a-z]+:', link): continue
            relative(p.parent, unquote(link))
    manifest = assets[ROOT / 'conformance/manifest.v2.json']
    ids = [x['id'] for x in manifest['fixtures']]
    require(len(ids) == len(set(ids)), 'duplicate fixture ID')
    require(set(ids) == {p.stem for p in (ROOT / 'fixtures').glob('*.json')}, 'fixture inventory')
    required_dims = {'recognition', 'structure', 'working_state', 'committed_integrity', 'history_completeness',
                     'signature', 'identity', 'evidence', 'online', 'reason_codes'}
    fixtures = {}
    schema_failures = 0
    for case in manifest['fixtures']:
        p = relative(ROOT / 'conformance', case['path'])
        require(digest(p.read_bytes()) == case['sha256'], 'fixture hash ' + case['id'])
        f = assets[p]; fixtures[f['id']] = f
        require(f['id'] == case['id'] and set(f['expected']) == required_dims, 'fixture manifest shape')
        require(set(case['levels']) <= set(manifest['levels']), 'unknown conformance level')
        failures = []
        for path, raw in tree(f).items():
            if raw is not None and path.endswith('.json') and '/.packtell/' in '/' + path:
                try: validate(parse(raw))
                except jsonschema.ValidationError: failures.append(path)
        require(bool(failures) == ('INVALID_SCHEMA' in f['expected']['reason_codes']), 'schema expectation ' + f['id'])
        schema_failures += len(failures)
    for name in manifest['vectors']: relative(ROOT / 'conformance', name)
    v = assets[ROOT / 'vectors/crypto.v2.json']
    require(v['warning'] == 'TEST ONLY — NEVER PRODUCTION', 'test key warning')
    key = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(v['seed_hex']))
    pub = key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    require(b64url(pub) == v['public_key_base64url'] and digest(pub) == v['fingerprint'], 'fixed key vector')
    for c in v['canonical_json']:
        out = canonical(c['input'])
        require(out.hex() == c['expected_utf8_hex'] and digest(out) == c['expected_digest'], 'canonical vector')
    for bad in v['invalid_json']:
        try: parse(bad)
        except (ValueError, AssertionError, UnicodeError): pass
        else: raise AssertionError('accepted invalid canonical-domain input')
    require(digest(canonical(v['manifest'])) == v['manifest_digest'], 'manifest digest')
    derived, sd = subject(tree(fixtures['valid-signature']), v['version']['package_version_id'])
    require(derived == v['subject'] and canonical(derived).hex() == v['subject_canonical_hex'] and sd == v['subject_digest'], 'subject vector')
    for name in ['package', 'version', 'manifest', 'subject', 'signature_envelope']: validate(v[name])
    msg = verify_envelope(v['signature_envelope'], 'orbifabric.package.version-signature.v2')
    require(msg.hex() == v['signing_input_hex'] and b64url(key.sign(msg)) == v['signature_envelope']['signature'], 'signature vector')
    for f in fixtures.values():
        if f['input']['kind'] != 'tree': continue
        t = tree(f)
        for path, raw in t.items():
            if raw is None or '/verification/versions/' not in path: continue
            e = parse(raw)
            _, expected = subject(t, e['package_version_id'])
            require(e['subject_digest'] == expected, 'fixture signature subject')
            try: verify_envelope(e, 'orbifabric.package.version-signature.v2')
            except Exception:
                require(f['id'] == 'bad-signature', 'unexpected bad signature')
            else: require(f['id'] != 'bad-signature', 'negative signature verifies')
            require(v['signature_verify'] is True, 'signature verify expectation')
        for path, raw in t.items():
            if raw is not None and '/evidence/objects/' in path:
                e = parse(raw);s = e['subject']
                require(e['subject_digest'] == digest(s['schema'].encode() + b'\n' + canonical(s)), 'evidence digest')
                verify_envelope(e, 'orbifabric.package.evidence-envelope.v1')
    for inv in v['invariants']:
        a = tree(parse(relative(ROOT / 'vectors', inv['before']).read_bytes()))
        b = tree(parse(relative(ROOT / 'vectors', inv['after']).read_bytes()))
        require(subject(a, inv['package_version_id']) == subject(b, inv['package_version_id']), 'evidence changed subject')
        for p in a:
            if '/verification/versions/' in p: require(a[p] == b[p], 'evidence changed signature')
            if '/evidence/deliveries/' in p:
                x, y = parse(a[p]), parse(b[p]); x.pop('evidence_refs'); y.pop('evidence_refs')
                require(digest(canonical(x)) == digest(canonical(y)), 'evidence changed delivery digest')
    vocab_check = assets[ROOT / 'vocabularies/core.v2.json']
    require(schemas['https://orbifabric.org/package/schemas/event.v1.schema.json']['properties']['type']['oneOf'][0]['enum'] == vocab_check['event_types'], 'event vocabulary drift')
    for f in fixtures.values():
        for dim, key in [('recognition','recognition'), ('structure','structure'), ('working_state','working_states'), ('history_completeness','history_completeness'), ('signature','signature_states'), ('identity','identity_states'), ('evidence','evidence_states'), ('online','online_states'), ('committed_integrity','committed_integrity')]:
            require(f['expected'][dim] in vocab_check[key], 'result vocabulary drift')
        require(set(f['expected']['reason_codes']) <= set(vocab_check['reason_codes']), 'reason vocabulary drift')
    profile = assets[ROOT / 'profiles/complete.v1.json']
    vocab = assets[ROOT / 'vocabularies/core.v2.json']
    require(profile['id'] in vocab['profiles'] and set(profile['required_capabilities']) <= set(vocab['capabilities']), 'profile references')
    for field in ['verification_clause', 'signature_policy_clause']: require(profile[field] in all_ids, 'profile clause')
    print(f'PASS: {len(schemas)} schemas; {len(ids)} fixtures; {len(all_ids)} paired clauses; {schema_failures} expected schema rejection; canonical/hash/Ed25519 vectors; evidence invariants; local links.')
    print('SDK conformance: NOT RUN. Product tests: NOT RUN. Remote CI: NOT RUN.')

if __name__ == '__main__':
    try: main()
    except Exception as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
