# rust

Rust learning companion and standards for Claude Code and Codex, published as `rust@tj-agents` from the
`tj-agents` marketplace.

## Optional sibling capabilities

Select `tauri@tj-agents` for `tauri:structure` and `tauri:commands`. For persistence a project selects
one library family: `rust-sqlx@tj-agents` (`rust-sqlx:persistence`, `rust-sqlx:migrations`) for hand-written
SQL with explicit row mapping, or `rust-seaorm@tj-agents` (`rust-seaorm:persistence`,
`rust-seaorm:migrations`) for SeaORM entities, ActiveModel and Rust migrations. Neither supersedes the
other; `rust:persistence` holds the rules both share. Each family depends on Rust but not on Tauri, React
or a database engine. Tauri, SQLx and SeaORM source evidence activates their routes; an ordinary Rust file
does not activate any framework.
SQLite-specific guidance is labelled; generic Rust contracts retain their existing scope and decisions.
Testing/packaging capabilities are added when those stages are entered, without placeholder families.

## Skills

- Knowledge: `rust:learning` (learning and delivery modes, teaching rules, and how a convention is agreed),
  `rust:knowledge` (what Tommy has proven he knows), `rust:direction` (the goal, the skill tree and the
  references).
- Core contracts, each rule recorded only after Tommy decides it: `rust:style`, `rust:structure`,
  `rust:domain-design`, `rust:errors`, `rust:testing`, `rust:build` and `rust:libraries`.
- Persistence, independent of library: `rust:persistence`.
- Utility: `rust:scaffold` creates a new package in the agreed layout.

The tier applies only where a `Cargo.toml` or `.rs` file is present (`tiers/rust.json` `applies: stack-present`).

## Authoring and verification

```powershell
pwsh .agents/sync-generated.ps1
pwsh .agents/sync-generated.ps1 -Check
python -B -m unittest discover -s .agents/tests -p "test_*.py"
```

The layout, the vendored generator and CI come from [Template](https://github.com/tj-agents/template).

Push to `main`; sessions pick the change up when the plugin updates.
