---
name: style
description: Tommy's agreed Rust style — naming, formatting, comments and lint policy. Read before writing or reviewing Rust that touches it; nothing applies until it is recorded here.
kind: contract
domain: rust
profile: contract
applicability: Rust projects
requires: rust
provenance: house
---

# Rust style

Owns naming, formatting, comments, and the lint policy above the repository's clippy configuration.

## Agreed

- A type does not repeat its module's name (`card::Title`, `card::Status`, `card::FinishError`); the main
  type may equal it (`card::Card`). Import types by path, call functions through their module
  (`service::finish_card`), and qualify a generic or clashing name (`card::Status`). Enforced by clippy
  `module_name_repetitions = "warn"`. Source: RFC 356 (`io::Error`); the Book 7.4.
