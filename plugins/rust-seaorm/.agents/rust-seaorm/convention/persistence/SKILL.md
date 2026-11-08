---
name: persistence
description: Use SeaORM entities, ActiveModel writes, upserts, transactions and DbErr classification in a Rust storage adapter, and configure its SQLite connection. Use when adding or changing SeaORM storage; generic transaction, failure and SQLite rules are `rust:persistence`, and hand-written SQL projects select `rust-sqlx` instead.
kind: convention
domain: rust
profile: core
applicability: Projects explicitly selecting rust-seaorm
requires: rust, sea-orm
provenance: framework
---

# SeaORM persistence

Owns SeaORM entities, ActiveModel writes, the SeaORM transaction API, `DbErr` classification and SeaORM's
SQLite connection setup. `rust:persistence` owns transaction scope, failure categories and SQLite engine
rules; `rust-seaorm:migrations` owns the schema.

```rust
let txn = db.begin().await?;
let row = session::Entity::insert(session::ActiveModel {
    id: NotSet,
    host: Set(handle.host().as_str().to_owned()),
    native_id: Set(handle.native_id().to_owned()),
    ..Default::default()
})
.on_conflict(
    OnConflict::columns([session::Column::Host, session::Column::NativeId])
        .update_columns([session::Column::Cwd, session::Column::EndedAt])
        .to_owned(),
)
.exec_with_returning(&txn)
.await?;
txn.commit().await?;
```

## Entities are adapter row types

Entities (`DeriveEntityModel`) live in the storage adapter, `pub(crate)`, and convert to and from domain
types at the edge per `rust:structure`; the domain never holds a `Model` or `ActiveModel`. Write each
entity to match the migrated schema, with `Option<T>` exactly where the column is nullable, and declare
`DeriveRelation` only for joins the adapter uses. A domain type never derives SeaORM traits.

## Writes

Build an `ActiveModel` with `Set` for every written column and `NotSet` for generated ones such as an
auto-increment key. Use `insert(...).exec_with_returning` to get the stored row, and
`on_conflict(OnConflict::columns(...))` for an upsert keyed by a natural unique key instead of a read
followed by an insert, which races. An upsert that inserts nothing returns `DbErr::RecordNotInserted`;
use `on_conflict_do_nothing` with `try_insert` when that is a normal outcome. Enable
`sqlite-use-returning-for-3_35` for `RETURNING` on SQLite.

## Transactions and failures

Begin with `TransactionTrait::begin`, pass `&txn` to every participating call and `commit()` it; a dropped
`DatabaseTransaction` rolls back. Generic over `impl ConnectionTrait`, a helper runs on either the
connection or a transaction. Classify `DbErr` with `sql_err()`: `SqlErr::UniqueConstraintViolation` and
`ForeignKeyConstraintViolation` are conflicts; other errors are unavailable storage, kept as the source.

## SQLite connection

Build `SqliteConnectOptions` from a path, set `create_if_missing`, `foreign_keys(true)`, `busy_timeout`
and `journal_mode`, connect a pool with `SqlitePoolOptions` and wrap it with
`SqlxSqliteConnector::from_sqlx_sqlite_pool`. `sea_orm::sqlx` re-exports the matching SQLx, so add no
separate `sqlx` dependency. Alternatively `ConnectOptions::map_sqlx_sqlite_opts` applies the same
options to a URL connection. Select only the features used: `sqlx-sqlite`, one `runtime-*`, `macros`
and the `with-*` type features.

Sources: [SeaORM docs](https://www.sea-ql.org/SeaORM/docs/index/),
[insert and upsert](https://www.sea-ql.org/SeaORM/docs/basic-crud/insert/),
[DbErr](https://docs.rs/sea-orm/latest/sea_orm/error/enum.DbErr.html),
[ConnectOptions](https://docs.rs/sea-orm/latest/sea_orm/struct.ConnectOptions.html).
