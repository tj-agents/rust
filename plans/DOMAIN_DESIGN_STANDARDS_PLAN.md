# Rust domain design, structure and scaffold standards

Status: handed off 2026-10-03, not started.

## Objective

Research idiomatic Rust for domain modelling (DDD's tactical patterns) and project/file structure. Start from
Tommy's existing C++ and .NET domain-design standards and translate each principle into Rust, keeping what
carries over, changing what Rust does differently, and dropping what does not apply. Tommy decides every rule.
Record the agreed rules in this plugin's contract skills, give `rust:structure` a **File structure** section,
and add a `rust:scaffold` utility that creates a new project in that structure, as `gpp:scaffold` and
`msvc:scaffold` do for C++.

The standards stay Rust-generic: not tied to Termboard, a web API or a desktop app. Split guidance by project
type (for example a web-service addendum) only where the research shows materially different idioms, and only
after asking Tommy.

## Authorization

Tommy authorized (2026-10-03): the research; asking him questions whenever anything is unclear or a decision
is needed; recording the rules he decides in `tj-agents/rust`; the scaffold skill and its templates; extending
this repo's generator and tests as needed; regenerating, verifying, committing and pushing to `main` of
`tj-agents/rust`.

Not authorized: recording a rule Tommy has not decided; editing `rust:knowledge` (explaining is not him
knowing); editing Termboard, the C++/.NET standards or any other repository.

## Checkout and ownership

`C:\Users\TommySeery\source\repos\tj-agents\rust`, branch `main`. This session is the only writer here.
A parallel session is designing a shared template for all standards packages
(`~/.claude/plans/tj-agents/STANDARDS_TEMPLATE_PLAN.md`); it reads this repo but does not edit it. Do not edit
its files.

## Inputs

Read these as files. Do not invoke `cpp:*` or `dotnet:*` skills: the tier gate blocks them outside their
stacks.

- C++, in `~/source/repos/tj-agents/cpp` (checked out on `Feature/TierConventionsStructure`):
  `.agents/base/contract/{domain-design,mixins,structure,style,testing}/SKILL.md`, the scaffold skills
  `.agents/{gpp,msvc,win32}/utility/scaffold/` with their scripts and templates, and the reasoning in
  `plans/cpp-design/CPP_DESIGN_STANDARDS_PLAN.md` and `CPP_NAMING_STANDARD_PLAN.md`.
- .NET, in `~/source/repos/tj-agents/dotnet/.agents/contract/`: `ddd`, `value-semantics`, `keyed-unions`,
  `keyed-strategies`, `domain-events`, `result-carriers`, `result-errors`, `result-terminals`, `validation`,
  `module-structure`, `csharp-naming`, `dependency-injection`, `persistence`.
- This repo: `rust:learning` (the convention procedure and teaching rules), `rust:direction` (the reference
  list), the empty contract skills, `.agents/sync_generated.py`, and `~/source/repos/tj-agents/core/PACKAGING.md`
  (skill-local scripts and templates live beside their `SKILL.md` and must ship with the package). Today's
  generator copies only `SKILL.md` bodies, so the scaffold needs it extended.
- `~/source/repos/termboard/plans/ROADMAP.md`: the standards map and the candidate decisions (module
  namespacing such as `card::Title`, layout, clippy pedantic).

## Research already done (2026-10-03, verify rather than repeat)

- Inside a crate: a thin `main.rs` with logic in `lib.rs` (Book ch. 12). `foo.rs` plus `foo/` is the newer
  module style and `mod.rs` the older (Book ch. 7.5), but real codebases split: rust-analyzer, zed and helix
  barely use `mod.rs`; cargo, nushell, ruff and bevy use it heavily. Clippy `mod_module_files` and
  `self_named_module_files` enforce either style. matklad recommends one integration-test binary
  (`tests/it/main.rs`).
- Across crates: small projects are one package (bat, eza, Zero To Production). Medium projects are a root
  binary plus a few crates (ripgrep, cargo, nushell) or top-level `project-*` folders (helix, zellij, tokio).
  Large projects use a virtual root manifest with a flat `crates/*`, where the folder name equals the crate
  name (rust-analyzer, ruff, uv, zed; matklad's "Large Rust Workspaces"). Big projects split by subsystem,
  not by technical layer. A crate is the unit of parallel compilation, so a chain of layer crates builds
  serially (matklad's "Fast Rust Builds").
- DDD: the type-level half (newtypes, private fields with fallible constructors, data-carrying enums,
  invariants) is mainstream Rust under other names ("parse, don't validate", "make illegal states
  unrepresentable"). The layered half is a web-backend niche. The most-cited guide (howtocodeit, "Master
  Hexagonal Architecture in Rust", repo `howtocodeit/hexarch`) uses one crate with `domain/`, `inbound/` and
  `outbound/` modules, keeps the traits (ports) inside `domain/`, groups by concept, and calls it overkill
  for solo projects. Hyperswitch is the large production example, with domain-model, interface, storage and
  router crates. DDD crates are niche: `cqrs-es` gets about 25k downloads per 90 days against axum's 127M.
- Layer names: `domain` is the only near-universal one. GitHub code-search counts of Rust files declaring
  `pub mod X;`: `ports` ~4.8k, `application` ~4.0k, `adapters` ~3.9k, `infrastructure` ~2.4k,
  `presentation` ~1.3k, `outbound` ~1.2k, `inbound` ~1.1k. These are rough, and the words overlap with
  networking meanings. Tommy leans towards `domain` / `application` / `infrastructure` plus `cli`.

## Questions to settle with Tommy

1. Value objects: newtypes, private fields, `new`/`parse`/`TryFrom` constructors, derive policy, `Deref` or not.
2. Entities and identity: ID newtypes, equality, mutation only through methods.
3. Aggregates and invariants: consistency boundaries, private children, `&mut self` operations.
4. State and transitions: data-carrying enums against the typestate pattern; transitions returning `Result`.
5. Errors in the domain: per operation or per module, `thiserror`, crossing layers (shared with `rust:errors`).
6. Shared behaviour: traits, default methods, blanket impls (where C++ uses mixins and C# uses base classes).
7. Domain events: is there an idiomatic Rust equivalent, or does it not apply?
8. Ports: where traits live, generics against `dyn`, and when a trait earns its place.
9. File structure: one crate or a workspace and when to split; layer module names; grouping by concept; the
   `mod.rs` style; visibility (`pub(crate)`); re-exports; module namespacing and `module_name_repetitions`.
10. Naming: Rust API Guidelines (case, `as_`/`to_`/`into_`, `new`/`from`/`try_from`/`parse`) against
    `csharp-naming` and `cpp:style`.
11. Scaffold: what it generates (the agreed tree, toolchain pin, rustfmt, lints, CI, scripts), its options
    (binary, library, workspace), and its script language (C++ uses PowerShell for MSVC and sh for G++).

## Method

1. Read the inputs. Build a mapping table of every C++ and .NET principle to its Rust form (carries over,
   changes, or does not apply), each with a source.
2. Research from primary sources: the Book, the Rust API Guidelines, Effective Rust, Rust for Rustaceans,
   Zero To Production, "Parse, don't validate", the standard library's own APIs as precedent, real
   codebases checked with `gh api`, and the clippy lint list. Use standard web search first and extended
   when results are thin.
3. Keep findings and the mapping table in this file under `## Findings`.
4. Take decisions to Tommy in groups with AskUserQuestion: a recommended option first, alternatives,
   one-line sources. Teach any concept he needs in chat while doing it (`rust:learning`). Ask whenever
   anything is unclear.
5. Record each decided rule in its owning contract skill: the rule, one line of why, and the source. Keep
   skill text minimal, because every word costs tokens wherever it loads. Domain rules go in
   `rust:domain-design`, layout in a **File structure** section of `rust:structure`, errors in `rust:errors`,
   naming in `rust:style`.
6. Build `rust:scaffold` (`kind: utility`) with templates that produce exactly the recorded File structure,
   extending the generator and tests so skill-local files ship. Prove it by scaffolding a throwaway project in
   the scratchpad and running `cargo fmt --check`, `cargo clippy -- -D warnings` and `cargo test` on it.
7. Verify: `pwsh .agents/sync-generated.ps1 -Check`, `python -B -m unittest discover -s .agents/tests -p
   "test_*.py"`, and `python -B ../core/.agents/hooks/check_tier_payload.py --root .`. Commit and push to
   `main`. Update Progress below at each boundary.

## Completion

Done when the mapping table and findings are recorded here; every question above is decided by Tommy or
explicitly deferred by him; the agreed rules are in the contract skills; `rust:scaffold` exists and its output
passes the Rust gate; the checks are green; and the work is pushed. Finish by listing which Termboard roadmap
candidate decisions the new rules settle, so the Termboard owner can apply them.

## Progress

- 2026-10-03: plan written and handed off. Launched on `claude-opus-5-5`, chosen by Tommy (the lane
  ladder would put this design work at L1).

## Next Steps

1. Read this plan and every input listed above.
2. Do steps 1–3 of the Method, then start step 4 with Tommy.
