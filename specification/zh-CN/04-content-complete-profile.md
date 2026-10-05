# Content Object 与 Complete Profile

状态：Draft / Normative  
Profile：`orbifabric.package.profile.complete.v1`

## 1. Content Object Store

Committed Version 的内容 bytes 使用 ContentID 去重保存于 Package portable object store：

```text
.packtell/objects/sha256/<prefix>/<digest>
```

`PKG-CONTENT-001`：Object path MUST 由 ContentID 确定；object bytes 的 SHA-256 MUST 与 ContentID 匹配。

`PKG-CONTENT-002`：同一 ContentID 被多个 FileVersion/PackageVersion 引用时，Complete Profile SHOULD 只保存一份 object bytes。

`PKG-CONTENT-003`：Complete Profile MUST 保存重建**所有 committed Versions**所需的全部 content objects，包括当前 HEAD 已在 Working Tree 中可见的内容。

> 说明：即使 HEAD bytes 当前也存在于 Working Tree，仍必须在 object store 中保存 committed copy；否则外部软件覆盖 Working Tree 后会破坏历史 Version 的离线可恢复性。

## 2. Working Tree 与 Object Store

`PKG-CONTENT-010`：Working Tree 是用户工作副本；object store 是 committed content authority 的 portable backing store。两者 MAY 物理重复相同 bytes。

`PKG-CONTENT-011`：实现 MAY 在本地使用 reflink、copy-on-write 或其他透明优化，但 portable semantics MUST 等价于独立可读取的 object bytes；不得依赖 symlink/hardlink 才能恢复历史。

## 3. Complete Profile

`PKG-CONTENT-020`：Complete Profile MUST 自包含以下内容：所有 committed Version manifests、所有 required content objects、当前 portable metadata、portable history、provenance、required verification material 与声明为内嵌的 evidence。

`PKG-CONTENT-021`：Complete Profile 验证 MUST 检查每个 committed Version 的所有 ContentID 都能从 Package 自身 materialize，而不访问网络。

`PKG-CONTENT-022`：若任一 committed content object 缺失、hash 不匹配或不可读取，Package MUST NOT 宣称 `history_completeness=FULL`。

## 4. 第三方存储导出

Package Protocol 不认识特定 Provider；Host 通过 Content Resolver 提供 bytes。

`PKG-CONTENT-030`：Exporter MUST 以 ContentID 为请求边界，不得要求 Package Core 了解 Google Drive、OneDrive、Dropbox、S3 或 NAS API。

`PKG-CONTENT-031`：远端 bytes MAY 直接流入 export staging；它们不必先永久写入 Packtell 本地 managed store。

`PKG-CONTENT-032`：正式 materialization MUST 对流入 bytes 重新计算 SHA-256 并与 expected ContentID 匹配；不匹配 MUST fail closed。

`PKG-CONTENT-033`：若来源具有 revision/version token，Host SHOULD 在读取前后验证同一 remote revision，禁止把不同 revision 拼成一个 ContentObject。

`PKG-CONTENT-034`：同一 export operation SHOULD 按 ContentID 去重远程读取。

## 5. Provenance 与自包含

`PKG-CONTENT-040`：Complete Profile MAY 记录原 Provider、object ID、revision 与 first-observed facts 作为 provenance，但这些字段 MUST NOT 成为打开/恢复 Package 的运行时依赖。

`PKG-CONTENT-041`：Credential-bearing URL、OAuth token、refresh token、signed URL 与 secret MUST NOT 进入 Package。
