# Package 2.0 implementation contract closure review

This is a review record, not additional protocol authority. Primary normative text is [中文 chapter 10](../specification/zh-CN/10-implementation-contracts.md); [English](../specification/en/10-implementation-contracts.md) is its official translation.

| Gate | Frozen authority / evidence |
|---|---|
| Exact Root paths, discriminator, HEAD bytes and unborn | PKG-CONTRACT-002/003/005; format/package schemas; core-minimal/unborn/invalid-head-crlf |
| Single linear history, ordinal and stale authority | PKG-CONTRACT-004/020; version schema; cycle/missing-parent/multiple-roots/detached-version/multiple-parents; writer operations |
| Complete manifest/identity/content/history | PKG-CONTRACT-007/008/010/018; manifest schema; complete profile; history/rename/move/modified/dirty/missing/hash cases |
| Portable notes/tags/provenance/events | PKG-CONTRACT-013/014/020; five metadata schemas; cloud-origin-provenance |
| Canonical bytes and VersionSubjectV2 | PKG-CONTRACT-009/011/022; subject schema; crypto.v2 golden bytes/digests |
| Signatures and distinct evidence subjects | PKG-CONTRACT-012/015/021/022; signature/delivery/four evidence subjects/envelope schemas; valid/bad signature, multi-delivery/later-evidence-append |
| Portable filesystem and codec identity separation | PKG-CONTRACT-016/017; traversal/case/NFC and wrapped/unwrapped/unsafe ZIP cases |
| Capabilities/extensions/unknown facts | PKG-CONTRACT-001/005/019/020; vocabulary; unknown optional extension/required capability |
| Language-independent asset consumption | conformance manifest/README; 7 levels, explicit resource/trust policy, 30 fixtures, writer operation contract |
| Bilingual parity | 160 clause IDs, per-clause MUST/MUST NOT/SHOULD/SHOULD NOT/MAY parity; matching new chapter sections |
| License and product boundary | Apache-2.0 unchanged; no DB schema, Provider API, Cloud online dependency or production keys |

Local evidence: `python3 conformance/check.py` PASS; `git diff --check` PASS. An independent OpenSSL `pkeyutl -verify -pubin -keyform DER -rawin` check verifies the stored signing input/signature with the test public key. A temporary corrupted manifest digest is rejected by the checker and the original vector was restored before final checks. All JSON assets are strictly parsed by the checker; all schema references resolve offline.

Review distinguishes structural JSON validation from relational/cryptographic rules: JSON Schema alone is insufficient to claim conformance. The checker validates assets and golden cryptography; it does not claim to test a future SDK's filesystem safety, crash consistency, concurrent writer behavior or product workflows. Downstream implementations must run the shared cases and their own unit/fuzz/integration suites.

Remaining implementation choices: API/package organization, streaming/buffering, scheduling, Host transaction/locking implementation, trust configuration and resource ceilings. These choices cannot change the normative fields, canonical bytes or results. Branching/merge is out of scope, not a deferred parent-array feature. No unresolved normative Founder decision remains in this closure.

Remote CI / GitHub Actions: NOT RUN. SDK implementation: NOT STARTED.
