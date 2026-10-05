# Content Objects and the Complete Profile

Status: Draft / Normative  
Profile: `orbifabric.package.profile.complete.v1`

## 1. Content Object Store

Bytes referenced by committed Versions are deduplicated by ContentID in the portable object store:

```text
.packtell/objects/sha256/<prefix>/<digest>
```

`PKG-CONTENT-001`: Object paths MUST be determined by ContentID; SHA-256 of object bytes MUST match the ContentID.

`PKG-CONTENT-002`: When one ContentID is referenced by multiple FileVersions/PackageVersions, a Complete Profile SHOULD store only one copy of the object bytes.

`PKG-CONTENT-003`: A Complete Profile MUST store every content object required to reconstruct **all committed Versions**, including content currently visible in the Working Tree for HEAD.

> Rationale: even when HEAD bytes are currently present in the Working Tree, a committed copy must remain in the object store; otherwise an external overwrite of the Working Tree would destroy offline reconstruction of the historical Version.

## 2. Working Tree and Object Store

`PKG-CONTENT-010`: The Working Tree is the user work copy; the object store is the portable backing store for committed content authority. The same bytes MAY physically appear in both.

`PKG-CONTENT-011`: An implementation MAY use reflinks, copy-on-write, or other transparent local optimizations, but portable semantics MUST be equivalent to independently readable object bytes; historical reconstruction MUST NOT depend on symlinks or hardlinks.

## 3. Complete Profile

`PKG-CONTENT-020`: A Complete Profile MUST self-contain all committed Version manifests, all required content objects, current portable metadata, portable history, provenance, required verification material, and evidence declared as embedded.

`PKG-CONTENT-021`: Complete Profile validation MUST verify that every ContentID in every committed Version can be materialized from the Package itself without network access.

`PKG-CONTENT-022`: If any committed content object is missing, hash-mismatched, or unreadable, the Package MUST NOT claim `history_completeness=FULL`.

## 4. Export from third-party storage

The protocol is provider-neutral; Hosts supply bytes through a Content Resolver.

`PKG-CONTENT-030`: An Exporter MUST request content by ContentID and MUST NOT require Package Core to understand Google Drive, OneDrive, Dropbox, S3, or NAS APIs.

`PKG-CONTENT-031`: Remote bytes MAY stream directly into export staging and need not be permanently stored in Packtell managed local storage first.

`PKG-CONTENT-032`: Formal materialization MUST recompute SHA-256 over incoming bytes and compare it with the expected ContentID; mismatch MUST fail closed.

`PKG-CONTENT-033`: If the source exposes a revision/version token, the Host SHOULD verify the same remote revision before and after reading so bytes from different revisions cannot be combined into one ContentObject.

`PKG-CONTENT-034`: A single export operation SHOULD deduplicate remote reads by ContentID.

## 5. Provenance and self-containment

`PKG-CONTENT-040`: A Complete Profile MAY record original Provider, object ID, revision, and first-observed facts as provenance, but these fields MUST NOT be runtime dependencies for opening or reconstructing the Package.

`PKG-CONTENT-041`: Credential-bearing URLs, OAuth tokens, refresh tokens, signed URLs, and secrets MUST NOT enter the Package.
