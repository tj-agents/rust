---
name: persistence
description: Use when Rust storage operations own transactions, classify failures, evolve schemas or validate real-engine behaviour.
kind: convention
domain: rust
profile: persistence
applicability: Rust projects that persist state, regardless of persistence library
requires: rust
provenance: framework
---

# Persistence

Owns library-independent storage rules: transactions, failure classification, schema lifecycle and tests.

```rust
#[derive(Debug, thiserror::Error)]
pub enum SaveError {
    #[error("work item {0} is already linked")]
    Conflict(WorkItemRef),
    #[error("link store unavailable")]
    Unavailable(#[source] Box<dyn std::error::Error + Send + Sync>),
}
// The adapter classifies its library's error; the domain never sees a driver type.
```

A project selects one library family: `rust-sqlx` for hand-written SQL with explicit row mapping, or
`seaorm` for entities, ActiveModel and Rust migrations. `rust:structure` owns where the adapter and its
row types live; `rust:errors` owns error shape.

## Transactions

The operation that needs atomicity owns the transaction: begin it once, send every participating
statement through it and commit only when the operation succeeds. A statement sent through the pool or
connection instead of the transaction is outside it. Dropping an unfinished transaction rolls it back;
handle a commit failure explicitly. Keep network calls and user interaction outside an open transaction.

## Failures

Map library failures at the adapter boundary into the operation's own error. Keep not found, constraint
conflict and unavailable storage distinct; never turn any of them into a successful empty result.

## Schema lifecycle

Apply pending migrations before admitting any operation that needs them, and make a migration failure a
visible startup or deployment failure. Never rewrite a migration that deployed data depends on; add a new
one. Run each migration in a transaction where the engine supports transactional DDL, so a failure leaves
the previous schema. Concurrent first use by several processes must either serialise or tolerate another
process having applied the same migration.

## Tests

Exercise constraints, transaction rollback and migrations against a real temporary instance of the
selected engine. Test both an empty database and an upgrade from a representative prior schema, checking
that data survives and constraints hold, and that a failing migration leaves the previous schema and the
migration unrecorded.

## SQLite

Enable foreign-key enforcement on every pooled connection; it is per connection. Set the busy timeout and
journal mode deliberately. WAL allows concurrent readers but still one writer, and copying only the main
file is not a consistent backup; use the engine's backup API and verify a restore. PRAGMAs that change
connection behaviour may not take effect inside a migration transaction, so set them in connection options.
PostgreSQL and MySQL do not inherit these rules.

Sources: [SQLite foreign keys](https://www.sqlite.org/foreignkeys.html),
[WAL](https://www.sqlite.org/wal.html), [backup API](https://www.sqlite.org/backup.html).
