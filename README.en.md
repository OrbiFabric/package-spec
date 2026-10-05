# OrbiFabric Package Protocol 2.0

> **Official bilingual specification · Chinese is the primary normative natural-language text**  
> 中文：[README.md](README.md)

This repository defines **OrbiFabric Package Protocol 2.0**: a portable Package object that can exist independently of Packtell and can be read, written, verified, imported, exported, and reconstructed by independent implementations.

```text
My Package/
├── ordinary user files and folders        # Working Tree
└── .packtell/                              # portable package memory
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

## Core principles

- The Package Root behaves like a normal folder; user files live directly at the root.
- `.packtell/` is the only root control namespace and carries protocol identity, versions, full history, notes, tags, provenance, verification material, and extensions.
- External software may modify the Working Tree; differences from `HEAD` make it Dirty rather than invalidating Package identity.
- PackageVersion is immutable logical state; the Version manifest is the authority for historical state.
- File Identity, Content Identity, and Materialized Path remain distinct.
- Complete Profile self-contains content objects for every committed Version, including HEAD bytes also visible in the Working Tree, so external overwrite of current files does not destroy historical reconstruction.
- Third-party storage only affects how a ContentResolver obtains bytes during export; a completed Complete Package does not depend on Cloud/Provider access.
- Version Signature binds a Canonical Version Subject, not ZIP bytes.
- Packtell uses a local Ed25519 package signer when no Cloud official signer is available; when a connected OrbiFabric official signer is selected, the Cloud/official signer signs the same subject. Cloud Anchor, Delivery Receipt, and Lifecycle Witness remain distinct evidence objects.
- Directory is the foundational materialization; ZIP/TAR/RAR/future native containers are codecs for the same Package Tree.
- Packtell is a reference consumer product, not a prerequisite for the protocol.

## Status

- Status: **Draft / Pre-release**
- Target protocol: **`orbifabric.package` / `2.0`**
- Tree profile: **`orbifabric.package-tree.v1`**
- Default Packtell export profile: **`orbifabric.package.profile.complete.v1`**
- Package 1.x: **unreleased development protocol; no compatibility, migration, old-data retention, or production legacy runtime.**

## Specification index

| # | Chinese primary | English |
|---|---|---|
| 00 | [概览与术语](specification/zh-CN/00-overview.md) | [Overview](specification/en/00-overview.md) |
| 01 | [Core Model](specification/zh-CN/01-core-model.md) | [Core Model](specification/en/01-core-model.md) |
| 02 | [Package Tree](specification/zh-CN/02-package-tree.md) | [Package Tree](specification/en/02-package-tree.md) |
| 03 | [Working Tree / HEAD / Version](specification/zh-CN/03-working-tree-versions.md) | [Working Tree / HEAD / Version](specification/en/03-working-tree-versions.md) |
| 04 | [Content / Complete Profile](specification/zh-CN/04-content-complete-profile.md) | [Content / Complete Profile](specification/en/04-content-complete-profile.md) |
| 05 | [Metadata / History / Provenance](specification/zh-CN/05-portable-metadata-history-provenance.md) | [Metadata / History / Provenance](specification/en/05-portable-metadata-history-provenance.md) |
| 06 | [Verification / Signing](specification/zh-CN/06-verification-signing.md) | [Verification / Signing](specification/en/06-verification-signing.md) |
| 07 | [Delivery / Evidence](specification/zh-CN/07-delivery-evidence.md) | [Delivery / Evidence](specification/en/07-delivery-evidence.md) |
| 08 | [Container Codecs](specification/zh-CN/08-container-codecs.md) | [Container Codecs](specification/en/08-container-codecs.md) |
| 09 | [Conformance / Security](specification/zh-CN/09-conformance-security.md) | [Conformance / Security](specification/en/09-conformance-security.md) |
| 10 | [实施合同](specification/zh-CN/10-implementation-contracts.md) | [Implementation contracts](specification/en/10-implementation-contracts.md) |

Authority and governance: [SPEC-AUTHORITY.en.md](SPEC-AUTHORITY.en.md) · [中文](SPEC-AUTHORITY.md)  
1.x clean break: [MIGRATION-1X-CLEAN-BREAK.en.md](MIGRATION-1X-CLEAN-BREAK.en.md) · [中文](MIGRATION-1X-CLEAN-BREAK.md)

## Machine-readable assets

- [`schemas/`](schemas/) — JSON Schemas
- [`vocabularies/`](vocabularies/) — stable enums/vocabularies
- [`profiles/`](profiles/) — Complete and future profiles
- [`fixtures/`](fixtures/) — valid/invalid Package trees
- [`vectors/`](vectors/) — canonicalization/hash/signature golden vectors
- [`conformance/`](conformance/) — cross-language expected results

Implementation fields and shared assets are frozen in chapter 10. Run `python3 conformance/check.py` for repository consistency; this does not certify SDK conformance.

## Reference implementation

Official Go Reference SDK: [github.com/orbifabric/package-go](https://github.com/OrbiFabric/package-go)

Authority order is specification → schema → canonical/crypto algorithms → vectors → official English translation → `package-go`. A Go behavior that conflicts with the specification is an implementation bug.

## License

This repository is licensed under the **Apache License 2.0**.

Unless otherwise noted, the specifications, schemas, test vectors, fixtures, examples, and all other repository contents are licensed under Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

## Local consistency / 本地一致性

Python 3.11+ with `jsonschema` 4.18+ and `cryptography` 41+: `python3 conformance/check.py`. No SDK or network is used.
