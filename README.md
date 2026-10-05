# OrbiFabric Package Protocol 2.0

> **中文主规范 · Official bilingual specification**  
> English: [README.en.md](README.en.md)

本仓库定义 **OrbiFabric Package Protocol 2.0**：一种可脱离 Packtell 独立存在、可被不同实现读写、验证、导入、导出和长期保存历史的通用 Package 对象。

Package 2.0 的核心结构非常简单：

```text
My Package/
├── ordinary user files and folders        # Working Tree
└── .packtell/                              # portable package memory
    ├── format.json
    ├── package.json
    ├── HEAD
    ├── versions/
    ├── objects/
    ├── metadata/
    ├── history/
    ├── verification/
    ├── evidence/
    └── extensions/
```

## 核心原则

- Package Root 对用户就是普通 folder；用户文件直接位于根目录。
- `.packtell/` 是唯一根级控制 namespace，保存协议身份、版本、完整历史、备注、标签、来源、验证材料和扩展。
- Working Tree 可以被 Packtell 外的软件直接修改；相对 `HEAD` 的变化表现为 Dirty，而不是 Package 失效。
- PackageVersion 是不可变逻辑状态；Version manifest 是历史状态 authority。
- File Identity、Content Identity、Materialized Path 永久分离。
- Complete Profile 自包含所有 committed Versions 的 content objects，即使 HEAD bytes 也同时存在于 Working Tree；因此外部覆盖当前文件不会破坏历史恢复。
- 第三方云盘只影响导出时 bytes 如何被 ContentResolver 取得；Complete Package 生成后不依赖 Cloud/Provider。
- Version Signature 绑定 Canonical Version Subject，而不是 ZIP 字节。
- Packtell 默认无 Cloud 时使用本机 Ed25519 package signer；连接并选择 OrbiFabric official signer 时使用 Cloud/official signer。Cloud Anchor、Delivery Receipt、Lifecycle Witness 是不同证据对象。
- Directory 是基础物化；ZIP/TAR/RAR/未来专有容器只是同一 Package Tree 的 codecs。
- Packtell 是参考消费产品，不是协议成立的前提。

## 状态

- Status: **Draft / Pre-release**
- Target protocol: **`orbifabric.package` / `2.0`**
- Tree profile: **`orbifabric.package-tree.v1`**
- Default Packtell export profile: **`orbifabric.package.profile.complete.v1`**
- Package 1.x: **未发布开发期协议；不兼容、不迁移、不保留旧数据或 production legacy runtime。**

## 规范入口

| # | 中文主规范 | English |
|---|---|---|
| 00 | [概览与术语](specification/zh-CN/00-overview.md) | [Overview](specification/en/00-overview.md) |
| 01 | [Core Model](specification/zh-CN/01-core-model.md) | [Core Model](specification/en/01-core-model.md) |
| 02 | [Package Tree](specification/zh-CN/02-package-tree.md) | [Package Tree](specification/en/02-package-tree.md) |
| 03 | [Working Tree / HEAD / Version](specification/zh-CN/03-working-tree-versions.md) | [Working Tree / HEAD / Version](specification/en/03-working-tree-versions.md) |
| 04 | [Content / Complete Profile](specification/zh-CN/04-content-complete-profile.md) | [Content / Complete Profile](specification/en/04-content-complete-profile.md) |
| 05 | [Metadata / History / Provenance](specification/zh-CN/05-portable-metadata-history-provenance.md) | [Metadata / History / Provenance](specification/en/05-portable-metadata-history-provenance.md) |
| 06 | [Verification / Signing](specification/zh-CN/06-verification-signing.md) | [Verification / Signing](specification/en/06-verification-signing.md) |
| 07 | [Delivery / Evidence](specification/zh-CN/07-delivery-evidence.md) | [Delivery / Evidence](specification/en/07-delivery-evidence.md) |
| 08 | [Container Codecs](specification/zh-CN/08-container-codecs.md) | [Container Codecs](specification/en/08-container-codecs.md) |
| 09 | [Conformance / Security](specification/zh-CN/09-conformance-security.md) | [Conformance / Security](specification/en/09-conformance-security.md) |
| 10 | [实施合同](specification/zh-CN/10-implementation-contracts.md) | [Implementation contracts](specification/en/10-implementation-contracts.md) |

治理与权威：[SPEC-AUTHORITY.md](SPEC-AUTHORITY.md) · [English](SPEC-AUTHORITY.en.md)  
1.x Clean Break：[MIGRATION-1X-CLEAN-BREAK.md](MIGRATION-1X-CLEAN-BREAK.md) · [English](MIGRATION-1X-CLEAN-BREAK.en.md)

## 机器可读资产

- [`schemas/`](schemas/) — JSON Schemas
- [`vocabularies/`](vocabularies/) — stable enums/vocabularies
- [`profiles/`](profiles/) — Complete and future profiles
- [`fixtures/`](fixtures/) — valid/invalid Package trees
- [`vectors/`](vectors/) — canonicalization/hash/signature golden vectors
- [`conformance/`](conformance/) — cross-language expected results

实施字段与共享测试资产已在第 10 章冻结。运行 `python3 conformance/check.py` 检查仓库一致性；该检查不构成 SDK conformance 声明。

## Reference Implementation

官方 Go Reference SDK：[github.com/orbifabric/package-go](https://github.com/OrbiFabric/package-go)

Authority 顺序是规范 → Schema → canonical/crypto algorithm → vectors → 英文官方翻译 → `package-go`。如果 Go 实现与规范冲突，应修复实现。

## License

本仓库采用 **Apache License 2.0**。

除非文件另有明确说明，本仓库中的规范、Schema、测试向量、Fixture、示例及其他内容均按 Apache License 2.0 授权。详情见 [LICENSE](LICENSE) 与 [NOTICE](NOTICE)。

## Local consistency / 本地一致性

Python 3.11+ with `jsonschema` 4.18+ and `cryptography` 41+: `python3 conformance/check.py`. No SDK or network is used.
