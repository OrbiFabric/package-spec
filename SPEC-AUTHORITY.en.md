# Package 2.0 Specification Authority, Language, and Change Rules

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

Stable namespaces include `PKG-CORE-*`, `PKG-TREE-*`, `PKG-VERSION-*`, `PKG-CONTENT-*`, `PKG-META-*`, `PKG-SIGN-*`, `PKG-DELIVERY-*`, `PKG-CODEC-*`, `PKG-CONF-*`, and `PKG-GOV-*`.

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
