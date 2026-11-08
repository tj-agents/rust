---
name: migrations
description: Manage Rust SQLx migration files, embedded migrations and offline query metadata when SQLx macros are selected. Use when changing SQLx schema, embedding migrations or updating .sqlx metadata; migration policy and tests are `rust:persistence`, and runtime queries do not require offline metadata.
kind: convention
domain: rust
profile: core
applicability: Projects explicitly selecting rust-sqlx
requires: rust, sqlx-migrate
provenance: framework
---

# SQLx migrations

Owns SQLx migration execution and optional query-macro metadata. `rust:persistence` owns when migrations
run, history immutability and migration tests. Select the engine and matching SQLx/CLI versions first.

```sh
# Against a disposable database with DATABASE_URL set for the selected engine:
cargo sqlx migrate run
# Only when query!/query_as! macros and workspace metadata are selected:
cargo sqlx prepare --workspace -- --all-targets --all-features
cargo sqlx prepare --check --workspace -- --all-targets --all-features
```

Migrations are SQL files under `migrations/`. For embedded `migrate!`, arrange Cargo rebuild tracking when
migration files change (for example `build.rs` `rerun-if-changed` on `migrations/`) and verify a newly added
migration actually ships in a fresh artifact.

Query macros check against a database or prepared .sqlx metadata; runtime query/query_as calls do not gain
compile-time schema validation from that metadata. If macros are selected, generate metadata from the
migrated disposable schema with all relevant feature/target combinations, commit it and check freshness
in CI. For offline builds set SQLX_OFFLINE=true explicitly so an ambient DATABASE_URL cannot silently
change the build path. Validate online preparation separately from offline compilation; neither replaces
real-engine migration and transaction tests.

Sources: [SQLx CLI](https://github.com/transact-rs/sqlx/blob/main/sqlx-cli/README.md),
[embedded migrations](https://docs.rs/sqlx/latest/sqlx/macro.migrate.html).
