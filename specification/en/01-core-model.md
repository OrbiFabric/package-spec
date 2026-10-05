# Package 2.0 Core Model

Status: Draft / Normative

## 1. Identifiers

`PKG-CORE-100`: `package_id`, `package_version_id`, `file_id`, `folder_id`, `event_id`, and `delivery_id` MUST use textual UUIDv7 values.

`PKG-CORE-101`: UUIDs MUST use lowercase hyphenated RFC 4122/9562-style text; implementations MUST NOT use database auto-increment IDs as portable identity.

`PKG-CORE-102`: `content_id` MUST be `sha256:<64 lowercase hex>`.

`PKG-CORE-103`: Identical bytes MUST produce the same ContentID; different FileIDs MAY reference the same ContentID.

## 2. File, Folder, Path, and Content

`PKG-CORE-110`: File/Folder logical identity MUST be independent of name and path.

`PKG-CORE-111`: Renaming or moving a File/Folder MUST preserve its ID.

`PKG-CORE-112`: Changing file content MUST preserve `file_id` and produce a new `content_id`.

`PKG-CORE-113`: Copying a file MUST create a new `file_id` but MAY reuse the same `content_id`.

`PKG-CORE-114`: Logical tree authority MUST be expressed by parent relationship plus name; materialized paths are derived and are not identity.

## 3. Package and Version

`PKG-CORE-120`: A Package is a mutable long-lived entity; a PackageVersion is an immutable logical snapshot.

`PKG-CORE-121`: The file set, FileIDs, FolderIDs, ContentIDs, version-level sealed metadata, and lineage of a committed Version MUST NOT be silently rewritten.

`PKG-CORE-122`: Any change to that Version authority MUST create a new PackageVersion.

`PKG-CORE-123`: Tags, Notes, later Delivery, Witness, Receipt, and other lifecycle/evidence MAY be appended without creating a new PackageVersion, but their portable history MUST be preserved.

## 4. Time and text

`PKG-CORE-130`: Protocol strings use UTF-8; machine path components MUST undergo Unicode NFC normalization before entering portable authority.

`PKG-CORE-131`: Canonical timestamps MUST use UTC RFC3339 in the form `YYYY-MM-DDThh:mm:ss.ffffffZ`.

`PKG-CORE-132`: Counts, sizes, and ordinals in protocol authority MUST use non-negative integers; exact identity facts MUST NOT rely on floating-point values.

## 5. `package.json`

`.packtell/package.json` stores stable Package identity and creation facts; it is not a Packtell database dump.

Minimum conceptual shape:

```json
{
  "created_at": "2026-10-05T00:00:00.000000Z",
  "package_id": "019a0000-0000-7000-8000-000000000001",
  "schema": "orbifabric.package.package.v2"
}
```

`PKG-CORE-140`: `package.json` MUST NOT contain OAuth tokens, credentials, OS Keyring references, absolute local paths, Cloud sessions, or internal database row IDs.

[Exact implementation contracts](10-implementation-contracts.md) freeze this chapter’s concepts into field, byte and relational constraints.
