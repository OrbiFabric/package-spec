# Pre-release Portable 2.0 UTC cutover — repository gate

Scope: Founder-authorized unreleased-development clean break, tracked by [Cloud Goal #690](https://github.com/OrbiFabric/orbifabric-cloud/issues/690) and [package-spec PR #4](https://github.com/OrbiFabric/package-spec/pull/4). No historical data migration, production signing or release authorization.

Tested and independently reviewed implementation: `42a78edf1ff10e6dcf37019e6d4ff7fde1dd9483`, based on main `81b8d45adeb212d0035faf358370de760282a4cf`. Subsequent report-only commits do not change the reviewed schemas, checker, fixtures or vectors. Ordinary Merge Commit and exact main read-back are recorded in PR #4.

The canonical time is UTC RFC3339 with exactly six fractional digits and literal `+00:00`. The Chinese/English normative clauses, 13 timestamp schemas (17 fields), all 30 original fixtures including four ZIP archives, VersionSubject digests, Version/Evidence Ed25519 envelopes and manifest SHA-256 inventory are updated. Fifteen new rejection fixtures cover old Z, other offsets, variable precision, impossible dates, leap seconds, year zero and trailing whitespace. All original expected results remain unchanged.

## Actual local verification

Isolated tool environment: `/tmp/packtell-protocol-utc-conformance-20261025`, Python 3.14, jsonschema 4.26.0 with format extras, cryptography 50.0.2, rfc3339-validator 0.1.4. No product or Provider credentials used.

Executed commands:

```sh
PYTHONDONTWRITEBYTECODE=1 /tmp/packtell-protocol-utc-conformance-20261025/bin/python conformance/regenerate_utc_assets.py
/tmp/packtell-protocol-utc-conformance-20261025/bin/python conformance/check.py
git diff --check
```

Result: **PASS: 17 schemas; 45 fixtures; 203 paired clauses; 16 expected schema rejection; canonical/hash/Ed25519 vectors; evidence invariants; local links.** A second regeneration was compared using SHA-256 across all 47 fixture/vector/manifest files: byte-identical, PASS. Independent in-memory reconstruction also reproduced all 47 assets.

New canonical subject digest: `sha256:deb4897f46dda45fa4f592f2c02a161abafb2d5db09dbb20101f523e98968e41`. Public key/fingerprint, content bytes/digests, entity IDs, signature domains and original append invariants are retained. New signed bytes are genuinely re-signed using the public TEST ONLY seed, not substituted under old signatures.

## Failures found and resolved

The inherited Draft failed on `schema expectation minimal-valid` because embedded bytes still used Z. Regenerating test assets repaired that failure. Calendar rejection tests then exposed an incomplete ambient jsonschema installation: `date-time` was silently unchecked. The checker now refuses a missing date-time checker; the declared format extras are installed in the isolated environment.

Independent review of `174e232f5c126056b6cb412a6ead05f367c16f16` found that `$` allowed a final LF in timestamp schemas. Commit `42a78edf1ff10e6dcf37019e6d4ff7fde1dd9483` replaces it with the strict end assertion `(?![\s\S])` in all 17 time patterns and adds LF/CRLF/space rejection fixtures. Review repeated only the affected increment plus the complete checker; no unresolved blocker remains.

## Independent technical review

Reviewer: separate agent `/root/protocol_review`, implementation SHA `42a78edf1ff10e6dcf37019e6d4ff7fde1dd9483`. Read-only review compared the original 30 fixture expectations, ordered entries, payload/HEAD/opaque bytes and ZIP metadata/faults; independently derived VersionSubject without importing the checker; reproduced the public-seed signatures; verified four valid envelopes including Evidence and rejected the bad-signature case. It also checked all 17 time fields against LF/CRLF/space/Tab/CR/Unicode separators, old Z, invalid dates and leap seconds. Conclusion: independent review PASS, no remaining blocking finding.

This is repository consistency and crypto asset evidence. **SDK reference conformance, Cloud/Packtell/Bellfly integration, real official Provider signing, native acceptance and remote CI: NOT_RUN at this gate.** Consumer pins must adopt the merged specification and revalidate their own behavior. Production and public release remain unauthorized.
