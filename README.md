# rust

Rust learning companion and standards for Claude Code and Codex, published as `rust@tj-agents` (repository
marketplace `rust-agents`).

Knowledge tier, Tommy's personal Rust guide:

- `rust:learning` — learning and delivery modes, teaching rules, and how a convention is agreed.
- `rust:knowledge` — what Tommy has proven he knows in Rust.
- `rust:direction` — the goal, the skill tree and the references.

Contract tier, empty until a decision is recorded: `rust:style`, `rust:structure`, `rust:domain-design`,
`rust:errors`, `rust:testing`, `rust:build` and `rust:libraries`.

The tier applies only where a `Cargo.toml` or `.rs` file is present (`tier.json` `applies: stack-present`).

## Authoring and verification

```powershell
pwsh .agents/sync-generated.ps1
pwsh .agents/sync-generated.ps1 -Check
python -B -m unittest discover -s .agents/tests -p "test_*.py"
```

Push to `main`; sessions pick the change up when the plugin updates.
