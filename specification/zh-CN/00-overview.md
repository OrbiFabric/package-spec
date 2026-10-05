# OrbiFabric Package Protocol 2.0：概览与术语

状态：Draft / Normative  
语言：中文主规范  
协议：`orbifabric.package` / `2.0`

## 1. 范围

Package 2.0 定义一种可移植、可验证、可长期演进的数字材料对象。Package 可以脱离 Packtell、OrbiFabric Cloud、特定数据库和特定编程语言独立存在。

`PKG-CORE-001`：Package MUST 拥有稳定 `package_id`，并且该身份 MUST NOT 由文件路径、容器文件名、ZIP 字节摘要、Cloud 记录或当前设备决定。

`PKG-CORE-002`：Package Root MUST 同时承载普通用户文件/文件夹组成的 Working Tree 与根级保留控制目录 `.packtell/`。

`PKG-CORE-003`：Directory 是 Package Tree 的基础物化。ZIP、TAR 及未来容器 MUST 仅编码同一 Package Tree，MUST NOT 引入新的 Package 业务语义。

`PKG-CORE-004`：Package MUST NOT 以 Packtell、Wails、SQLite、OrbiFabric Cloud、Google Drive、OneDrive、Dropbox 或任何单一 Host 为成立条件。

## 2. 核心对象

- **Package**：长期存在、可持续演进的数字材料对象。
- **Working Tree**：Package Root 中除根级 `.packtell/` 外的当前用户可见文件树。
- **HEAD**：最近一个 committed PackageVersion 的引用；首次提交前为 unborn。
- **PackageVersion**：某个历史点的不可变逻辑状态。
- **File / Folder Identity**：逻辑条目的稳定身份。
- **ContentID**：文件 bytes 的内容身份，2.0 Core 使用 SHA-256。
- **Portable History**：Versions、domain events、portable metadata revisions 与 provenance 的可交换历史。
- **Evidence**：关于 Package/Version/lifecycle 的外部或签名证明。
- **Container Codec**：Directory、ZIP、TAR 等对 Package Tree 的物化/编码方式。

`PKG-CORE-005`：File Identity、Content Identity 与 Materialized Path MUST 永久分离。

`PKG-CORE-006`：PackageVersion MUST 是逻辑状态，MUST NOT 以某个 physical representation 是否存在作为成立条件。

`PKG-CORE-007`：Delivery、Receive、Archive、Witness、Receipt、Cloud 状态与搜索索引 MUST NOT 定义 Package identity。

## 3. Profile

Package 2.0 使用“小 Core + Profile”模型。

`PKG-CORE-010`：Core Reader/Writer MAY 只实现最低 Package 语义，不要求实现 Packtell 全部产品能力。

`PKG-CORE-011`：`orbifabric.package.profile.complete.v1` 定义自包含完整历史 Profile；Packtell 正式 Package 导出默认 MUST 生成该 Profile，除非用户明确选择其他 Profile。

`PKG-CORE-012`：Complete Profile MUST 在没有原设备、Cloud、第三方云盘或原 Packtell 数据库的情况下恢复所有 committed Versions 及其 portable history。

## 4. 1.x 政策

`PKG-CORE-020`：Package 1.x 是未公开发布的开发期协议，不属于 2.0 兼容集合。

`PKG-CORE-021`：2.0 implementation MUST NOT 因 1.x 保留 production reader、writer、migration、fallback 或旧数据兼容义务。

## 5. 非目标

Package 2.0 Core 不定义：Packtell UI、Space/Family/Organization 权限、Cloud 计费、OAuth、Provider API、搜索索引、AI/MCP、协作聊天、任务管理或通用文件管理器行为。这些系统可以消费 Package Protocol，但不能改变 Core 语义。

[实施精确合同](10-implementation-contracts.md)将本章概念冻结为字段、字节和关系约束。
