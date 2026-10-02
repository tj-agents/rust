# rust

Read `README.md` and `SOURCE_LAYOUT.md` before changing repository structure.

Authored capabilities live once under `.agents/<kind>/<name>/SKILL.md`. `.agents/plugins/sources.json` owns the
source map and generated-root declaration. `.codex/skills/`, `.claude/skills/`, `.agents/INDEX.md`, both
marketplace bridges, and `plugins/*` are generated. Authored host manifests live under `.agents/plugins/manifests/`.
Run `pwsh .agents/sync-generated.ps1` after authored changes and require `pwsh .agents/sync-generated.ps1 -Check`
before delivery.

`knowledge` is Tommy's progress record: change it only under `learning`'s promotion rules. A `contract` skill
gains a rule only through `learning`'s convention procedure, after Tommy decides it.
