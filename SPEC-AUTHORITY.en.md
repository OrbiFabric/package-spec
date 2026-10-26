# Package 2.1 Specification Authority, Language, and Change Rules

Status: Draft / Normative Governance

## 1. Normative keywords

MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY use their RFC-style meanings. Chinese and English counterparts must preserve the same requirement strength.

## 2. Authority order

In case of conflict:

1. Chinese normative specification;
2. machine-readable schemas for structure, types, and required/allowed values;
3. canonicalization and cryptographic algorithm specifications for byte-level behavior;
4. conformance vectors and expected results for defined test inputs;
5. official English translation;
6. `package-go` reference implementation;
7. other SDKs, CLI, web verifier, and product implementations.

An implementation conflict is an implementation bug, not an automatic specification change.

## 3. Bilingual requirements

`PKG-GOV-001`: Every normative Chinese document MUST have a corresponding English document.  
`PKG-GOV-002`: Corresponding Chinese and English clauses MUST use identical Clause IDs.  
`PKG-GOV-003`: Protocol fields, schema IDs, enum values, algorithm names, and paths MUST use English only.  
`PKG-GOV-004`: Irreducible natural-language ambiguity is resolved in favor of the Chinese primary text.

## 4. Clause IDs

Stable namespaces include `PKG-CORE-*`, `PKG-TREE-*`, `PKG-VERSION-*`, `PKG-CONTENT-*`, `PKG-META-*`, `PKG-SIGN-*`, `PKG-DELIVERY-*`, `PKG-CODEC-*`, `PKG-CONF-*`, `PKG-GOV-*`, and `PKG-STORAGE-*` (optional 2.1 storage-service extension).

## 5. Version governance

`PKG-GOV-010`: Minor changes within Protocol `2.x` MUST remain backward compatible.  
`PKG-GOV-011`: Breaking Core semantics, Package Tree interpretation, Canonical Subject semantics, or required-field meaning MUST increment the protocol major version.  
`PKG-GOV-012`: Subschemas such as Notes, Events, Provenance, and Evidence MAY evolve independently without mechanically incrementing the protocol major version.  
`PKG-GOV-013`: Unknown optional extensions MUST be preservable and safely ignorable; unknown required capabilities MUST fail closed.

## 6. Package 1.x policy

`PKG-GOV-020`: Package 1.x is an unreleased development protocol.  
`PKG-GOV-021`: Package 2.0 has no reader, writer, migration, or data-compatibility obligation for 1.x.  
`PKG-GOV-022`: 1.x code and fixtures MAY be used temporarily during the clean break, but production legacy fallback MUST NOT remain after the migration is complete.

## 7. Specification versus implementation

`PKG-GOV-030`: The protocol MUST NOT depend on Packtell, Wails, SQLite, OrbiFabric Cloud, or one programming language.  
`PKG-GOV-031`: `package-go` is a reference implementation, not the normative source.  
`PKG-GOV-032`: Other language SDKs MUST implement against this specification and the shared conformance assets.

## 8. 2.1 compatibility supplement and optional services

`PKG-GOV-033`: The optional 2.1 Cloud storage architecture **MUST NOT** introduce a Cloud/Provider dependency for Package Core or silently alter byte semantics of existing `protocol_version="2.0"` files, Version Subjects, schemas, signatures, or conformance.

`PKG-GOV-034`: New Storage services **MUST** distinguish Control Plane from optional Managed/BYO Data Planes; managed backups reside at actual providers, not as persistent user bytes in the control plane. Service APIs and the portable protocol are separately versioned. See [chapter 11](specification/en/11-storage-control-plane.md).

## 9. Explicit pre-release 2.0 timestamp representation reset (Founder 2026-10-25)

`PKG-GOV-035`: Before any public 2.0 release, the Founder expressly authorizes **one development-time 2.0 clean break**: every Portable 2.0 timestamp MUST be UTC RFC3339 with **exactly six microsecond digits and literal `+00:00`**, not `Z`. This supersedes pre-release timestamp byte semantics and is not a backward-compatible published 2.x minor upgrade. Implementations MUST update Subjects, schemas, conformance vectors, and verifiers, and MUST NOT silently accept old `Z` as a current signed timestamp. New signed hashes and bytes must be generated from new canonical content; string replacement cannot make historical signatures valid. Once published, breaking changes remain subject to the major-version rule in `PKG-GOV-010/011`.
