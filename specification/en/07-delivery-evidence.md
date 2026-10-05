# Delivery, Witness, and Evidence

Status: Draft / Normative

## 1. Delivery is an independent lifecycle aggregate

`PKG-DELIVERY-001`: A Delivery MUST reference a specific `package_id` and `package_version_id`; Delivery MUST NOT define Package or Version identity.

`PKG-DELIVERY-002`: One PackageVersion MAY have multiple Deliveries, each with an independent `delivery_id`.

`PKG-DELIVERY-003`: A formal Delivery MUST reference a verifiable signed Version Subject; a Dirty Working Tree MUST first become a new committed Version.

## 2. Portable Delivery history

A Complete Profile MAY store:

```text
.packtell/evidence/deliveries/<delivery-id>/
├── delivery.json
├── record.json                 # optional
├── receipt.json                # optional
└── verification.json           # optional cached/result facts
```

`PKG-DELIVERY-010`: `delivery.json` SHOULD preserve portable business facts such as recipient, purpose, channel, and time while avoiding unnecessary secrets and credentials.

`PKG-DELIVERY-011`: A signature used by a Delivery to prove the Package MUST ultimately reference/verify the Version Seal of the PackageVersion being delivered; it MUST NOT replace the Version Subject by signing ZIP bytes.

`PKG-DELIVERY-012`: When Cloud produces a Delivery Record, verification capability, signed receipt, or Lifecycle Witness, those MUST be stored as separate evidence objects and MUST NOT rewrite a committed Version.

## 3. Cloud Evidence

`PKG-DELIVERY-020`: Cloud Anchor, Package Witness, Lifecycle Witness, and Delivery Verification Receipt MUST each use their own versioned schema, canonical subject, and signing-key purpose.

`PKG-DELIVERY-021`: Offline cryptographic validity and online current status MUST be reported separately; online states such as `revoked`, `invalidated`, or `compromised` MUST NOT be represented by rewriting historical signature bytes.

`PKG-DELIVERY-022`: A Complete Profile MAY carry Cloud evidence snapshots already obtained at creation/export time, but MUST NOT claim that a snapshot automatically represents future online status.

## 4. Evidence append

`PKG-DELIVERY-030`: Appending later Evidence MUST NOT change a previous PackageVersion's Version Subject, ContentID, VersionID, or signature.

`PKG-DELIVERY-031`: Evidence objects SHOULD identify issuer, subject reference, created/observed time, schema, signature/key metadata, and an optional status reference.

`PKG-DELIVERY-032`: Missing or deleted Evidence MUST NOT automatically turn already-passing local content integrity into failure; a Verifier must report dimensions separately.
