# Portable Metadata、History 与 Provenance

状态：Draft / Normative

## 1. Portable metadata

`.packtell/metadata/` 保存跨实现有意义的 Package metadata，例如：

```text
metadata/
├── package.json
├── tags.json
├── notes.json
└── provenance.json
```

`PKG-META-001`：Portable metadata MUST 表达 Package 语义，不得作为 Packtell SQLite/ORM 结构的序列化镜像。

`PKG-META-002`：Notes MUST 使用稳定 `note_id`；修改 Note 不得通过删除旧字符串再创建无关联字符串来伪装。

`PKG-META-003`：Tags SHOULD 使用规范化文本值；实现 MAY 为 tag 提供稳定 ID，但不得要求某个 Packtell 数据库 ID。

## 2. Portable domain history

`PKG-META-010`：`.packtell/history/events.ndjson` MAY 保存 append-oriented portable domain events。

建议 vocabulary 包括：

`PACKAGE_CREATED`、`FILE_ADDED`、`FILE_REMOVED`、`FILE_MOVED`、`FILE_RENAMED`、`FILE_CONTENT_CHANGED`、`VERSION_CREATED`、`TAG_ADDED`、`TAG_REMOVED`、`NOTE_CREATED`、`NOTE_UPDATED`、`NOTE_DELETED`、`PACKAGE_ARCHIVED`、`PACKAGE_RESTORED`、`DELIVERY_CREATED`、`DELIVERY_COMPLETED`、`WITNESS_ATTACHED`、`PACKAGE_IMPORTED`、`PACKAGE_EXPORTED`、`PROTOCOL_MIGRATED`。

`PKG-META-011`：Portable events MUST NOT 包含 UI 点击、cache rebuild、worker lease、sync retry、telemetry、临时下载 job、绝对本地路径或 credential。

`PKG-META-012`：Version manifest 是 Version state authority；events 用于解释 chronology，不得要求 replay events 才能恢复 committed Version。

`PKG-META-013`：未知 optional event type MUST 可原样保留；Reader MAY 以 generic event 展示而不理解其业务语义。

## 3. Provenance

`PKG-META-020`：Provenance MAY 同时存在 Package-level、File-level 与 Content-level facts。

建议来源 kind：`local_import`、`package_import`、`google_drive`、`onedrive`、`dropbox`、`external_api`、`generated`、`other`。

`PKG-META-021`：Provenance MAY 保存 privacy-safe source object ID、source revision、original name、first observed time 与 source Package/Version reference。

`PKG-META-022`：Provenance MUST NOT 保存 OAuth/refresh token、session、credential、signed URL、OS Keyring locator 或非必要绝对路径。

`PKG-META-023`：Source facts MUST NOT 改变 FileID/ContentID authority；来源是“从哪里来”，不是“现在依赖哪里才能存在”。

## 4. Extensions

`PKG-META-030`：第三方扩展 MUST 位于 `.packtell/extensions/<reverse-domain-or-stable-namespace>/`。

`PKG-META-031`：未知 optional extension MUST 可被 preserve-through-read/write，除非用户明确要求删除。

`PKG-META-032`：Extension MUST NOT 覆盖 Core path、伪造 Core schema 或要求 Reader 执行未信任代码才能读取 Core Package。
