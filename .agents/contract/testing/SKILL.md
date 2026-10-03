---
name: testing
description: Tommy's agreed Rust testing — unit and integration tests, their naming, layout and fixtures. Read before writing or reviewing Rust that touches it; nothing applies until it is recorded here.
kind: contract
domain: rust
profile: contract
applicability: Rust projects
requires: rust
provenance: house
---

# Rust testing

Owns unit and integration tests, their naming and layout, and fixtures.

## Agreed

- Unit tests sit in a `#[cfg(test)] mod tests` at the bottom of the file they test. Integration tests form
  one binary, `tests/it/main.rs`, with a module per area. Why: one binary links the crate once. Source: the
  Book 11.3; matklad, "Delete Cargo Integration Tests".
