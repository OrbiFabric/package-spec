# Conformance / 共享一致性合同

Authority: [中文实施合同](../specification/zh-CN/10-implementation-contracts.md) / [Official English](../specification/en/10-implementation-contracts.md).

[manifest.v2.json](manifest.v2.json) lists Core Reader, Core Writer, Complete Reader, Complete Writer, Verifier, Directory Codec and ZIP Codec cases. IDs and expected results are protocol assets, never generated from package-go output.

## Input / 输入

Each referenced fixture is a UTF-8 JSON document with id, input, expected. `input.kind=tree` supplies an ordered entries array: path is a relative UTF-8 path, directory entries have a trailing slash and no bytes; files have standard padded `bytes_base64`. Implicit parent directories are permitted. Decode bytes without newline or Unicode conversion. The array preserves duplicate entries if a case requires them. Paths are untrusted test data; feed a virtual tree or safe preflight interface before materialization. `input.kind=zip` contains standard padded base64 archive bytes; feed them directly to the codec.

Each result has recognition, structure, working_state, committed_integrity, history_completeness, signature, identity, evidence, online and reason_codes. NOT_CHECKED is an intentional short circuit, never a success. Evaluate unsafe paths before opening payload files, unsupported required capabilities before history, then schema/topology before content. Hash/signature/evidence dimensions remain independent. A runner may perform more safe checks, but must match each tested dimension that is not NOT_CHECKED and include the expected reason codes. It must never report PASS for a failed mandatory dimension. Missing objects are unavailable integrity and NOT_FULL, not evidence failure. Negative signature input still has FULL content history.

中文：按 manifest 载入 fixture，先做安全预检，再识别能力、结构/历史、对象、签名和证据；各维度独立报告。NOT_CHECKED 不代表通过。测试报告必须包含规范 exact commit、实现 exact commit、声明 level、逐 case 实际值与期望值、资源策略及未运行项。

## Level adapters / 级别适配

Each case lists its applicable levels; Core-only implementations are not required to interpret portable-memory. Additional capability claims require the corresponding Complete/Verifier cases. Readers inspect tree fixtures and report structural/working/history facts; Complete Readers additionally prove all-version offline object coverage. Verifiers consume crypto vectors and all signature/evidence cases without trusting embedded keys. Directory Codec materializes each safe tree into an isolated temporary root and reads it back; unsafe tree input must fail before output publication. ZIP Codec consumes ZIP inputs and encodes/decodes valid tree fixtures with a single wrapper directory. Writers consume valid trees, preserve IDs/unknown optional facts/extension bytes and round-trip logical state through their output; negative source trees must fail validation rather than be silently repaired. Core Writer may preserve Complete data without claiming Complete Writer until it proves all coverage. Complete Writer must export all historical bytes without borrowing Working Tree bytes for missing committed objects.

Writer operations in manifest test expected-HEAD compare-and-commit: stale input publishes no committed Version; successful commit has the single expected parent and next ordinal. The fixture pairs minimal-valid→renamed-file/moved-file/modified-file test stable FileID with path/content changes; complete-history must reconstruct both versions offline. multi-delivery→later-evidence-append must preserve subjects, Version signatures and receipt-bound Delivery digests. unknown-optional-extension must preserve exact opaque bytes on round-trip.

## Local checker / 仓库检查

Run `python3 conformance/check.py` with Python 3.11+, jsonschema 4.18+, cryptography 41+. It checks bilingual clause parity and strength, JSON syntax/schema structure, offline references, fixture schema expectations, vector digests/Ed25519 signatures, fixture hashes, invariants and Markdown links. It does not implement a consumer SDK or certify implementations. Full filesystem, archive, fuzz, concurrent writer and product tests belong to downstream implementations; their results cannot be inferred from this consistency PASS. No network/SDK/production key is used. Dependencies are development tools, not protocol dependencies.
