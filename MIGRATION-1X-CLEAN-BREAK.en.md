# Package 1.x → 2.0 Clean Break

Status: Accepted project policy / Pre-release

Package 1.x was never released as the public Package Protocol. Package 2.0 therefore uses a clean break rather than compatibility migration.

- Old 1.x Package data: **not compatible, not migrated, not retained**.
- 2.0 production Reader: no 1.x fallback.
- 2.0 production Writer: writes 2.0 only.
- 1.x verifier/importer/migration paths: removed from the production runtime after cutover.
- Existing 1.x code, fixtures, and cryptographic primitives: temporary migration references only; correct SHA-256, Merkle, Ed25519, canonical JSON, path-safety, signer, and trust experience may be reused in 2.0.

Recommended engineering order: freeze 2.0 spec → establish `package-go` → cut Packtell callers over incrementally → pass conformance/golden tests → reach zero 1.x production callers → delete 1.x runtime/data paths.

The goal is to avoid manufacturing a permanent legacy burden before the first public release.
