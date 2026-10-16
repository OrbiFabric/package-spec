# Package Protocol 2.1: Optional Storage and Cloud Control Plane

Status: Draft / Normative (applies only to implementations opting into this storage-service extension)  
Specification release: **2.1**; existing portable wire/format discriminator remains **`orbifabric.package` / `2.0`**.

Without changing Package 2.0 Core, the Complete Profile, version identity, signing inputs, or offline verification, this chapter governs an **optional storage and recovery service architecture** usable by Packtell and OrbiFabric Cloud. "Cloud" here means the product system comprising a control plane and optional managed data plane. **The control plane not storing or relaying user file bytes does not imply that the Cloud product may never offer managed file backup.** A completed Complete Package remains independent of networks and storage vendors.

## 1. Scope and layers

`PKG-STORAGE-001`: A Host implementing these optional services **MUST** preserve Package existence, identity, Versions, offline verification, and Complete Profile semantics without requiring a Cloud account, vendor, or backup service.

`PKG-STORAGE-002`: This chapter **MUST NOT** modify existing Package 2.0 tree layout, format/version/schema discriminator, ContentID, VersionSubject, signature rules, conformance fixtures, or complete-history offline contracts; 2.1 is a backward-compatible specification supplement, not a mandatory migration of existing files.

`PKG-STORAGE-003`: A deployment using Cloud-coordinated storage **MUST** distinguish the Control Plane (accounts, authorization, entitlements, metadata, routing, jobs, policy, metering, audit), Managed Data Plane (storage vendors selected or replaced by OrbiFabric holding server-side encrypted objects), and Client-managed Data Plane (vendors where the user retains credentials). File bytes may reside in the latter two layers; the architecture does not prohibit all customer bytes from Cloud-managed infrastructure.

`PKG-STORAGE-004`: The Cloud Control Plane **MUST NOT** persist user files or Package bytes as ordinary application database records, upload/download proxies, or persistent request logs; direct client-to-storage-provider transfers are the default data path, coordinated by the control plane.

## 2. Identity, objects, and multiple locations

`PKG-STORAGE-010`: A Host providing remote backup **MUST** distinguish logical BackupObject / ContentID / File Revision / Package Version relationships from physical StorageLocations. Provider object keys, buckets, accounts, regions, and transfer URLs do not establish portable protocol identity.

`PKG-STORAGE-011`: A logical object **MAY** have multiple managed StorageLocations at once, such as local storage, user-owned Dropbox, and multiple Cloud-managed storage vendors. Migration or copying a location does not recreate the historical revision identity.

`PKG-STORAGE-012`: StorageLocation service metadata **MUST** retain non-secret facts sufficient for authorized lookup, environment/Space/account isolation, digest/length verification, and health assessment, without assuming a Package has only one physical location.

`PKG-STORAGE-013`: Backup target selection **SHOULD** be configurable policy rather than a hard-coded provider. Different objects may use different targets or redundancy policies, while location changes cannot alter portable Package authority.

## 3. File sources are not backups

`PKG-STORAGE-020`: A Host **MUST** distinguish references to third-party file sources (for example, Google Drive, OneDrive, and Dropbox) from explicitly authorized byte-backup destinations. A source reference does not prove a backup replica exists.

`PKG-STORAGE-021`: Cloud or a backup worker **MUST NOT** automatically download, replicate, or host a referenced third-party file merely because a user added that reference to a Package. Hydration and backup require an explicit business operation, source authorization, and revision checks.

`PKG-STORAGE-022`: For a formal Complete Package export, the Host **MUST** obtain all required bytes using the established ContentResolver and self-containment/integrity rules. A network-accessible StorageLocation or temporary download URL is not an embedded object of a Complete Profile.

## 4. First Packtell / Cloud release boundary (V1)

`PKG-STORAGE-030`: The first released Packtell personal byte-backup feature **MUST** expose only user-owned Dropbox (BYO / CLIENT_MANAGED) as its implemented destination. Google Drive and OneDrive remain file sources; other backup destinations and OrbiFabric-managed storage are future capabilities, not V1 deliverables.

`PKG-STORAGE-031`: Starting a new V1 automatic or manual backup write **MUST** obtain valid Cloud authorization under the approved commercial-entitlement contract; an unavailable Cloud or missing session cannot be reported as a new successful backup.

`PKG-STORAGE-032`: Existing V1 Dropbox backups **MUST** remain discoverable, readable, and restorable using the same user's Dropbox account and independent Backup Catalog when Cloud is unreachable, signed out, expired, or the account is disabled. Cloud APIs, tokens, indexes, and subscription renewal cannot be prerequisites for reading existing BYO backups.

`PKG-STORAGE-033`: V1 Dropbox backup **MUST** reuse the existing Provider OAuth connection and locally protected credential storage; it does not introduce a second backup authorization or upload Dropbox OAuth/refresh tokens to Cloud. The approved V1 Full Dropbox app uses a dedicated `/Apps/Packtell` directory; that directory is not an App Folder permission sandbox.

## 5. Future managed storage, vendors, and BYO extensions

`PKG-STORAGE-040`: An optional future CLOUD_MANAGED backup feature **MAY** place customer bytes at one or more underlying object storage vendors selected and operated by OrbiFabric (including S3-compatible services), with a unified Packtell/Cloud user experience rather than a vendor account requirement.

`PKG-STORAGE-041`: Future adapters **SHOULD** support policy-based configuration, replacement, migration, and simultaneous use of multiple vendors. "Switching vendors" means safe cutover after required copying and verification, not instant availability of bytes that have not yet been moved.

`PKG-STORAGE-042`: Future CLIENT_MANAGED backup **MAY** extend beyond Dropbox to user-owned S3/S3-compatible, WebDAV, and other adapters while keeping credentials in the client or a separately authorized user-controlled boundary and without forcing Cloud-managed storage.

`PKG-STORAGE-043`: Hybrid deployments **MAY** retain both BYO and CLOUD_MANAGED locations per ContentID/revision and select priority, capacity, quota, or failover policy. Hybrid does not mean automatically uploading every referenced source file.

`PKG-STORAGE-044`: A provider that is not actually enabled **MUST NOT** be advertised as operational, restorable, or cross-device tested merely because the data model or interface includes a placeholder.

## 6. Cloud coordination and client direct transfer

`PKG-STORAGE-050`: Before a CLOUD_MANAGED upload, the Control Plane **MUST** verify the user, Space, device, authority, entitlement, intended object, size/digest, quota, and provider policy, then select a StorageLocation and issue or coordinate an object-scoped, time-limited, operation-specific direct transfer authorization.

`PKG-STORAGE-051`: Before a CLOUD_MANAGED download, the Control Plane **MUST** revalidate current read authority and location status and supply the provider's direct-download capability or a governed location selection. A client-supplied object key, StorageLocation ID, or historical URL alone does not authorize reading.

`PKG-STORAGE-052`: For providers supporting presigned URLs, the Control Plane **SHOULD** return a short-lived TLS-only authorization URL limited to the HTTP method and a single object/scope. Expiration, retries, and multipart transfers belong to separately versioned service contracts.

`PKG-STORAGE-053`: Providers without native presigned URLs (including some WebDAV deployments) **MUST** use a separately security-reviewed direct-access delegation mechanism or stay CLIENT_MANAGED with credentials held by the client. S3-style presigning cannot be assumed universal.

`PKG-STORAGE-054`: Clients **MUST NOT** persist presigned URLs, temporary tokens, provider master credentials, or other transient transfer grants in portable Packages, Cloud Registry metadata, permanent Catalogs, analytics, or durable logs.

`PKG-STORAGE-055`: Upload/download status **MUST** distinguish a grant being issued, an attempted transfer, provider confirmation, end-to-end byte verification, publication of Catalog/Location, and successful client restoration. An issued URL or HTTP success is not equivalent to a completed backup or restore.

## 7. Integrity, security, and secrets

`PKG-STORAGE-060`: Before any managed or BYO BackupObject is published as restorable, the system **MUST** validate original-content ContentID/SHA-256, expected byte length, and immutable object binding. ETag, object key, or a provider upload success response alone is insufficient.

`PKG-STORAGE-061`: Restorable historical objects **MUST** use immutable or content-addressed no-overwrite storage semantics. Lost responses, conflicts, and uncertain side effects are reconciled under the original object identity rather than faking success or overwriting another revision.

`PKG-STORAGE-062`: Managed and BYO transfers **MUST** use protected transport and explicit at-rest encryption and key-responsibility models. TLS, provider SSE, and SHA-256 are compatible with V1; E2EE or zero-knowledge are not V1 claims. Future E2EE requires a separate key-loss, sharing, and recovery design.

`PKG-STORAGE-063`: The Cloud Control Plane **MUST NOT** hold CLIENT_MANAGED user OAuth refresh tokens, WebDAV passwords, or S3 master keys, or mix raw Package Root/full history/file bytes into Registry APIs that admit metadata only.

`PKG-STORAGE-064`: Managed direct-transfer grants **SHOULD** use least privilege, short TTL, and the narrowest object scope necessary, constraining digests, lengths, multipart operations, and receipts where vendor capabilities permit.

## 8. Vendor switching, migration, and reliability

`PKG-STORAGE-070`: A provider change **MUST** be treated as a controlled object migration or routing-policy adjustment, not as renaming a provider field in the database and pretending the bytes have moved.

`PKG-STORAGE-071`: Before changing an object's preferred download location, the migration process **MUST** establish that the destination exists, its complete SHA-256 and length match, its Catalog/revision closure is valid, and it is readable. Failures preserve the previous viable location.

`PKG-STORAGE-072`: Provider migration **SHOULD** copy and verify first, then change read routing, and only later consider deletion under separate retention rules. Old and new locations can coexist during migration; a verified prior location remains an available fallback.

`PKG-STORAGE-073`: Disabling backup, failed migration, expired Cloud entitlement, or revoked connection **MUST NOT** automatically delete existing BYO backups, historical objects, or their independent Catalog. Explicit deletion, lifecycle handling, and retention policy require separate authorization.

`PKG-STORAGE-074`: Provider outages, expired URLs, insufficient quotas, changed accounts, partial migrations, duplicate submissions, and uncertain asynchronous outcomes **MUST** produce distinct retryable, reauthorization-required, corrupt, partially restorable, or operator-required states, instead of being concealed as an empty Package.

## 9. Recovery and cross-device capabilities

`PKG-STORAGE-080`: BYO restoration **MUST** support independently listing Backup Catalogs in the authorized user's provider account, checking objects and history relationships, and recovering available content on a fresh installation without any Cloud session or metadata.

`PKG-STORAGE-081`: Future CLOUD_MANAGED cross-device recovery **MAY** use Cloud identity and metadata indexes to supply short-lived provider download authorization to a newly authorized device. Access rights during suspension, expiration, refund, deletion, and retention must be defined before this feature launches; BYO's perpetual independent-reading promise does not automatically apply.

`PKG-STORAGE-082`: A restorer **MUST** distinguish "file-source references requiring user reauthorization", "verified restorable backup bytes", and "Cloud metadata hints only"; none of these conditions establishes either of the other two.

`PKG-STORAGE-083`: A formal Complete Profile **MUST** continue to self-contain all committed Version bytes and portable history under the 2.0 offline contract. A remote-location-backed online backup is not a new portable Complete Profile and does not supersede offline verification.

## 10. Compatibility and implementation boundaries

`PKG-STORAGE-100`: This 2.1 supplement **MUST NOT** require changes to the existing `.packtell/format.json` `protocol_version="2.0"`, `schemas/*.v2`, `package-go` byte contracts, Version Subjects, existing fixtures/vectors, or support for 2.0 Readers. New portable wire fields and migrations require separate review and versioning.

`PKG-STORAGE-101`: Control Plane APIs, vendor adapters, grants/confirmations, quotas, keys, storage billing, migration jobs, location models, and restore authorization **SHOULD** be versioned in separate Cloud/Packtell service contracts. This chapter does not invent already-implemented APIs/schemas or claim present clients support future capabilities.

`PKG-STORAGE-102`: Products opting into this extension **MUST** separately validate real provider authorization, upload/download, byte digests, restorable Catalogs, native devices, Cloud outages, supplier migrations, and permission revocation. Passing portable 2.0 conformance does not constitute passing optional Cloud storage acceptance.

## 11. Phased product scope (informative)

| Capability | Packtell V1 | Future increments |
|---|---|---|
| Package Core/Complete/Profile/signatures | Existing 2.0 portable byte contract | Compatible evolution |
| Third-party file sources | Google Drive, OneDrive, Dropbox | Extendable references, no automatic source-byte backup |
| Bring-your-own backup | **Dropbox only**, existing OAuth and independent Catalog | BYO S3, WebDAV, others |
| OrbiFabric-managed byte backup | **Not available**; do not claim release readiness | Multiple managed providers coordinated by Cloud, direct client transfer |
| Location policies / hybrid / migrations | Extensible model only; no managed switching operation | Multiple locations, verified cutover, governed migration |
| Cross-device restore | Independent Dropbox restore design; platform acceptance must be demonstrated | Managed download grants and explicit access/retention policy |
| User file bytes within Cloud product | V1 only metadata and witnesses; Dropbox backup bytes bypass Cloud | Managed bytes at replaceable vendor data planes, not the Cloud control-plane database |

References: existing [Core and Complete Profile](04-content-complete-profile.md), [signing](06-verification-signing.md), [Delivery and Evidence](07-delivery-evidence.md), and [exact byte contracts](10-implementation-contracts.md) remain in force.
