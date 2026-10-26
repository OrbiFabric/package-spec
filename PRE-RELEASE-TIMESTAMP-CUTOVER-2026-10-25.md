# Package Protocol 2.0 — Pre-release UTC timestamp clean break

Founder approved 2026-10-25. STATUS: **NORMATIVE + 13 SCHEMAS + GOLDEN ASSETS REBUILT / LOCAL CHECKER PASS / REVIEW AND NORMAL MERGE PENDING**.

## Canonical target

All Portable Package 2.0 timestamp fields use the Cloud AuditTrail UTC RFC3339 representation:

    2026-10-25T12:34:56.123456+00:00

Require exactly six microsecond digits, literal +00:00, valid Gregorian dates and seconds 00..59. Reject old Z, all other offsets, variable precision, local time, leap seconds and impossible dates. Version Subject, Signature, Event, Delivery, Witness, Notes, Provenance and other portable date-time fields are covered. The stored/signed bytes are canonical, not automatically normalized on read. The protocol stays called 2.0 only because this is a Founder-approved unreleased development Clean Break, not a compatible public 2.x minor update.

Changing Z to +00:00 changes canonical package/version bytes and derived SHA-256 subject hashes; changing signed_at changes Ed25519 signature input. Previous pre-release test signatures do not survive a string substitution. Re-sign only known TEST ONLY fixture material with the public vector seed; never fabricate valid signatures.

## REQUIRED before PR can merge

1. Regenerate all dependent conformance assets, not just visible Schema text. Fixtures encode portable JSON/NDJSON and some ZIP as base64. Decode, update only real portable time fields, canonicalize with current deterministic byte rules, preserve deliberate negative test paths/format errors.
2. Recalculate package/version/manifest/subject/evidence digests, Version signature envelope and evidence signatures from the existing public fixture test seed, canonical hex/signing input and signatures in vectors/crypto.v2.json.
3. Update every affected fixture hash in conformance/manifest.v2.json. Valid-signature, bad-signature, multi-delivery and later-evidence-append must preserve their intended VALID/BAD and append invariants, not be reclassified to hide failures. Recreate ZIP fixtures if timestamps appear inside them.
4. Add positive/negative samples for literal +00:00, old Z, offset -04:00/+01:00, millisecond-only, omitted fractions, invalid dates and leap seconds; keep the complete existing fixture inventory.
5. Run the actual python3 conformance/check.py with documented jsonschema and cryptography dependencies, record the real output and checksum/Ed25519 checks. Additional schema-pattern assertions already exist in this branch; documentation review does not equal a PASS.
6. Search all normative Chinese/English texts, Schema, fixed vector and fixture bytes for contradictory old UTC-Z time authority. Chinese-English clause ID/strength parity must remain intact.
7. After golden assets are correct, update package-go reference SDK and pinned consumers Cloud/Packtell/PHP/browser verifier, then prove same UTC time yields same Version Subject, signature and verifier result across the supported implementations. This is **one upstream protocol cutover**, not an invitation to relax signature verification or add a legacy reader.

## Implementation sequencing

First complete this isolated package-spec branch and its conformance, then normal PR Merge Commit to package-spec main and read back SHA. Next, update reference package-go and pinned consumer SDKs before claiming the Cloud Goal signed Registry/Version acceptance and S05 time standard complete. Existing Cloud Goal contract that previously exempted portable Z must be revised to reflect the new source authority.

There is no historical Package or old client migration obligation under the Founder's pre-release authorization. Do not modify real user data or unrelated active development contexts.

## Honest status

The original 30 fixtures (including four ZIP inputs) and Ed25519/digest vectors have now been rebuilt from the public TEST ONLY seed. Twelve additional invalid-time fixtures and 16 timestamp samples exercise all 17 date-time fields across 13 schemas. The local checker passes with 17 schemas, 42 fixtures, 203 paired clauses and 13 intentional schema rejections. Its original expectations, malformed archives and evidence append invariants are retained. A missing JSON Schema date-time dependency now fails closed. See [the checker instructions](conformance/README.md) for deterministic regeneration and required dependencies.

This is repository-asset consistency evidence only. package-go reference conformance, downstream Cloud/Packtell/browser verifiers and real official Provider integration remain **NOT RUN** at this upstream stage. Independent review and an ordinary Merge Commit remain required before consumers adopt the new authority.
