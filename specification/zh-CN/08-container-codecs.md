# Container Codecs

状态：Draft / Normative

## 1. 原则

`PKG-CODEC-001`：Container Codec MUST 是 Package Tree 的编码层，MUST NOT 拥有独立 Package identity。

`PKG-CODEC-002`：将同一个 Package Tree 编码成 Directory、ZIP 或 TAR MUST 保持 PackageID、PackageVersionID、Version Subject 与 portable history 不变。

`PKG-CODEC-003`：Container artifact SHA-256 MAY 因编码、压缩级别、entry 顺序或 metadata 不同而变化；artifact digest MUST NOT 冒充 logical Version digest。

## 2. Directory Codec

`PKG-CODEC-010`：Directory materialization 是基础参考语义：用户文件位于根，`.packtell/` 位于同一 Package Root。

`PKG-CODEC-011`：Directory export MUST 使用 staging + validation + commit 语义，避免中断后留下看似完整的半成品 Package。

## 3. ZIP Codec v1

ZIP v1 的概念行为是“压缩一个 Package Folder”。

```text
My Package.zip
└── My Package/
    ├── user files...
    └── .packtell/
```

`PKG-CODEC-020`：ZIP v1 SHOULD 包含单一顶层 Package directory；该目录名称是 display/materialization fact，不是 Package identity。

`PKG-CODEC-021`：解压 ZIP v1 后 MUST 得到与 Directory Codec 等价的 Package Tree。

`PKG-CODEC-022`：ZIP Reader MUST 拒绝 traversal、绝对路径、重复 normalized path、case/Unicode collision、symlink/special entry、未支持 encryption 与不安全结构。

`PKG-CODEC-023`：ZIP writer MAY 使用 STORE/DEFLATE/Zip64；具体压缩方法 MUST NOT 改变 logical digest。

## 4. TAR/RAR/未来容器

`PKG-CODEC-030`：TAR、RAR 或未来 Packtell-native container 在成为 supported codec 前 MUST 有独立 profile、安全解析规则与 conformance fixtures。

`PKG-CODEC-031`：Core 2.0 MUST NOT 因未来 codec 需求改变 Package Tree 或 Version identity。

## 5. Direct streaming implementation

`PKG-CODEC-040`：实现 MAY 直接把同一 Package Tree plan 流式写入 ZIP/TAR，而不先物化临时目录；只要逻辑结果与 Directory Codec 一致。

[实施精确合同](10-implementation-contracts.md)将本章概念冻结为字段、字节和关系约束。
