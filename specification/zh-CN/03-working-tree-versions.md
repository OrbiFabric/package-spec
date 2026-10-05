# Working Tree、HEAD 与 Version History

状态：Draft / Normative

## 1. Working Tree

`PKG-VERSION-001`：Package Root 中除根级 `.packtell/` 外的树 MUST 定义当前 Working Tree。

`PKG-VERSION-002`：Working Tree MAY 被 Packtell 之外的软件直接修改；这种修改 MUST NOT 使 Package 丢失身份。

`PKG-VERSION-003`：Reader MUST 将 Package recognition 与 Working Tree state 分开报告。

推荐状态：`UNBORN`、`CLEAN`、`DIRTY`、`UNREADABLE`。

## 2. HEAD

`PKG-VERSION-010`：`.packtell/HEAD` MUST 引用最近 committed PackageVersion，首次提交前使用规范 unborn 表达。

`PKG-VERSION-011`：HEAD MUST NOT 因普通 Working Tree 改动而自动移动。

`PKG-VERSION-012`：当 Working Tree 与 HEAD Version logical state 不一致时，Package 状态 MUST 为 Dirty，而不是 Invalid。

## 3. Version authority

每个 Version 至少包含：

```text
versions/<package-version-id>/
├── version.json
└── manifest.json
```

`PKG-VERSION-020`：`manifest.json` MUST 是该 Version 完整逻辑文件/目录状态的 authority；events MUST NOT 成为恢复 Version 所必需的唯一来源。

`PKG-VERSION-021`：Version manifest MUST 记录稳定 FileID/FolderID、parent relationship、name、kind；file entry 还 MUST 记录 ContentID 与 size。

`PKG-VERSION-022`：Version MAY 有 ordinal 与 label，但 `package_version_id` 是 portable identity。

`PKG-VERSION-023`：版本 lineage MUST 使用 previous/parent VersionID 表达，MUST NOT 以文件名顺序推断。

## 4. Dirty export

`PKG-VERSION-030`：Dirty Package MAY 被导出为 Package Repository；导出 MUST 明确区分 committed history 与未提交 Working Tree。

`PKG-VERSION-031`：Dirty Working Tree MUST NOT 冒充 HEAD 的已签名 logical state。

`PKG-VERSION-032`：要求正式交付、Version Seal 或对当前状态进行 committed verification 的动作 MUST 先创建新的 PackageVersion。

## 5. 外部修改检测

`PKG-VERSION-040`：Diff MUST 至少能够报告 Added、Removed、Moved/Renamed 与 Content Changed。

`PKG-VERSION-041`：Path 变化与 Content 变化 MUST 分开表达；相同 FileID 的 rename MUST NOT 伪装为 delete+new-file，除非实现无法建立合法 identity continuity。

[实施精确合同](10-implementation-contracts.md)将本章概念冻结为字段、字节和关系约束。
