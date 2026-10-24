---
name: persistence
description: Use Rust SQLx pools, bound queries, explicit row mapping and transactions. Use when adding SQLx storage, handling driver failures, or configuring a SQLite connection; Tauri and other database engines are independent selections.
kind: convention
domain: rust
profile: core
applicability: Projects explicitly selecting rust-sqlx
requires: rust, sqlx
provenance: framework
---

# SQLx persistence

Owns SQLx connection/pool lifetime, bound queries, row mapping and explicit transactions in Rust.
The namespace distinguishes this crate from Go sqlx. Domain operations and generic Rust error rules stay
with their owners; Tauri is not a prerequisite and a driver is explicitly selected by the application.

```rust
async fn rename_record(pool: &sqlx::SqlitePool, id: i64, name: &str)
    -> Result<u64, sqlx::Error>
{
    let mut transaction = pool.begin().await?;
    let changed = sqlx::query("UPDATE records SET name = ? WHERE id = ?")
        .bind(name).bind(id).execute(&mut *transaction).await?.rows_affected();
    transaction.commit().await?;
    Ok(changed)
}
// SQLite example; the caller maps this adapter error to its operation-owned error.
```

Own the pool for the application's actual lifetime; cloning a pool handle shares its underlying pool.
Pass a borrowed pool/connection or transaction to the operation that needs it rather than reconnecting for
each query. Bind values and map rows deliberately. Placeholder syntax and supported types depend on the
driver; identifiers and SQL fragments need an explicit trusted construction strategy, not value binding.

For a change spanning statements, begin one transaction, execute every participating statement through
that transaction's connection and commit only when the operation succeeds. A statement sent through the
pool is outside that transaction. Explicitly handle commit failure; dropping an unfinished transaction
initiates rollback. Keep external calls and renderer interactions outside a long-held database transaction.

Map driver failures at the owning adapter/operation boundary, retaining useful causes per `rust:errors`.
Do not collapse not-found, constraint conflict and unavailable storage into one successful empty result.
Choose query macros or runtime queries explicitly; `rust-sqlx:migrations` covers schema and macro metadata.
Exercise constraints and transaction failure/rollback with a real temporary instance of the selected engine.

SQLite-specific: configure foreign-key enforcement for every pooled connection through SqliteConnectOptions;
set timeout/concurrency and journal policy deliberately for the application. WAL does not permit multiple
simultaneous writers or make copying only the main file a consistent backup. Use an engine-supported
snapshot/backup procedure and verify restore; PostgreSQL/MySQL do not inherit these SQLite details.

Sources: [Pool](https://docs.rs/sqlx/latest/sqlx/struct.Pool.html),
[Transaction](https://docs.rs/sqlx/latest/sqlx/struct.Transaction.html),
[SqliteConnectOptions](https://docs.rs/sqlx/latest/sqlx/sqlite/struct.SqliteConnectOptions.html),
[query binding](https://github.com/transact-rs/sqlx/blob/main/FAQ.md).
