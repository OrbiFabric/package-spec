# Package 1.x → 2.0 Clean Break

状态：Accepted project policy / Pre-release

Package 1.x 从未作为正式公开 Package Protocol 发布。Package 2.0 因此采用 clean break，而不是兼容迁移。

- 旧 1.x Package 数据：**不兼容、不迁移、不要旧数据**。
- 2.0 production Reader：不保留 1.x fallback。
- 2.0 production Writer：只写 2.0。
- 1.x verifier/importer/migration：完成切换后从 production runtime 删除。
- 现有 1.x 代码、fixture、密码学 primitive：只作为迁移开发期参考；正确的 SHA-256、Merkle、Ed25519、canonical JSON、path safety 与 signer/trust 经验可以重用到 2.0。

推荐工程切换顺序：2.0 规范冻结 → `package-go` 建立 → Packtell caller 逐项切换 → conformance/golden PASS → 1.x production caller = 0 → 删除 1.x runtime/data paths。

本政策的目标是避免在首次正式发布前人为制造永久 legacy burden。
