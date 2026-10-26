# Package 2.1 规范权威、语言与变更规则

状态：Draft / Normative Governance  
适用：OrbiFabric Package Protocol 2.x（当前规范发布 2.1）及其子规范

## 1. 规范关键词

本规范使用以下强度词：

- **必须（MUST）**：实现必须满足；
- **不得（MUST NOT）**：实现不得违反；
- **应该（SHOULD）**：除非有明确且可说明的原因，否则应满足；
- **不应该（SHOULD NOT）**：除非有明确且可说明的原因，否则不应实施；
- **可以（MAY）**：可选行为。

中文和英文版本必须保留相同的 RFC 风格强度。

## 2. 权威顺序

发生冲突时，按以下顺序处理：

1. **中文 Normative Specification**；
2. **Machine-readable Schemas**，对结构、类型、required/allowed value 具有规范性；
3. **Canonicalization / Cryptographic Algorithm Specification**，对字节级输入输出具有规范性；
4. **Conformance Vectors / Expected Results**，对已定义测试输入具有规范性；
5. **官方英文版本**；
6. **`package-go` Reference Implementation**；
7. 其他 SDK、CLI、Web Verifier 和产品实现。

如果 Reference Implementation 与规范冲突，应修复实现。

## 3. 双语要求

`PKG-GOV-001`：每一份 Normative 中文文档必须有对应英文文档。  
`PKG-GOV-002`：中英文对应条款必须使用完全一致的 Clause ID。  
`PKG-GOV-003`：协议字段、Schema ID、枚举值、算法名和路径名只使用英文，不建立中英文字段双轨。  
`PKG-GOV-004`：无法消除的自然语言歧义以中文主规范为准。

## 4. Clause ID

规范条款使用稳定 ID：

- `PKG-CORE-*`
- `PKG-TREE-*`
- `PKG-VERSION-*`
- `PKG-CONTENT-*`
- `PKG-META-*`
- `PKG-SIGN-*`
- `PKG-DELIVERY-*`
- `PKG-CODEC-*`
- `PKG-CONF-*`
- `PKG-GOV-*`
- `PKG-STORAGE-*`（2.1 可选存储服务扩展）

已公开的 Clause ID 不因排版或章节移动而复用给不同语义。

## 5. 版本治理

`PKG-GOV-010`：Protocol `2.x` 的 minor 变更必须保持向后兼容。  
`PKG-GOV-011`：破坏 Core 语义、Package Tree 解释、Canonical Subject 或强制字段含义的变更必须升级 Protocol major。  
`PKG-GOV-012`：Notes、Events、Provenance、Evidence 等子 Schema 可以独立版本化，不得因为局部可兼容扩展机械升级整个 Protocol major。  
`PKG-GOV-013`：未知 optional extension 必须可保留并安全忽略；未知 required capability 必须 fail closed。

## 6. Package 1.x 政策

`PKG-GOV-020`：Package 1.x 被定义为正式发布前的开发期协议。  
`PKG-GOV-021`：Package 2.0 不承担 1.x 的 reader、writer、migration 或 data compatibility 义务。  
`PKG-GOV-022`：实现迁移过程中可临时使用 1.x 代码、fixture 或测试作为设计参考，但完成 clean break 后不得保留 production legacy fallback。

## 7. 标准与实现分离

`PKG-GOV-030`：Package Protocol 不依赖 Packtell、Wails、SQLite、OrbiFabric Cloud 或任何单一语言。  
`PKG-GOV-031`：`package-go` 是 Reference Implementation，不是协议权威来源。  
`PKG-GOV-032`：不同语言 SDK 必须依据本规范与同一套 conformance assets 独立实现。

## 8. 2.1 兼容性增补与可选服务

`PKG-GOV-033`：2.1 的可选 Cloud 存储架构 **MUST NOT** 引入对 Cloud/Provider 的 Package Core 依赖，或静默改变现有 `protocol_version="2.0"` 文件、Version Subject、schema、签名与 conformance 的字节语义。

`PKG-GOV-034`：新增 Storage 服务 **MUST** 保持 Control Plane 与可选 Managed/BYO Data Plane 的明确边界；托管备份位于实际 Provider，不等于在控制面持久化用户实体。服务 API 与便携协议应分别版本化。参见 [第 11 章](specification/zh-CN/11-storage-control-plane.md)。

## 9. 开发期 2.0 时间表示规范明确重置（Founder 2026-10-25）

`PKG-GOV-035`：Founder 在任何正式 2.0 发布前，明确批准**一次开发期 2.0 Clean Break**：所有现行 Portable 2.0 时间字段的规范串 MUST 为 UTC RFC3339、**固定六位微秒、字面 `+00:00`**，而非 `Z`。本调整覆盖先前开发快照的 timestamp 字节规范，但不是已发行 2.x 的 minor 兼容升级。实现 MUST 更新 Subject、Schema、Conformance vectors 和验证器，并 MUST NOT 静默把旧 `Z` 输入视为新规范签名。已签名数据的哈希和签名字节随重新生成的新规范内容变化；不得通过字符串替换伪造原签名有效。后续正式发布后的破坏性字节变更继续适用 `PKG-GOV-010/011` 的 major 升级规则。
