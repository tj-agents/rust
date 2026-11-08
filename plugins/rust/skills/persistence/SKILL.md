---
name: persistence
description: Rust persistence rules that hold whichever database library a project selects — the operation that owns a transaction, classifying storage failures, applying the schema before use, immutable migration history, tests against a real engine, and SQLite engine settings. Use when adding storage, a transaction or a migration to a Rust project; library detail lives in `rust-sqlx` or `rust-seaorm`.
kind: convention
domain: rust
profile: persistence
applicability: Rust projects that persist state, regardless of persistence library
requires: rust
provenance: framework
---

# Persistence

Read and follow the [canonical definition](../../.agents/rust/convention/persistence/SKILL.md) in full.
This discovery entry is generated; edit the referenced `.agents/` definition.
