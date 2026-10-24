# rust

Rust learning companion and standards for Claude Code and Codex, published as `rust@tj-agents` from the
`tj-agents` marketplace.

## Optional sibling capabilities

Select `tauri@tj-agents` for `tauri:structure` and `tauri:commands`; select `rust-sqlx@tj-agents`
for `rust-sqlx:persistence` and `rust-sqlx:migrations`. Both depend on Rust but not on each other,
React or a database engine. Explicit application composition chooses their combination. Tauri/SQLx
source evidence activates their routes; an ordinary Rust file does not activate either framework.
SQLite-specific guidance is labelled; generic Rust contracts retain their existing scope and decisions.
Testing/packaging capabilities are added when those stages are entered, without placeholder families.

## Skills

- Knowledge: `rust:learning` (learning and delivery modes, teaching rules, and how a convention is agreed),
  `rust:knowledge` (what Tommy has proven he knows), `rust:direction` (the goal, the skill tree and the
  references).
- Core contracts, each rule recorded only after Tommy decides it: `rust:style`, `rust:structure`,
  `rust:domain-design`, `rust:errors`, `rust:testing`, `rust:build` and `rust:libraries`.
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
