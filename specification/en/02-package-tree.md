# Package Tree v1

Status: Draft / Normative  
Tree Profile: `orbifabric.package-tree.v1`

## 1. Directory layout

A Package Root MUST appear to ordinary users as a normal folder: user files and folders live directly at the root, while machine control data lives in the root `.packtell/` directory.

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

`PKG-TREE-001`: Root `.packtell` MUST be the only reserved namespace with Package control semantics.

`PKG-TREE-002`: User payload MUST NOT be forced into an additional wrapper directory such as `files/` or `data/`.

`PKG-TREE-003`: A same-named `.packtell` under a child directory MAY be treated as ordinary user content and MUST NOT alter the outer Package control authority.

## 2. `format.json`

`PKG-TREE-010`: `.packtell/format.json` MUST be the primary discriminator for Package detection.

Recommended fields:

```json
{
  "schema": "orbifabric.package.format.v2",
  "protocol": "orbifabric.package",
  "protocol_version": "2.0",
  "tree_profile": "orbifabric.package-tree.v1",
  "profiles": ["orbifabric.package.profile.complete.v1"],
  "capabilities": []
}
```

`PKG-TREE-011`: A Reader MUST NOT claim support for an unknown major protocol merely because a directory is named `.packtell`.

`PKG-TREE-012`: An unknown required capability MUST fail closed; an unknown optional capability MAY degrade while being preserved.

## 3. Portable path rules

`PKG-TREE-020`: Portable Tree v1 allows only regular files and directories.

`PKG-TREE-021`: Portable Tree v1 MUST NOT represent business content with symlinks, junctions, device nodes, sockets, FIFOs, or other special files.

`PKG-TREE-022`: Portable paths MUST be relative, use `/` as the logical separator, and reject empty paths, absolute paths, drive/UNC paths, `.`, `..`, NUL, and control characters.

`PKG-TREE-023`: Portable export MUST detect Unicode-normalized collisions and case-fold collisions; a conflict MUST block portable Package creation or require user resolution.

`PKG-TREE-024`: Permission bits, ACLs, owners, Windows Hidden attributes, filesystem creation times, and local inode/file IDs MUST NOT participate in Package logical identity.

## 4. `.packtell` visibility

`PKG-TREE-030`: Host UI SHOULD hide `.packtell/` from ordinary user views, but visibility MUST NOT be a validity condition.

`PKG-TREE-031`: A Windows Host MAY set the Hidden attribute; whether an extraction tool preserves that attribute does not affect Package validity.
