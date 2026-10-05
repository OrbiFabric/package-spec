# Package Tree v1

状态：Draft / Normative  
Tree Profile：`orbifabric.package-tree.v1`

## 1. 目录布局

Package Root 对普通用户 MUST 看起来像普通文件夹：用户文件与文件夹直接位于 Root；机器控制数据位于根级 `.packtell/`。

```text
My Package/
├── passport.pdf
├── Photos/
│   └── photo.jpg
└── .packtell/
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

`PKG-TREE-001`：根级 `.packtell` MUST 是唯一具有 Package control semantics 的保留 namespace。

`PKG-TREE-002`：用户 payload MUST NOT 被强制放入 `files/`、`data/` 等额外包装目录。

`PKG-TREE-003`：位于子目录中的同名 `.packtell` MAY 被当作普通用户目录；它 MUST NOT 改变外层 Package 的 control authority。

## 2. `format.json`

`PKG-TREE-010`：`.packtell/format.json` MUST 是 Package detection 的首要 discriminator。

建议字段：

```json
{
  "extensions": [],
  "optional_capabilities": [
    "orbifabric.package.capability.delivery-evidence.v1",
    "orbifabric.package.capability.version-signature.v1"
  ],
  "profiles": [
    "orbifabric.package.profile.complete.v1"
  ],
  "protocol": "orbifabric.package",
  "protocol_version": "2.0",
  "required_capabilities": [
    "orbifabric.package.capability.content-sha256.v1",
    "orbifabric.package.capability.linear-history.v1",
    "orbifabric.package.capability.portable-memory.v1"
  ],
  "schema": "orbifabric.package.format.v2",
  "tree_profile": "orbifabric.package-tree.v1"
}
```

`PKG-TREE-011`：Reader MUST NOT 仅因目录名为 `.packtell` 就宣称支持未知 major protocol。

`PKG-TREE-012`：未知 required capability MUST fail closed；未知 optional capability MAY 降级并保留。

## 3. Portable path rules

`PKG-TREE-020`：Portable Tree v1 只允许 regular file 与 directory。

`PKG-TREE-021`：Portable Tree v1 MUST NOT 使用 symlink、junction、device node、socket、FIFO 或其他 special file 表达业务内容。

`PKG-TREE-022`：Portable path MUST 为相对路径，使用 `/` 作为逻辑分隔符，并拒绝空路径、绝对路径、drive/UNC path、`.`、`..`、NUL 与控制字符。

`PKG-TREE-023`：Portable export MUST 检测 Unicode-normalized collision 与 case-fold collision；发现冲突时 MUST 在生成可移植 Package 前阻断或要求用户解决。

`PKG-TREE-024`：权限位、ACL、owner、Windows Hidden attribute、filesystem creation time 与本地 inode/file-id MUST NOT 参与 Package logical identity。

## 4. `.packtell` 可见性

`PKG-TREE-030`：Host UI SHOULD 在普通用户视图中隐藏 `.packtell/`，但“是否可见” MUST NOT 成为协议正确性条件。

`PKG-TREE-031`：Windows Host MAY 设置 Hidden attribute；解压工具是否保留该 attribute 不影响 Package validity。

[实施精确合同](10-implementation-contracts.md)将本章概念冻结为字段、字节和关系约束。
