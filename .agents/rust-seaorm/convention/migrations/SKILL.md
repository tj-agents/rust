---
name: migrations
description: Author and run SeaORM schema migrations with sea-orm-migration — a Migrator listing Rust migration modules, SchemaManager table definitions, transactional application on SQLite and running pending migrations at startup. Use when creating or changing a SeaORM schema; migration policy and tests are `rust:persistence`.
kind: convention
domain: rust
profile: core
applicability: Projects explicitly selecting rust-seaorm
requires: rust, sea-orm-migration
provenance: framework
---

# SeaORM migrations

Owns how a SeaORM project writes and applies migrations. `rust:persistence` owns when they run, history
immutability, concurrent first use and migration tests; `rust-seaorm:persistence` owns entities.

```rust
#[derive(DeriveMigrationName)]
pub(crate) struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    fn use_transaction(&self) -> Option<bool> {
        Some(true)
    }

    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .create_table(
                Table::create()
                    .table(Sessions::Table)
                    .col(pk_auto(Sessions::Id))
                    .col(string(Sessions::Host))
                    .col(timestamp_with_time_zone_null(Sessions::EndedAt))
                    .index(Index::create().unique().col(Sessions::Host).col(Sessions::NativeId))
                    .to_owned(),
            )
            .await
    }
}
```

Migrations are the only author of the schema. Each is a module named `mYYYYMMDD_HHMMSS_<what>` listed in
order by one `Migrator: MigratorTrait`; an application keeps them in a `migration` module of its storage
adapter unless a separate migration crate or CLI is a concrete need. Name tables and columns with
`DeriveIden` enums local to the migration and build columns with `sea_orm_migration::schema` helpers;
never reference entities, which change after the migration ships.

SeaORM wraps a migration in a transaction only on PostgreSQL by default. Return `Some(true)` from
`use_transaction` so a failed SQLite migration rolls back with its `seaql_migrations` record. Implement
`down` only when the application actually rolls back.

At startup call `Migrator::up(db, None)` when `Migrator::get_pending_migrations(db)` is non-empty, before
serving operations. If `up` fails, re-check pending migrations: an empty list means another process
applied them, otherwise surface the failure. Use `sea-orm-cli migrate generate` for new files and
`sea-orm-cli generate entity` against a migrated disposable database to check hand-written entities.
Do not use entity-first schema sync for a schema that has deployed data.

Sources: [migrations](https://www.sea-ql.org/SeaORM/docs/migration/setting-up-migration/),
[running migrations](https://www.sea-ql.org/SeaORM/docs/migration/running-migration/),
[MigrationTrait](https://docs.rs/sea-orm-migration/latest/sea_orm_migration/trait.MigrationTrait.html).
