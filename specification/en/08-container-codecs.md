# Container Codecs

Status: Draft / Normative

## 1. Principle

`PKG-CODEC-001`: A Container Codec MUST be an encoding layer for the Package Tree and MUST NOT own independent Package identity.

`PKG-CODEC-002`: Encoding the same Package Tree as Directory, ZIP, or TAR MUST preserve PackageID, PackageVersionID, Version Subject, and portable history.

`PKG-CODEC-003`: A container artifact SHA-256 MAY differ because of encoding, compression level, entry ordering, or metadata; an artifact digest MUST NOT impersonate a logical Version digest.

## 2. Directory Codec

`PKG-CODEC-010`: Directory materialization is the foundational reference semantics: user files live at the root and `.packtell/` lives in the same Package Root.

`PKG-CODEC-011`: Directory export MUST use staging + validation + commit semantics so interruption does not leave a partial object that appears complete.

## 3. ZIP Codec v1

ZIP v1 conceptually means "compress one Package Folder".

```text
My Package.zip
└── My Package/
    ├── user files...
    └── .packtell/
```

`PKG-CODEC-020`: ZIP v1 SHOULD contain one top-level Package directory; that directory name is a display/materialization fact, not Package identity.

`PKG-CODEC-021`: Extracting ZIP v1 MUST produce a Package Tree equivalent to Directory Codec materialization.

`PKG-CODEC-022`: A ZIP Reader MUST reject traversal, absolute paths, duplicate normalized paths, case/Unicode collisions, symlink/special entries, unsupported encryption, and unsafe structures.

`PKG-CODEC-023`: A ZIP writer MAY use STORE/DEFLATE/Zip64; compression method MUST NOT alter the logical digest.

## 4. TAR/RAR/future containers

`PKG-CODEC-030`: TAR, RAR, or a future Packtell-native container MUST have its own profile, safe parsing rules, and conformance fixtures before becoming a supported codec.

`PKG-CODEC-031`: Core 2.0 MUST NOT change the Package Tree or Version identity solely to satisfy a future codec.

## 5. Direct streaming implementation

`PKG-CODEC-040`: An implementation MAY stream the same Package Tree plan directly into ZIP/TAR without first materializing a temporary directory, provided the logical result is equivalent to Directory Codec semantics.

[Exact implementation contracts](10-implementation-contracts.md) freeze this chapter’s concepts into field, byte and relational constraints.
