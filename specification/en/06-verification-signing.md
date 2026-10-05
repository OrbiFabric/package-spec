# Verification, Signing, and Trust

Status: Draft / Normative

## 1. Verification dimensions

`PKG-SIGN-001`: A Verifier MUST separately report at least Package Recognition, Tree Structure, Working Tree State, Committed Content Integrity, Version Seal, History Completeness, and Evidence/Online Status.

`PKG-SIGN-002`: A `DIRTY` Working Tree MUST NOT automatically imply invalid committed history.

`PKG-SIGN-003`: Successful hash integrity MUST NOT be presented as verified real-world identity.

## 2. Canonical JSON

Package 2.0 reuses `orbifabric.canonical-json.v1`.

`PKG-SIGN-010`: Canonical JSON MUST use UTF-8 without BOM or insignificant whitespace; object keys are recursively ordered by the lexical order of UTF-8 bytes corresponding to Unicode code points; strings are not HTML-escaped; NaN/Infinity and identity-critical floating-point values are forbidden.

`PKG-SIGN-011`: Every signed subject MUST use a domain-separated, versioned subject schema; implementations MUST NOT directly sign arbitrary UI JSON.

## 3. Version Subject

Conceptual subject:

```text
PackageID
PackageVersionID
Version ordinal / lineage facts
Version manifest digest
Committed content root/digests
Sealed version metadata digest
Protocol / tree profile reference
```

`PKG-SIGN-020`: A Version signature MUST bind the canonical Version Subject rather than complete ZIP/TAR/container bytes.

`PKG-SIGN-021`: Directory, ZIP, and TAR representations of the same committed logical Version MUST verify to the same Version Subject digest.

## 4. Signer Profile

Package 2.0 continues the existing OrbiPack/Packtell `PackageSigner` abstraction.

Standard signer types include at least:

- `local_device`
- `orbifabric_official`

`PKG-SIGN-030`: When no Cloud official signer is available, Packtell Complete Profile MUST by default use a dedicated local Ed25519 package-signing key; the private key MUST NOT be written into the Package.

`PKG-SIGN-031`: When a connected and selected OrbiFabric official signing profile is available, Packtell MUST use the Cloud/official signer to sign the same Version Subject.

`PKG-SIGN-032`: Once a signing operation selects a signer profile, failure MUST NOT silently switch to another signer while presenting the same operation as successful.

`PKG-SIGN-033`: A local private key SHOULD live in an OS secure credential store; the Package carries only public key, fingerprint, Key ID, algorithm, and signature metadata required for verification.

`PKG-SIGN-034`: A Cloud/official signing response MUST be verified by the client for subject, environment, Key ID, public-key fingerprint, and Ed25519 signature before embedding it.

## 5. Trust separation

`PKG-SIGN-040`: Version Signature, Cloud Anchor, Delivery Record/Receipt, and Lifecycle Witness MUST use distinct schemas/subjects and MUST NOT collapse into a single `valid` boolean.

`PKG-SIGN-041`: Cloud Anchor/Witness MAY be created after the Version and MUST NOT change Version identity.

`PKG-SIGN-042`: A Verifier SHOULD distinguish local/unregistered signer, cloud-registered/official signer, unknown signer, invalid signature, and online status.
