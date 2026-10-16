# Package Protocol 2.1：可选存储与 Cloud 控制面

状态：Draft / Normative（仅对选择本扩展的存储服务实现适用）  
规范版本：**2.1**；现有 portable wire/format discriminator 保持 **`orbifabric.package` / `2.0`**。

本章在不改变 Package 2.0 Core、Complete Profile、版本身份、签名输入或离线可验证性的前提下，规定 Packtell / OrbiFabric Cloud 可以采用的**可选存储与恢复服务架构**。这里的 Cloud 指包含控制面和可选托管数据面的产品体系；**控制面本身不持久化或转发用户文件字节，并不意味着 Cloud 产品永远不能提供用户文件的托管备份**。已完成的 Complete Package 仍独立于任何网络或供应商。

## 1. 规范边界和分层

`PKG-STORAGE-001`：实现本章可选服务的 Host **MUST** 保证 Package 的存在、身份、Version、离线验证和 Complete Profile 语义不以 Cloud 账户、存储供应商或备份服务为前提。

`PKG-STORAGE-002`：本章 **MUST NOT** 改变既有 Package 2.0 文件结构、format/version/schema discriminator、ContentID、VersionSubject、签名规范、conformance fixtures 或 complete-history 离线合同；2.1 是兼容性规范增补，而不是现有文件的强制迁移。

`PKG-STORAGE-003`：使用 Cloud 协调式存储的部署 **MUST** 清楚区分：Control Plane（账户、授权、权益、元数据、位置路由、任务、策略、用量、审计）、Managed Data Plane（由 OrbiFabric 选择或更换的供应商保存加密静态对象）、Client-managed Data Plane（用户自己持有凭据的供应商）。用户文件实体可以存储在后两者，而不是要求全部永不进入 Cloud 管理的基础设施。

`PKG-STORAGE-004`：Cloud Control Plane **MUST NOT** 将用户文件或 Package 实体字节作为常规应用数据库记录、上传代理、下载代理或持久请求日志内容保存；本章的默认数据路径是客户端与实际存储供应商直接传输，控制面负责协调。

## 2. 身份、对象和多个位置

`PKG-STORAGE-010`：采用远程备份的 Host **MUST** 将逻辑 BackupObject / ContentID / File Revision / Package Version 关联与物理 StorageLocation 分离，供应商对象键、桶、账号、区域和传输 URL 不定义协议对象身份。

`PKG-STORAGE-011`：一个逻辑对象 **MAY** 同时有多个受管理的 StorageLocation，例如本机、用户 Dropbox 和若干 Cloud-managed 存储供应商；同一历史修订的身份不得因迁移或复制位置而重建。

`PKG-STORAGE-012`：StorageLocation 的服务元数据 **MUST** 记录足以进行经授权定位、环境/Space/账号隔离、对象内容摘要/长度校验与健康状态判断的非秘密事实，且不得假定一个 Package 只能归属一个存储位置。

`PKG-STORAGE-013`：备份目标选择 **SHOULD** 是可配置策略而非写死的单一 Provider；不同对象可以采用不同目标或冗余策略，但位置变化不改变 portable Package authority。

## 3. 文件来源不同于备份

`PKG-STORAGE-020`：Host **MUST** 区分第三方文件来源（例如 Google Drive、OneDrive、Dropbox 的原始引用）和明确授权的实体备份目标；引用来源本身不代表备份副本已创建。

`PKG-STORAGE-021`：Cloud 或备份 Worker **MUST NOT** 仅因为用户将远端文件加入 Package 就自动下载、复制或托管该来源文件实体；任何 hydration/backup 都必须符合明确业务动作、来源授权和对应版本校验。

`PKG-STORAGE-022`：导出正式 Complete Package 时，Host **MUST** 按现有 ContentResolver、完整性与自包含规则取得所有必要字节，不能把可联网的 StorageLocation 或临时下载 URL 冒充 Complete Profile 内嵌对象。

## 4. 首版 Packtell / Cloud 边界（V1）

`PKG-STORAGE-030`：Packtell 首个正式版本的个人实体备份 **MUST** 仅开放用户自有 Dropbox（BYO / CLIENT_MANAGED）作为已实现目标；Google Drive 和 OneDrive 保留文件来源功能，其他实体备份供应商及 OrbiFabric-managed storage 均属于未来能力而非本版交付声明。

`PKG-STORAGE-031`：V1 启用新的自动/手动备份写入 **MUST** 按已批准的产品权益合同取得有效 Cloud 授权；Cloud 失效或未登录时不能误报新备份成功。

`PKG-STORAGE-032`：V1 已存在的 Dropbox 备份 **MUST** 能在 Cloud 不可达、未登录、权益过期或账号停用时，凭同一用户 Dropbox 账号和独立 Backup Catalog 被发现、读取及恢复；不得把 Cloud API、Token、索引或续费设为读取已有 BYO 备份的前置条件。

`PKG-STORAGE-033`：V1 Dropbox 备份 **MUST** 重用既有 Provider OAuth 连接及其本地安全凭据存储，不为备份另建一次授权，不上传用户的 Dropbox OAuth/refresh token 到 Cloud。V1 使用已批准的 Full Dropbox App 下专用 `/Apps/Packtell` 目录，该目录不是 App Folder 权限沙箱。

## 5. 未来托管、多 Provider 与 BYO 扩展

`PKG-STORAGE-040`：未来可选 CLOUD_MANAGED 备份 **MAY** 将文件实体放在由 OrbiFabric 管理的一个或多个底层对象存储供应商（例如 S3 兼容服务），用户通过 Packtell/Cloud 统一入口管理备份，不必直接拥有供应商账号。

`PKG-STORAGE-041`：未来适配器 **SHOULD** 支持按策略配置、替换、迁移和并行使用多个供应商；“可切换供应商”表示能在完成必要数据复制/核验后安全切换，不承诺尚未迁移的字节瞬时可用。

`PKG-STORAGE-042`：未来 CLIENT_MANAGED 备份 **MAY** 在 Dropbox 之外扩展为用户自有 S3/S3-compatible、WebDAV 或其他适配器，保持用户凭据由客户端或独立用户授权边界掌握，不强制使用 Cloud-managed 存储。

`PKG-STORAGE-043`：Hybrid 模式 **MAY** 允许按 ContentID/修订同时保留 BYO 与 CLOUD_MANAGED 位置，并定义优先级、容量、限额及故障转移策略；不得将“混合”解释为默认上传所有来源文件。

`PKG-STORAGE-044`：未正式启用的 Provider **MUST NOT** 仅因数据模型或界面占位存在就被对外宣称为可用、可恢复或完成跨设备联调。

## 6. Cloud 协调与客户端直传

`PKG-STORAGE-050`：对 CLOUD_MANAGED 上传，Control Plane **MUST** 在核实用户、Space、设备、权限、权益、目标对象、大小/摘要、容量与供应商策略后，选择 StorageLocation 并签发/协调对象级、限时、限定操作的直传授权。

`PKG-STORAGE-051`：对 CLOUD_MANAGED 下载，Control Plane **MUST** 重新核实当前读取权限和位置状态，返回对应 Provider 的直接下载能力或受控位置选择结果；不得仅凭客户端提交的对象键、StorageLocation ID 或历史链接放行。

`PKG-STORAGE-052`：支持 presigned URL 的 Provider **SHOULD** 由控制面返回限定 HTTP 方法、单一对象/作用域、短有效期且只经 TLS 使用的授权 URL；授权到期、重试及分片传输应由独立服务合同处理。

`PKG-STORAGE-053`：不支持原生 presigned URL 的 Provider（包括某些 WebDAV 部署）**MUST** 使用经过明确安全审查的直接访问授权机制，或保持 CLIENT_MANAGED 由客户端自行持有 Provider 凭据；不能伪称每一种 Provider 都支持 S3 式签名 URL。

`PKG-STORAGE-054`：客户端 **MUST NOT** 把预签名 URL、临时令牌、主 Provider 凭据或其他短期传输授权写入 portable Package、Cloud Registry 元数据、永久 Catalog、Analytics 或持久日志。

`PKG-STORAGE-055`：上传/下载完成状态 **MUST** 区分授权已签发、传输已尝试、供应商已确认、端到端字节校验成功、Catalog/Location 已发布及客户端已恢复，不得将返回 URL 或 HTTP 成功直接视为已备份/恢复。

## 7. 完整性、安全与秘密

`PKG-STORAGE-060`：任何 Managed/BYO BackupObject 发布为可恢复之前 **MUST** 校验原始内容的 ContentID/SHA-256、期望长度和不可变对象绑定；仅依赖 ETag、对象键或供应商上传成功回执不够。

`PKG-STORAGE-061`：可恢复的历史对象 **MUST** 使用不可变或经过内容寻址防覆盖的存储语义；丢失响应、冲突和未知副作用应按原对象身份对账，避免生成虚假成功或覆盖其他修订。

`PKG-STORAGE-062`：Cloud-managed / BYO 传输 **MUST** 使用受保护链路，并明确存储端加密与密钥责任；V1 可采用 TLS、供应商 SSE 与 SHA-256，不把 E2EE 或 zero-knowledge 冒充首版功能。未来加入 E2EE 需单独设计密钥丢失、共享与恢复模型。

`PKG-STORAGE-063`：Cloud Control Plane **MUST NOT** 托管 CLIENT_MANAGED 用户 OAuth refresh token、WebDAV 密码、S3 master key，或把原始 Package Root/完整历史/文件实体混入只允许元数据的 Registry 接口。

`PKG-STORAGE-064`：对 managed direct transfer 的授权 **SHOULD** 采取最小权限、短 TTL、一次操作所需的最窄对象范围，并在供应商能力允许时约束请求摘要、长度、上传分段和回执。

## 8. 供应商切换、迁移和可靠性

`PKG-STORAGE-070`：Provider 变更 **MUST** 视为受控数据迁移/路由策略调整，而不是通过修改数据库 Provider 名称来假装对象已经转移。

`PKG-STORAGE-071`：切换某对象的优先下载位置之前，迁移流程 **MUST** 确认目标对象真实存在、完整 SHA-256/长度匹配、关联 Catalog/修订已闭合且可读取；失败时保留已有可用位置。

`PKG-STORAGE-072`：Provider 迁移 **SHOULD** 采用先复制与核验、再切换读取策略、最后按单独保留规则清理的方式；切换期间允许新旧位置并存，失败可退回已验证的旧位置。

`PKG-STORAGE-073`：用户停用备份、迁移失败、Cloud 权益过期或撤销连接 **MUST NOT** 自动删除已有 BYO 备份、历史对象或其独立 Catalog；显式删除、生命周期与保留政策需单独授权。

`PKG-STORAGE-074`：Provider 断供、签名 URL 过期、配额不足、账号变更、迁移部分完成、重复提交及异步未知结果 **MUST** 分别报告可重试、需要重新授权、损坏、部分可恢复或管理员介入状态，不得将失败掩盖为不存在的空 Package。

## 9. 恢复和跨设备能力

`PKG-STORAGE-080`：BYO 恢复路径 **MUST** 可以独立列举用户授权下的 Backup Catalog，核对对象及版本关系，并在没有 Cloud session/metadata 的新安装上恢复已有可访问内容。

`PKG-STORAGE-081`：未来 CLOUD_MANAGED 跨设备恢复 **MAY** 使用 Cloud 身份与元数据索引取得新设备的短期 Provider 下载授权；具体账号停用、订阅过期、退款、删除和保留期的读取权益必须在该功能上线前另行明确，不照搬 BYO 永久独立读取承诺。

`PKG-STORAGE-082`：恢复器 **MUST** 区分“文件来源引用仍需用户自行重新授权”“备份实体已经验证可恢复”“只具有 Cloud 元数据线索”这三种状态；不能由其中之一推定另两种成立。

`PKG-STORAGE-083`：正式 Complete Profile **MUST** 继续按 2.0 的离线合同自包含所有 committed Version 内容与历史；基于远端对象位置的在线备份不是新的 portable Complete Profile，也不取代其离线验证要求。

## 10. 兼容性与实施边界

`PKG-STORAGE-100`：本 2.1 规范增补 **MUST NOT** 强制改变现有 `.packtell/format.json` 的 `protocol_version="2.0"`、`schemas/*.v2`、`package-go` 字节合同、Version Subject、既有 fixture/vectors 或 2.0 Reader 支持；新的 wire 字段与迁移需另外审核并版本化。

`PKG-STORAGE-101`：Control Plane API、供应商 Adapter、授予/确认端点、配额、密钥、存储收费、迁移作业、位置数据模型和恢复授权 **SHOULD** 在独立的 Cloud/Packtell 服务合同中版本化；本章不捏造已经实现的 API/schema 或宣称现有客户端支持未来能力。

`PKG-STORAGE-102`：选择实现本扩展的产品 **MUST** 分别验证真实 Provider 授权、上传/下载、内容摘要、可恢复 Catalog、原生设备、Cloud 故障、供应商迁移及权限回收；原 2.0 portable conformance 通过不等于可选 Cloud 存储功能通过。

## 11. 分阶段产品范围（说明性）

| 能力 | Packtell V1 | 未来增量 |
|---|---|---|
| Package Core/Complete/Profile/签名 | 继续使用现有 2.0 portable 字节合同 | 兼容演进 |
| 第三方文件来源 | Google Drive、OneDrive、Dropbox | 可扩展来源，不自动备份引用 |
| 自带云盘实体备份 | **Dropbox only**，现有 OAuth，独立 Catalog | BYO S3、WebDAV 等 |
| OrbiFabric-managed 实体备份 | **不提供**，不得宣称已上线 | Cloud 协调多 Provider、客户端直传 |
| 位置策略 / Hybrid / 存储迁移 | 仅保留扩展能力，不提供托管切换操作 | 多位置、验证后切换、可控迁移 |
| 跨设备恢复 | 已有 Dropbox 独立恢复设计；具体平台按实际验收宣称 | Cloud-managed 授权直读、权限/保留政策 |
| Cloud 用户文件实体 | V1 仅元数据与见证（自有 Dropbox 实体不经 Cloud） | 托管实体位于可替换的 managed data plane，而非 Cloud 控制面数据库 |

参考：现有 [Core 及完整 Profile](04-content-complete-profile.md)、[签名](06-verification-signing.md)、[交付 Evidence](07-delivery-evidence.md)、[精确字节合同](10-implementation-contracts.md) 保持有效。
