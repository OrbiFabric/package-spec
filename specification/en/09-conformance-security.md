# Conformance, Security, and Evolution

Status: Draft / Normative

## 1. Conformance levels

Standard implementation levels are:

- Core Reader
- Core Writer
- Complete Reader
- Complete Writer
- Verifier
- Container Codec

`PKG-CONF-001`: An implementation MUST claim only levels it actually passes in the conformance suite.

`PKG-CONF-002`: Packtell's formal Package 2.0 integration SHOULD pass at least Complete Reader, Complete Writer, Verifier, Directory Codec, and ZIP Codec.

## 2. Shared fixtures

`PKG-CONF-010`: Go, JS, Python, PHP, and other SDKs MUST use the same language-independent fixtures/vectors to determine compatibility.

Recommended fixtures include minimal-valid, complete-history, dirty-working-tree, renamed-file, modified-file, missing-object, unknown-extension, bad-signature, path-traversal, case-conflict, cloud-origin, and multi-delivery.

`PKG-CONF-011`: `package-go` is the Reference Implementation; when it conflicts with normative specification/vector behavior, the Go implementation must be fixed.

## 3. Security

`PKG-CONF-020`: Parsers MUST apply resource policies for entry count, per-file size, total expanded size, compression ratio, JSON/NDJSON size, and recursion/depth when reading untrusted Packages.

`PKG-CONF-021`: A Verifier MUST NOT execute Package HTML/JS/binaries to determine Core validity.

`PKG-CONF-022`: Extract MUST use no-traversal, no-overwrite/staging, and safe commit semantics; failure must not leave output that can be mistaken for success.

`PKG-CONF-023`: Private keys, OAuth tokens, refresh tokens, PKCE verifiers, Cloud sessions, and credentials MUST NOT be written into Packages, fixtures, or diagnostic logs.

## 4. Forward compatibility

`PKG-CONF-030`: An unknown Protocol major MUST return unsupported and MUST NOT be guessed at.

`PKG-CONF-031`: Within the same major, unknown optional fields SHOULD be ignored while being preserved when possible; an unknown required capability MUST fail closed.

`PKG-CONF-032`: Extension, Evidence, and event subschemas SHOULD version independently so local changes do not mechanically increment the entire Package major.

## 5. Migration and protocol upgrade

`PKG-CONF-040`: A protocol migration event MUST be distinct from a business PackageVersion; a structural protocol upgrade with unchanged logical state SHOULD NOT create a new business PackageVersion.

`PKG-CONF-041`: For a future major upgrade, any destructive migration MUST be defined by that major's independent specification; 2.0 does not pre-authorize silent destruction of history.
