# Working Tree, HEAD, and Version History

Status: Draft / Normative

## 1. Working Tree

`PKG-VERSION-001`: The tree under the Package Root, excluding the root `.packtell/`, MUST define the current Working Tree.

`PKG-VERSION-002`: The Working Tree MAY be modified directly by software other than Packtell; such modification MUST NOT cause the Package to lose identity.

`PKG-VERSION-003`: A Reader MUST report Package recognition separately from Working Tree state.

Recommended states are `UNBORN`, `CLEAN`, `DIRTY`, and `UNREADABLE`.

## 2. HEAD

`PKG-VERSION-010`: `.packtell/HEAD` MUST reference the latest committed PackageVersion, using the canonical unborn representation before the first commit.

`PKG-VERSION-011`: HEAD MUST NOT move automatically because of ordinary Working Tree changes.

`PKG-VERSION-012`: When the Working Tree differs from the HEAD logical state, the Package MUST be Dirty rather than Invalid.

## 3. Version authority

Each Version contains at least:

```text
versions/<package-version-id>/
├── version.json
└── manifest.json
```

`PKG-VERSION-020`: `manifest.json` MUST be the authority for the complete logical file/folder state of the Version; events MUST NOT be the sole source required to reconstruct the Version.

`PKG-VERSION-021`: The Version manifest MUST record stable FileID/FolderID, parent relationship, name, and kind; file entries MUST also record ContentID and size.

`PKG-VERSION-022`: A Version MAY have an ordinal and label, but `package_version_id` is the portable identity.

`PKG-VERSION-023`: Version lineage MUST be expressed using previous/parent VersionIDs and MUST NOT be inferred from filename ordering.

## 4. Dirty export

`PKG-VERSION-030`: A Dirty Package MAY be exported as a Package repository; the export MUST clearly distinguish committed history from the uncommitted Working Tree.

`PKG-VERSION-031`: A Dirty Working Tree MUST NOT impersonate the signed logical state of HEAD.

`PKG-VERSION-032`: An operation requiring formal Delivery, Version Seal, or committed verification of the current state MUST first create a new PackageVersion.

## 5. External modification detection

`PKG-VERSION-040`: Diff MUST at minimum report Added, Removed, Moved/Renamed, and Content Changed.

`PKG-VERSION-041`: Path changes and Content changes MUST be distinct; a rename of the same FileID MUST NOT be represented as delete plus new file unless valid identity continuity cannot be established.
