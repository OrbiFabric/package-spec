# OrbiFabric Package Protocol 2.0: Overview and Terminology

Status: Draft / Normative  
Language: Official English translation  
Protocol: `orbifabric.package` / `2.0`

## 1. Scope

Package 2.0 defines a portable, verifiable, long-lived digital-material object. A Package can exist independently of Packtell, OrbiFabric Cloud, any database, and any programming language.

`PKG-CORE-001`: A Package MUST have a stable `package_id`; that identity MUST NOT be derived from a file path, container filename, ZIP-byte digest, Cloud record, or current device.

`PKG-CORE-002`: The Package Root MUST contain both the normal user-visible Working Tree and the reserved root control directory `.packtell/`.

`PKG-CORE-003`: A directory is the foundational Package Tree materialization. ZIP, TAR, and future containers MUST only encode the same Package Tree and MUST NOT introduce new Package business semantics.

`PKG-CORE-004`: A Package MUST NOT depend on Packtell, Wails, SQLite, OrbiFabric Cloud, Google Drive, OneDrive, Dropbox, or any single Host in order to exist.

## 2. Core objects

- **Package**: a long-lived digital-material object that can evolve over time.
- **Working Tree**: the current user-visible tree under the Package Root, excluding the root `.packtell/` directory.
- **HEAD**: reference to the latest committed PackageVersion; unborn before the first commit.
- **PackageVersion**: an immutable logical state at a historical point.
- **File / Folder Identity**: stable logical identity of a tree entry.
- **ContentID**: content identity of file bytes; Core 2.0 uses SHA-256.
- **Portable History**: exchangeable versions, domain events, portable metadata revisions, and provenance.
- **Evidence**: external or signed proof about Package, Version, or lifecycle facts.
- **Container Codec**: a materialization/encoding such as Directory, ZIP, or TAR.

`PKG-CORE-005`: File Identity, Content Identity, and Materialized Path MUST remain distinct.

`PKG-CORE-006`: PackageVersion MUST represent logical state and MUST NOT depend on a physical representation being present.

`PKG-CORE-007`: Delivery, Receive, Archive, Witness, Receipt, Cloud state, and search indexes MUST NOT define Package identity.

## 3. Profiles

Package 2.0 follows a small-Core-plus-Profile model.

`PKG-CORE-010`: A Core Reader/Writer MAY implement only minimum Package semantics and is not required to implement all Packtell product capabilities.

`PKG-CORE-011`: `orbifabric.package.profile.complete.v1` defines the self-contained full-history profile. A formal Packtell Package export MUST produce this profile by default unless the user explicitly selects another profile.

`PKG-CORE-012`: A Complete Profile MUST reconstruct every committed Version and its portable history without the original device, Cloud, third-party storage, or original Packtell database.

## 4. 1.x policy

`PKG-CORE-020`: Package 1.x is an unreleased development protocol and is not part of the 2.0 compatibility set.

`PKG-CORE-021`: A 2.0 implementation MUST NOT retain production readers, writers, migration paths, fallbacks, or old-data compatibility obligations solely for 1.x.

## 5. Non-goals

Package 2.0 Core does not define Packtell UI, Space/Family/Organization permissions, Cloud billing, OAuth, Provider APIs, search indexes, AI/MCP, collaboration chat, task management, or general file-manager behavior. Those systems may consume the protocol but cannot redefine Core semantics.

[Exact implementation contracts](10-implementation-contracts.md) freeze this chapter’s concepts into field, byte and relational constraints.
