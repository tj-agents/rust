# rust

Rust learning companion and standards for Claude Code and Codex, published as `rust@tj-agents` (repository
marketplace `rust-agents`).

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

The layout, the vendored generator and CI come from [kit](https://github.com/tj-agents/kit).

Push to `main`; sessions pick the change up when the plugin updates.
