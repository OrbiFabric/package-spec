# Package Protocol 2.0 — Canonical UTC offset-time correction

> Founder approved on 2026-10-25. Status: IMPLEMENTATION_CONTRACT / CONFORMANCE_NOT_RUN.
> Target: all protocol-owned timestamps use the OrbiFabric Cloud AuditTrail format,
> `YYYY-MM-DDTHH:mm:ss.ffffff+00:00`, UTC, exactly six fractional microseconds.
> Current spec main still requires the `Z` spelling. This is an intentional
> coordinated clean break of the timestamp representation, NOT an already accepted
> protocol revision. No pre-release historical data migration is required.
> **Do not merge this branch into main before all new fixture hashes, digests,
> Ed25519 test signatures and conformance checks are regenerated and PASS.**

## Why this must be atomic

The old PKG-CONTRACT-020 normatively enforces `YYYY-MM-DDTHH:mm:ss.ffffffZ`.
Version subject contains created_at; the version-signature envelope contains signed_at.
The canonical signed JSON bytes and SHA-256 domain-separated digests therefore change
when timestamp serialization switches to the literal `+00:00` suffix.
A regex/schema-only migration would make existing crypto.v2 vectors and
valid-signature fixtures invalid. Do not change validation without regenerating
the corresponding canonical test inputs, hashes, signatures and expected outcomes.

## Implementation requirements

1. Read the three repositories' current identity/time contracts and this repository's
   authority: SPEC-AUTHORITY.md, 10-implementation-contracts in zh-CN/en,
   schemas/README.md, schemas/*.schema.json, fixtures/*, vectors/*,
   conformance/check.py and every linked fixture manifest, hash inventory, diagram,
   sample/negative vector and executable conformance rule.
2. Update every *protocol-owned* DateTime schema/parser/example/positive fixture
   to require strict UTC RFC3339 `YYYY-MM-DDTHH:mm:ss.ffffff+00:00`.
   Reject old `Z`, non-UTC offsets, missing fractional part,
   non-six fractional digits, invalid calendar dates, seconds=60.
   Preserve exact canonical codepoint ordering and representation, not ordinary
   parser equivalent semantics. Update both language specifications identically.
3. Keep RFC 9562 UUIDv7 requirements, canonical JSON, SHA-256, Version/Signature
   identity, domain separation, Ed25519 validation, graph consistency and
   feature/capability contracts unchanged in meaning. The only authorized
   cryptographic input change is the timestamp spelling for newly generated
   subjects/evidence. Do not reuse old signature bytes with new timestamps.
4. Regenerate **deterministically** all affected positive fixtures, signatures,
   signed subjects, version_digest, subject_digest, canonical byte hashes, manifests,
   cryptographic test vectors and golden references using designated **public test
   seed fixtures** where present. Never import or use live signing keys or Provider
   credentials. Verify the produced vector with an independently derived public key,
   an independent Ed25519 verify path, and SHA-256 recomputation.
5. Update negative fixtures/expected error classifications: old `Z` is now a
   format rejection in this clean-break profile, non-UTC `+01:00` etc rejected;
   genuine signature/tamper negatives must remain actually invalid for the reason
   their oracle states after rebuilding valid inputs.
6. Run `python3 conformance/check.py` with its documented Python/dependencies.
   Run bilateral clause parity, JSON Schema, all fixture expectations, real
   canonical hashes, all Ed25519 crypto vector checks, manifest hash references,
   path/link checks and owned unit tests. No bypass, no assertion deletions to
   manufacture a PASS. Record actual commands, environment, counts and errors.
7. Document that this intentional pre-release timestamp clean break requires
   **same-version consumer update** in Cloud, Packtell and Bellfly where they
   read/write protocol timestamps. Do not claim spec-only PASS establishes
   the SDK/Cloud consumers are ready. Caller realignment belongs to the
   cross-product Goal's S05 and final S06 acceptance.
8. Do not rewrite old Git history, published conformance reports, sealed
   in-use user data, or unrelated protocol wire domains. Do not bump to 2.1
   or change unrelated schemas. If existing version/compatibility gates
   require a formal protocol compatibility/version decision, document the
   exact gate and stop rather than silently ignoring it.

## Git and reporting

Work only on existing local repository Git branch
`goal/utc-microseconds-offset-20261025`; no worktree, no production deployment,
no direct push to main. Create a report `docs/UTC-OFFSET-IMPLEMENTATION-RESULT.zh-CN.md`
showing affected field inventory, all updated fixture/vector hashes, actual
conformance results, unsigned/signed subject changes, immutable omitted domains,
actual code SHA and the blocked/passed conditions.

Only after full conformance and independent review: normal GitHub PR,
ordinary Merge Commit, readback of package-spec main and an explicit
cross-repo consumer handoff. A failed or unrun conformance is BLOCKED,
not PASS, and must not be merged.

## Completion state

- `SPEC_UTC_OFFSET_CONFORMANCE_ACCEPTED`: all spec-owned schemas, normal and
  negative vectors, digests and Ed25519 signatures consistent and tested.
- `SPEC_UTC_OFFSET_BLOCKED_WITH_EXACT_REASON`: any broken digest, signature,
  manifest, needed protocol decision, conflict or unavailable validation.
