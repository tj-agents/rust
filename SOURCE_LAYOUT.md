# Source ownership and generation

`.agents/` is the only authored home for host-neutral capabilities, laid out as `.agents/<kind>/<name>/SKILL.md`.
A definition contains the full instruction body and applicability metadata.

`.agents/plugins/manifests/` contains authored Codex and Claude manifest inputs. `.codex/` and `.claude/` contain
generated discovery entries only. `plugins/rust/` is a generated self-contained distribution; the two root
marketplace files and `.agents/INDEX.md` are generated too. Edit no generated body. Regenerate with
`pwsh .agents/sync-generated.ps1` and prove zero drift with `pwsh .agents/sync-generated.ps1 -Check`.
