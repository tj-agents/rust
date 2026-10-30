---
name: migrations
description: Manage Rust SQLx schema migrations, preservation tests and offline query metadata when SQLx macros are selected. Use when changing SQLx schema, embedding migrations or updating .sqlx metadata; runtime queries do not require offline metadata.
kind: standard
domain: rust
profile: core
applicability: Projects explicitly selecting rust-sqlx
requires: rust, sqlx-migrate
provenance: framework
---

# SQLx migrations

Owns SQLx migration execution, schema verification and optional query-macro metadata. The application owns
schema content and deployment policy. Select the engine and matching SQLx/CLI versions before using commands.

```sh
# Against a disposable database with DATABASE_URL set for the selected engine:
cargo sqlx migrate run
# Only when query!/query_as! macros and workspace metadata are selected:
cargo sqlx prepare --workspace -- --all-targets --all-features
cargo sqlx prepare --check --workspace -- --all-targets --all-features
```

Apply migrations before admitting operations against the schema they require; make migration failure a
visible startup/deployment failure. For embedded migrate!, arrange Cargo rebuild tracking when migration
files change (for example build.rs rerun-if-changed on migrations/); verify a newly added migration actually
ships in a fresh artifact. Do not rewrite migration history that deployed data depends on unless the
application explicitly owns a resettable database policy. Test both an empty database and an upgrade from
a representative prior schema, preserving data and checking constraints. Verify failure leaves the
application in its documented recoverable state. SQLite-specific connection PRAGMAs may not take effect
inside a migration transaction; connection configuration belongs in `rust-sqlx:persistence`.

Query macros check against a database or prepared .sqlx metadata; runtime query/query_as calls do not gain
compile-time schema validation from that metadata. If macros are selected, generate metadata from the
migrated disposable schema with all relevant feature/target combinations, commit it and check freshness
in CI. For offline builds set SQLX_OFFLINE=true explicitly so an ambient DATABASE_URL cannot silently
change the build path. Validate online preparation separately from offline compilation; neither replaces
real-engine migration and transaction tests. Add a separate SQLx testing skill only when that concern grows.

Sources: [SQLx CLI](https://github.com/transact-rs/sqlx/blob/main/sqlx-cli/README.md),
[embedded migrations](https://docs.rs/sqlx/latest/sqlx/macro.migrate.html).
