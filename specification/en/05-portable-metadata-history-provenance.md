# Portable Metadata, History, and Provenance

Status: Draft / Normative

## 1. Portable metadata

`.packtell/metadata/` stores Package metadata meaningful across implementations, for example:

```text
metadata/
├── package.json
├── tags.json
├── notes.json
└── provenance.json
```

`PKG-META-001`: Portable metadata MUST express Package semantics and MUST NOT be a serialized mirror of Packtell SQLite/ORM structure.

`PKG-META-002`: Notes MUST use stable `note_id` values; updating a Note MUST NOT be represented as unrelated string deletion and recreation when identity continuity exists.

`PKG-META-003`: Tags SHOULD use normalized textual values. An implementation MAY provide stable tag IDs but MUST NOT require a Packtell database ID.

## 2. Portable domain history

`PKG-META-010`: `.packtell/history/events.ndjson` MAY store append-oriented portable domain events.

Recommended vocabulary includes:

`PACKAGE_CREATED`, `FILE_ADDED`, `FILE_REMOVED`, `FILE_MOVED`, `FILE_RENAMED`, `FILE_CONTENT_CHANGED`, `VERSION_CREATED`, `TAG_ADDED`, `TAG_REMOVED`, `NOTE_CREATED`, `NOTE_UPDATED`, `NOTE_DELETED`, `PACKAGE_ARCHIVED`, `PACKAGE_RESTORED`, `DELIVERY_CREATED`, `DELIVERY_COMPLETED`, `WITNESS_ATTACHED`, `PACKAGE_IMPORTED`, `PACKAGE_EXPORTED`, and `PROTOCOL_MIGRATED`.

`PKG-META-011`: Portable events MUST NOT contain UI clicks, cache rebuilds, worker leases, sync retries, telemetry, temporary download jobs, absolute local paths, or credentials.

`PKG-META-012`: A Version manifest is the authority for Version state; events explain chronology and MUST NOT need to be replayed to reconstruct a committed Version.

`PKG-META-013`: Unknown optional event types MUST be preservable. A Reader MAY display them generically without understanding their business semantics.

## 3. Provenance

`PKG-META-020`: Provenance MAY include Package-level, File-level, and Content-level facts.

Recommended source kinds include `local_import`, `package_import`, `google_drive`, `onedrive`, `dropbox`, `external_api`, `generated`, and `other`.

`PKG-META-021`: Provenance MAY store privacy-safe source object IDs, source revisions, original names, first-observed times, and source Package/Version references.

`PKG-META-022`: Provenance MUST NOT store OAuth/refresh tokens, sessions, credentials, signed URLs, OS Keyring locators, or unnecessary absolute paths.

`PKG-META-023`: Source facts MUST NOT alter FileID/ContentID authority; provenance describes where content came from, not a runtime dependency required for the Package to exist.

## 4. Extensions

`PKG-META-030`: Third-party extensions MUST live under `.packtell/extensions/<reverse-domain-or-stable-namespace>/`.

`PKG-META-031`: Unknown optional extensions MUST support preserve-through-read/write unless the user explicitly requests deletion.

`PKG-META-032`: Extensions MUST NOT override Core paths, impersonate Core schemas, or require execution of untrusted code in order to read the Core Package.
