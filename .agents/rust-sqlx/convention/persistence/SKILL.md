---
name: persistence
description: Use Rust SQLx pools, bound queries, explicit row mapping and SQLx transactions. Use when adding SQLx storage or configuring a SQLx SQLite connection; generic transaction, failure and SQLite rules are `rust:persistence`, and an ORM project selects `seaorm` instead.
kind: convention
domain: rust
profile: core
applicability: Projects explicitly selecting rust-sqlx
requires: rust, sqlx
provenance: framework
---

# SQLx persistence

Owns SQLx connection/pool lifetime, bound queries, row mapping and the SQLx transaction API in Rust.
The namespace distinguishes this crate from Go sqlx. `rust:persistence` owns transaction scope, failure
classification and SQLite engine rules; Tauri is not a prerequisite and the application selects the driver.

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
```

Own the pool for the application's actual lifetime; cloning a pool handle shares its underlying pool.
Pass a borrowed pool/connection or transaction to the operation that needs it rather than reconnecting for
each query. Bind values and map rows deliberately. Placeholder syntax and supported types depend on the
driver; identifiers and SQL fragments need an explicit trusted construction strategy, not value binding.
Execute statements inside a transaction through `&mut *transaction`.

Inspect `sqlx::Error::Database` and its `kind()` to tell a unique or foreign-key violation from an
unavailable database. Choose query macros or runtime queries explicitly; `rust-sqlx:migrations` covers
schema and macro metadata. Configure SQLite through `SqliteConnectOptions` (`foreign_keys`,
`busy_timeout`, `journal_mode`, `create_if_missing`) so every pooled connection gets it.

Sources: [Pool](https://docs.rs/sqlx/latest/sqlx/struct.Pool.html),
[Transaction](https://docs.rs/sqlx/latest/sqlx/struct.Transaction.html),
[SqliteConnectOptions](https://docs.rs/sqlx/latest/sqlx/sqlite/struct.SqliteConnectOptions.html),
[query binding](https://github.com/transact-rs/sqlx/blob/main/FAQ.md).
