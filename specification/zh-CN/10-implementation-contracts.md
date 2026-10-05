# Package 2.0 Implementation Contracts / 实施合同

中文 Primary Normative Text。

## 1. Contract authority / 合同权威

`PKG-CONTRACT-001`: 本章把 00–09 的概念字段冻结为 exact contract；同主题的“建议字段/概念示例”由本章及 schemas/ 替代。实现 MUST 同时验证 JSON Schema 2020-12 的结构与本章的关系/字节约束。Schema 的 `$id` 是稳定标识，不要求联网解引用；仓库文件是离线副本。所有控制 JSON MUST 是合法 UTF-8、无 BOM、无重复 key、无孤立 surrogate、无尾随第二个 JSON 值。未知 optional 属性仅在 schema 允许 additionalProperties 的位置保留并安全忽略；闭合对象未知字段拒绝，扩展使用声明 namespace。未知字段 MUST NOT 改变已知 Core 字段语义。

## 2. Exact tree / 精确目录

`PKG-CONTRACT-002`: Core MUST 有 `.packtell/format.json`、`package.json`、`HEAD`、`versions/`、`objects/sha256/`（后四项均相对 `.packtell/`）。每个 committed Version 目录 MUST 为 `versions/<package_version_id>/`，恰含 `version.json` 与 `manifest.json`；VersionSubject 是派生值，不另存 authority 文件。objects 路径为 `objects/sha256/<digest前2字符>/<完整64字符digest>`，文件内容就是原始 bytes，不加 header。metadata/package.json、notes.json、tags.json、provenance.json 与 history/events.ndjson 在 Core 可省略（分别解释为空 title、空 revisions/records/events）；Complete 必需。verification/versions/<version_id>/<signature_id>.json 保存 signature；evidence/deliveries/<delivery_id>/delivery.json 保存 delivery；evidence/objects/<evidence_id>.json 保存 evidence。extensions/<namespace>/ 下保存任意安全 regular files/directories。其余 control 路径 MUST NOT 出现；未使用的可选目录可省略。用户 Root 可有任意合法 payload 名称，但根级 `.packtell` 的 case-fold/NFC 别名保留；子目录 `.packtell` 是普通 payload。读者 MUST 只检查调用者指定 Root 的 discriminator，不向父子目录递归猜 authority。

## 3. HEAD bytes / HEAD 字节

`PKG-CONTRACT-003`: HEAD MUST 恰为 ASCII `unborn` 加一个 LF（hex `756e626f726e0a`），或小写 UUIDv7 加一个 LF（37 bytes）。不得 BOM、CRLF、空格、额外行、JSON 引号、空文件或无 LF。unborn 时 versions/ MUST 为空；committed HEAD MUST 对应同一 Package 的现存 Version 目录。错误编码为 INVALID_HEAD；编码合法但所指 Version 缺失为 MISSING_PARENT。普通 payload 改动 MUST NOT 移动 HEAD。

## 4. Linear history / 线性历史

`PKG-CONTRACT-004`: Version 的 parent_version_id MUST 始终存在：唯一 root 为 JSON null，其 ordinal=1；后续为恰好一个 UUIDv7，ordinal=parent.ordinal+1。ordinal MUST 是 1..9007199254740991 的整数，不能作为 identity。HEAD→parent 链 MUST 覆盖 versions/ 下全部目录且只覆盖一次；cycle、多 root、detached、重复 ordinal、跨 Package parent、parent array、branches/named refs/merge/DAG 均 INVALID（缺失 parent 用 MISSING_PARENT，schema 形状错误为 INVALID_SCHEMA，其余 NON_LINEAR_HISTORY）。Dirty 不创建 branch。并发/离线 writer MUST 在发布前比较预期 HEAD 与实际 HEAD，stale 时返回 STALE_HEAD 并先 reconcile；不得静默提交分叉。尚未接受的 proposal 不属于 committed history，MUST NOT 放入 versions/。copy/reuse/derivation/supersession 使用 provenance relationship；未来 branching 需要独立兼容决策，可能需要 major 升级。

## 5. Format and identity / 格式与身份

`PKG-CONTRACT-005`: format.v2.schema.json 与 package.v2.schema.json 冻结 discriminator 和稳定创建事实。protocol=`orbifabric.package`、protocol_version=`2.0`、tree_profile=`orbifabric.package-tree.v1` MUST exact match；缺 discriminator 为 NOT_PACKAGE，其他 protocol/version/tree 为 UNSUPPORTED。profiles/required_capabilities/optional_capabilities MUST 无重复并按 UTF-8 字节序排序；两类 capability 不重叠。未知 required capability MUST fail closed 为 UNKNOWN_REQUIRED_CAPABILITY；未知 optional capability 保留。未知 profile 返回 UNSUPPORTED，不得宣称通过其 conformance。extension declaration 的 namespace 唯一且排序；required_capability=null 表示 optional，否则该值 MUST 在 required_capabilities 中。extension 路径与 declaration 一一对应；空 extension 目录也可声明。Package identity/created_at 在生命周期中不可变。

## 6. Version fields / Version 字段

`PKG-CONTRACT-006`: version.v2.schema.json 的 package_id/package_version_id 与目录、manifest MUST 一致；created_at 是提交事实而非可信第三方时间。protocol/tree 必须符合本章；profiles/capabilities 是提交时冻结引用，后续 format 变化不得回写它们，且读取所有历史 Version 时也要检查 required capability。当前 format 的 required_capabilities MUST 覆盖全部历史 Version 所需 capability。sealed_metadata 是该 Version 的不可变快照，title 必需但允许空文本，description/extensions 可选；当前 metadata 修改不改它。label 是可选已封存显示值，MUST NOT 决定 identity。空 Package、仅空目录 Version 合法。签名、representation、Delivery 和网络不是 Version 存在的前置条件。

## 7. Manifest and identity / Manifest 与身份

`PKG-CONTRACT-007`: manifest.v2.schema.json 的 entries MUST 为整个历史逻辑树；隐式 Root 没有 FolderID/name/entry。Root 子项 parent_folder_id=null；其余 parent MUST 指向同一 manifest 的 folder。file 仅有 file_id，folder 仅有 folder_id，禁止同时出现两种 identity；所有 entry ID 在 manifest 内唯一且跨版本不得换 kind/重用给另一实体。entries MUST 按 entry UUID 文本 UTF-8 序排序（跨 file/folder 同一序）。name 是单 NFC component；完整 path 递归 parent+name 派生；拒绝 cycle、孤儿、sibling collision。empty folder 有明确 entry。rename/move 保持 ID；content change 保持 FileID 改 ContentID；copy 使用新 ID。相同 ContentID 的 size MUST 一致。未知 optional manifest/entry 字段参与完整 manifest digest，但不能改已知语义。

## 8. Working Tree and diff / 工作树与差异

`PKG-CONTRACT-008`: Reader MUST 以当前 Root payload 的 derived paths、kind、whole-file ContentID/size 与 HEAD manifest 比较，包含空目录，忽略 permissions/mtime/owner/inode。HEAD 为 unborn 时为 UNBORN；相同为 CLEAN；新增/删除/移动/改名/内容不同为 DIRTY；无法安全读取为 UNREADABLE。DIRTY MUST NOT 导致 committed content integrity 失败。外部文件系统本身不携带 FileID；同 path/kind 允许沿用 HEAD ID，显式 Host identity tracking 可证明 rename/move；仅相同 bytes 不足以唯一确定 copy/rename，歧义时 Added/Removed，禁止伪造 continuity。Diff MUST 分开表达 ID 对应的 path 与 content 变化。新的扫描 ID 和 proposal 属于 Host 工作状态，提交时才进入 manifest。

## 9. Canonical JSON bytes / Canonical JSON 字节

`PKG-CONTRACT-009`: 定义 J(x)=orbifabric.canonical-json.v1 在 Package 2.0 的受限域：null/boolean/string/array/object 与整数，整数范围 -9007199254740991..9007199254740991。解析输入 MUST 拒绝浮点、指数、-0、NaN/Infinity；整数仅 `0` 或 `-?[1-9][0-9]*`。object key 按 Unicode scalar 的 UTF-8 字节词法序递归排序；array 保留顺序。字符串 MUST 只转义 quote 为 `\"`、backslash 为 `\\`、U+0008/0009/000A/000C/000D 为 `\b/\t/\n/\f/\r`，其他 U+0000..001F 为小写 `\u00xx`；其余 scalar 直接 UTF-8（包括 /、<、>、&、U+2028/2029、非 BMP），不做任意 NFC 文本转换。输出 MUST 无 BOM、空白或尾 LF；true/false/null 为小写。输入 JSON 可有合法无意义空白与等价字符串 escape；digest 始终对 J(parsed value)，不是文件原始排版。H(b)=`sha256:`+lowerhex(SHA-256(b))。

## 10. Content commitment / 内容承诺

`PKG-CONTRACT-010`: ContentID MUST 是 H(whole file raw bytes)，包括零长度 bytes，不解码文本、不改换行、不拼入 path。content commitment 输入 C 为 manifest 中 distinct (content_id,size) 对象的数组，按 content_id 升序，每个对象恰有 `content_id`、`size`；重复引用只出现一次；空 manifest 为 `[]`。content_commitment MUST = H(ASCII `orbifabric.package.content-set.v1` + LF + J(C))。这是明确的 content set commitment，不使用 V1 Merkle leaf 或 hex pair 规则；Core 不要求独立 Merkle 文件。object filename 必须是完整 digest；验证内容和 size，不相信文件名。

## 11. VersionSubjectV2 / VersionSubjectV2

`PKG-CONTRACT-011`: version-subject.v2.schema.json MUST 逐字段按如下方式生成：schema/domain 为 schema 常量；package_id/package_version_id/parent_version_id/ordinal/created_at/protocol/protocol_version/tree_profile/profiles/required_capabilities/optional_capabilities 直接来自已验证 version.json；package_digest=H(J(package.json))；version_digest=H(J(完整 version.json))；manifest_digest=H(J(完整 manifest.json))；content_commitment 按上一条；sealed_metadata_digest=H(J(version.sealed_metadata))。subject digest MUST 为 H(ASCII `orbifabric.package.version-subject.v2` + LF + J(subject))。root parent 是 null，绝不是省略或数组。subject MUST NOT 包含 container bytes/hash、当前 mutable metadata、后续 evidence/signature、local path、credentials、DB ID、online status。完整 version_digest 包括 label 与未知 optional 字段，避免未签名 authority。

## 12. Signature envelope / 签名封装

`PKG-CONTRACT-012`: version-signature.v2.schema.json 定义完整 envelope E。Verifier MUST 从 manifest/version 重算 subject digest，交叉 package/version/signature ID 与路径，fingerprint=H(raw 32-byte public key)，public_key/signature 使用无 padding 的 canonical base64url，分别 decode 32/64 bytes 且 re-encode 相等。签名输入 MUST 是 ASCII `orbifabric.package.version-signature.v2` + LF + J(E 删除 signature 字段)。使用 RFC8032 Ed25519（非 Ed25519ph），签 envelope 中的 subject_digest 及 signer/signed_at/key/official facts，避免可替换署名时间或类型。MUST 拒绝非 canonical point/scalar、small-order public key/R 与错误 signature；有效验签不等于身份可信。local_device 不含 official；orbifabric_official 必需 official，信任由 Host 根据 environment/profile/key pin 判定；不信任 embedded 自称。Core/Complete 可无签名；Packtell 默认正式导出遵循 PKG-SIGN-030/031，正式 Delivery 必须至少一个有效引用签名。选择 signer 后 MUST NOT 静默 fallback，也不要求 local+official 双签。新增签名不改变 Version。

## 13. Notes and tags / Notes 与 tags

`PKG-CONTRACT-013`: notes.v1 的 revisions MUST 按 (note_id,revision) 排序；每个 note_id 使用 UUIDv7，revision 从1连续增加，target 在该 note 的各 revision 中不变。当前 projection 为最大 revision，deleted=true 表示 tombstone 且 body 必须空字符串；下一 revision 可显式恢复。tags.v1 的 revisions MUST 为全局连续 1..n；tag 是非空 NFC 文本、区分大小写、无首尾空白；从空 set 按顺序 add/remove 得到当前 projection，重复 add 或移除不存在 tag 为 INVALID_METADATA。metadata/package.json 是当前可变显示事实，不是 sealed metadata。所有 portable document 的 package_id MUST 一致；note target 引用历史中存在的对象（event target 要有对应 event）。manifest 恢复不依赖 note/event replay。

## 14. Events and provenance / Events 与 provenance

`PKG-CONTRACT-014`: events.ndjson MUST 为零 bytes 或每行一个 event.v1 JSON 加 LF，不允许空行/CR/BOM；文件行序就是 portable 记录序，不按 occurred_at 重排。event_id 唯一，schema_version=1；未知 optional namespaced type/data 保留为不解释的事实；需要解释才能保持正确性的事件必须声明 required capability。已知 type 是 vocabulary 中的观察标签，data 是可选业务说明的 JSON object，不是 state transition 程序；版本/notes/tags state 仍由对应文档决定。actor 可 null；字符串 id 是隐私安全 opaque identity，非 credential。provenance.records MUST 按 provenance_id 排序且唯一、append-only；target 为 package/file/content；source_kind 来自 vocabulary；source_id/source_revision 是可省略的非秘密 opaque 事实，不是可 fetch URL。relationship 绑定另一个 Package，可附其 Version；reuse/copy/derived_from/supersedes 不创建本 Package branch。所有 portable facts MUST NOT 保存 OAuth/refresh token、private key、credential/keyring ref、signed URL、绝对本地路径、SQLite ID、cache/index/embedding/worker state。schema 验证不等于内容脱敏；Host 导出必须选择安全事实。

## 15. Delivery and evidence / Delivery 与 evidence

`PKG-CONTRACT-015`: delivery.v1 MUST 交叉 package/version/subject_digest，signature_ids 引用该 Version 的现存 signature 且至少一条有效；坏的引用不因另一条有效而忽略。DeliveryID/created facts 不可静默改写；新 Delivery 用新 ID，同 Version 可多次 Delivery。evidence_refs 是 append-only 可选 evidence 清单；embedded=true 的文件必须存在，false 不要求联网；后续 append 不改变旧 subject。delivery_digest 定义为 H(J(delivery 删除 evidence_refs))，这样后续 evidence_refs append 不改变 receipt 绑定的 Delivery facts。evidence-envelope.v1 MUST 按 kind 选择同名 `*-subject.v1`，cross-check package/version/subject digest；receipt 还核对 delivery_id/delivery_digest，lifecycle witness 核对 event_id/event_digest=H(J(event))。envelope subject_digest=H(ASCII subject.schema + LF + J(subject))；signature 输入为 ASCII `orbifabric.package.evidence-envelope.v1` + LF + J(envelope 删除 signature)。key/Ed25519 校验同签名条款，各 kind 是不同 subject schema/key purpose；Host trust store MUST 将 key purpose 绑定 kind，不接受 Version signer 自动充当 evidence issuer。online revocation/status 不写入 historical subject；embedded snapshot 不代表当前状态。Evidence 的失败独立于 committed content integrity。

## 16. Portable filesystem / 可移植文件系统

`PKG-CONTRACT-016`: 所有路径 component MUST 按 Unicode 16.0.0 NFC 与 Default Full Case Folding（CaseFolding.txt 的 C/F，不用 T）处理；collision key=NFC(casefold(NFC(name)))。authority 输入 name 必须已 NFC，非 NFC 为 INVALID_PATH；物化候选先计算 NFC collisions（UNICODE_NORMALIZATION_CONFLICT），再 case-fold collisions（CASE_CONFLICT），再拒绝单个非法名字。路径 MUST 使用相对 `/`，拒绝 absolute、drive/UNC、反斜杠、空 component、`.`/`..`、NUL、C0/DEL、`<>:"|?*`、末尾点或空格、超过255 UTF-16 code units 的 component。Windows reserved basename（第一个点前，去末尾空格，不区分大小写）CON/PRN/AUX/NUL/CONIN$/CONOUT$/COM1..9/LPT1..9（含¹²³变体）拒绝。Root 自身的 display name 不参与 logical identity。portable tree MUST 只用 regular file/directory，拒绝 symlink/junction/special file；hardlink 不得成为恢复依赖，export 必须写独立 bytes。Writer 在发布前 preflight 全树含 control/extension；不能静默改名解决碰撞。

## 17. Directory and ZIP codecs / Directory 与 ZIP

`PKG-CONTRACT-017`: Directory export MUST 在目标外 staging，验证完整计划/objects/历史后以 no-overwrite commit 发布；中断或非 atomic 平台必须由 Host 隔离 pending output、恢复或报未完成，不能宣称成功。commit Version MUST 保护 expected HEAD、稳定读取 payload、写完整 Version/object 后最后发布 HEAD；事务中间状态不能当已完成 Package 交给读者。Host 锁/journal 放在 portable tree 外。ZIP v1 writer MUST 写单一顶层 display directory；reader 接受这一形式，也接受没有 wrapper 且根部直接有 `.packtell/format.json` 的形式（对应 PKG-CODEC-020 的 SHOULD 例外）；多候选 root/额外顶层 siblings 拒绝。UTF-8 ZIP names（非 ASCII 要 UTF-8 flag），STORE/DEFLATE 和 Zip64 MUST 支持；encryption、multi-volume、其它方法返回 unsupported/unsafe；不信 extra Unicode name override，路径仅按 UTF-8 entry name。MUST 在任何写出前检查全部 central entries/隐式父目录的 duplicate、file/dir、NFC/case collision、traversal 和 mode；local/central name/method/flags/size 不一致拒绝（data descriptor 的合法延迟 size 除外）；CRC、实际展开 size 必须验证。显式空目录必须保存；entry 顺序、压缩级别、mtime、permissions 不改变 logical subject。ZIP artifact digest 与 Version digest 分开。

## 18. Completeness proof and results / 完整性证明与结果

`PKG-CONTRACT-018`: Verifier MUST 分开输出 recognition、structure、working_state、committed_integrity、history_completeness、signature、identity、evidence、online。FULL 的算法：识别/结构/schema/path/capability 合法；HEAD 唯一线性链覆盖全部 Version；每份 manifest/tree/reference 合法；枚举全部 distinct ContentID，逐一从对象路径离线读取、核 SHA-256/size（也检查额外 object 的名称/hash）；Complete 必需 portable files 存在且 revision/reference 有效；声明 embedded 的 evidence 存在。全部满足才 FULL，profile label 不够。缺失/不可读 content object 或 Complete 必需 memory 文件为 NOT_FULL；missing parent/non-linear topology、schema/path/hash mismatch/非法 memory 为 INVALID。bad signature 独立 signature=INVALID，不把完整且正确 bytes 改为 NOT_FULL；错误 evidence 同样独立报告，但缺声明 embedded 文件为 NOT_FULL。无签名=ABSENT，不是无历史。未执行维度为 NOT_CHECKED，禁止写 PASS。UNBORN 空历史可 FULL。MUST NOT 从 Working Tree bytes 代替缺失 HEAD object，或联网补齐后冒称原输入 FULL。离线证明只涵盖所提供 Package 的 committed chain，不能证明从未存在被恶意整体回滚/移除的外部历史；freshness 属 Host/evidence。

## 19. Capabilities and resource limits / 能力与资源限制

`PKG-CONTRACT-019`: vocabularies/core.v2.json MUST 是初始词汇表，profiles/complete.v1.json 是 Complete machine contract。Core 必须理解 linear-history/content-sha256；portable-memory capability 要理解 notes/tags/provenance/events；version-signature 与 delivery-evidence 独立。声明 required capability 表示该 reader 必须理解其语义，不代表每个可选文件都必须存在。export/import MUST 保留未知 optional extension bytes 和允许的 optional JSON fields；无法保留必须拒绝有损写出或取得用户明确删除意图。Parser MUST 在分配/展开前执行 entry count、single/total bytes、JSON depth/size、NDJSON line、compression ratio 限制；具体数值是 Host policy，触发报 RESOURCE_LIMIT 而非协议损坏，conformance runner 要说明 policy。SDK 不获取 Provider credential，不自动联网，Resolver 的 bytes 在输出 commit 前重新 hash。

## 20. Shared field and result rules / 公共字段与结果规则

`PKG-CONTRACT-020`: 所有 Schema 中 UUID 字段 MUST 使用小写 RFC 9562 UUIDv7（版本位7，variant 8/9/a/b），不得从 ordinal/path/content 导出；生成时防止本 Package 已用 ID 冲突，不以时间戳排序取代 parent authority。时间 MUST 使用 Gregorian 年0001..9999、合法日期、UTC `YYYY-MM-DDTHH:mm:ss.ffffffZ`，秒00..59，不接受 leap second、offset 或可变精度。ordinal 达到最大值时停止提交，不能 wrap。format 与 version MUST 声明 required linear-history/content-sha256；Complete 另需 portable-memory。capability 名均使用词汇表完整 namespace。出现 signature/evidence 时，其对应 capability 必须在 required 或 optional 声明中；不支持 optional 语义的 reader 保留 bytes 并报告 NOT_CHECKED，不能宣称已验签。provenance target 必须在本 Package 历史中存在；event subject 可指向随后删除的历史实体，但不可指向不存在的实体；package target 必须等于当前 PackageID。所有 control 路径中的 ID 必须等于文件中的相应 ID。evidence_refs 按追加顺序、evidence_id 唯一；signature_ids 按 UUID 排序。已存在的 receipt/evidence subject 不可修改。evidence kind 与 subject schema MUST 按同名连字符替代下划线映射；全部四类使用 evidence-envelope.v1，不引入 Cloud API schema。

`PKG-CONTRACT-021`: vocabulary 中结果值 MUST 按维度使用。committed_integrity=VALID 表示所有 committed manifest 引用对象均 hash/size 通过；缺对象为 UNAVAILABLE，错误 bytes 为 INVALID；未执行为 NOT_CHECKED。结构结果不把 object 缺失视为无效目录拓扑。signature/evidence 汇总：没有对象为 ABSENT；全部有效为 VALID；任何无效为 INVALID；未执行为 NOT_CHECKED；单项结果应保留，不能掩盖失败。数学上有效但无信任 pin 的签名为 identity=UNTRUSTED，无 signer 为 UNKNOWN；只有 Host 已授权的匹配信任规则才为 TRUSTED。在线默认 NOT_REQUESTED。输入同时出现多错误时，MUST 先阻断不安全路径/不支持能力，随后检查 schema/topology，再 content/signature/evidence；不得为了收集更多错误而不安全读取。reason_codes 是去重集合，测试至少包含 expected code。资源限制不得伪装语义 PASS。

`PKG-CONTRACT-022`: canonical string escape 的确切输出 bytes MUST 为：quote→hex `5c22`，backslash→`5c5c`，BS→`5c62`，TAB→`5c74`，LF→`5c6e`，FF→`5c66`，CR→`5c72`；其他C0用ASCII `\u00xx`（小写hex）。这些hex定义消除 prose排版转义歧义。Ed25519 verification MUST 解码 canonical curve points A、R，拒绝 small-order points（[8]P 为 identity），要求 0≤S<L，并验证未乘 cofactor 的 `[S]B = R + [k]A`，其中 k=SHA-512(R_bytes || A_bytes || message) mod L，参数按 RFC8032；不能使用只检查 cofactor 等式而接受更多输入的宽松 verifier。

## References / 引用

- [Schema index](../../schemas/README.md)
- [Conformance contract](../../conformance/README.md)
- [Complete profile](../../profiles/complete.v1.json)
- [Ed25519 / RFC 8032](https://www.rfc-editor.org/rfc/rfc8032.html)
- [Unicode 16.0.0 case folding](https://www.unicode.org/Public/16.0.0/ucd/CaseFolding.txt)
- [Unicode 16 normalization](https://www.unicode.org/versions/Unicode16.0.0/)
