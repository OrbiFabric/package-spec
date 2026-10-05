# Package 2.0 Core Model

状态：Draft / Normative

## 1. 标识符

`PKG-CORE-100`：`package_id`、`package_version_id`、`file_id`、`folder_id`、`event_id`、`delivery_id` MUST 使用 UUIDv7 文本表示。

`PKG-CORE-101`：UUID MUST 使用 RFC 4122/9562 风格小写连字符文本；实现 MUST NOT 依赖数据库自增 ID 作为 portable identity。

`PKG-CORE-102`：`content_id` MUST 为 `sha256:<64 lowercase hex>`。

`PKG-CORE-103`：相同 bytes MUST 得到相同 ContentID；不同 FileID MAY 指向相同 ContentID。

## 2. File、Folder、Path、Content

`PKG-CORE-110`：File/Folder 的逻辑身份 MUST 独立于名称与路径。

`PKG-CORE-111`：重命名或移动一个 File/Folder MUST 保持其 ID 不变。

`PKG-CORE-112`：修改文件内容 MUST 保持 `file_id` 不变并产生新的 `content_id`。

`PKG-CORE-113`：复制文件 MUST 产生新的 `file_id`，但 MAY 复用相同 `content_id`。

`PKG-CORE-114`：逻辑树 authority MUST 使用 parent relationship + name 表达；materialized path 是派生结果，不是 identity。

## 3. Package 与 Version

`PKG-CORE-120`：Package 是 mutable long-lived entity；PackageVersion 是 immutable logical snapshot。

`PKG-CORE-121`：已 committed Version 的文件集合、FileID、FolderID、ContentID、版本级 sealed metadata 与 lineage MUST NOT 被静默改写。

`PKG-CORE-122`：任何需要改变上述 Version authority 的修改 MUST 创建新的 PackageVersion。

`PKG-CORE-123`：Tags、Notes、后续 Delivery、Witness、Receipt 与其他 lifecycle/evidence MAY 在不创建新 PackageVersion 的情况下追加，但其 portable history MUST 保留。

## 4. 时间与文本

`PKG-CORE-130`：协议字符串使用 UTF-8；机器路径组件在进入 portable authority 前 MUST 经过 Unicode NFC normalization。

`PKG-CORE-131`：Canonical timestamp MUST 使用 UTC RFC3339，格式 `YYYY-MM-DDThh:mm:ss.ffffffZ`。

`PKG-CORE-132`：协议 authority 中的计数、size、ordinal MUST 使用非负整数，MUST NOT 使用浮点数表达精确身份事实。

## 5. `package.json`

`.packtell/package.json` 保存稳定 Package identity 与创建事实，不是 Packtell 数据库 dump。

最小概念字段：

```json
{
  "created_at": "2026-10-05T00:00:00.000000Z",
  "package_id": "019a0000-0000-7000-8000-000000000001",
  "schema": "orbifabric.package.package.v2"
}
```

`PKG-CORE-140`：`package.json` MUST NOT 包含 OAuth token、credential、OS Keyring 引用、绝对本地路径、Cloud session 或内部数据库 row ID。

[实施精确合同](10-implementation-contracts.md)将本章概念冻结为字段、字节和关系约束。
