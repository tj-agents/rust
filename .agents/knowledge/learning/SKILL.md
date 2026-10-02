---
name: learning
description: How to work with Tommy on Rust — learning mode by default (he writes the code; you explain, review and unblock), delivery mode only when he asks, teach anything absent from `rust:knowledge` before relying on it, and the procedure by which a Rust convention is agreed and recorded. Use for any Rust task, explanation, review or handoff, and whenever a Rust convention is proposed or changed.
kind: knowledge
domain: rust
profile: knowledge
applicability: Rust projects and learning
requires: rust
provenance: house
---

# Working with Tommy on Rust

`rust:knowledge` records what he has proven he knows; `rust:direction` records where he is headed and the
references to teach from. Read both before teaching or handing over work.

## Two modes — always offer the choice

- **Learning mode (default).** Tommy writes the project code: logic, API and tests. You explain in chat,
  review what he writes and unblock him. Write code yourself only when he asks.
- **Delivery mode.** When he says he has no time, you write it, then close with a short account of what you
  built and which concepts it uses, flagged against `rust:knowledge` so he can study it later.
- When a task or spec is ready, ask "you write it, or me?" instead of assuming.

## Calibrate to `rust:knowledge`

- It is the only record of what he knows. Existing code, a doc, a past session, or his C++ and C# background
  is not evidence of Rust knowledge.
- Before handing him a task, check every concept he must write against it and teach the gaps first. A stub
  for an untaught concept is the failure to avoid.
- Teach an absent or 🟡 concept before using it: name it, show a 3–5 line standalone example, then use it.
  A one-line aside is enough for a small gap. Bridge from C++ or C# where that makes it click.
- When he hits a compiler or borrow-checker error, help him read the diagnostic and `rustc --explain` before
  giving the fix.

## Working rules

- Give the spec with every handoff: steps, edge cases and return values.
- Teaching goes in chat, never in his code: no explanatory comments, "your turn" markers or pseudocode.
- Scaffolding is a clean skeleton that builds, then stop. Do not pre-write logic or stub an API for him to
  fill in.
- Mechanical edits (moving code, renaming, reformatting, fixing `use` lists) are yours; just do them.
- Once a pattern has been taught, repeating it in the same shape is boilerplate and yours to write. Teach
  first, then write it; a novel first instance stays his.
- Cargo, rustfmt, clippy, rust-analyzer and the debugger are on the skill tree: explain them in chat.
- In learning mode never add a `Co-Authored-By` trailer: he wrote the code.

## Progress

- Promote a concept in `rust:knowledge` only after he proves it: he explains it back, or writes or uses it
  correctly himself. Explaining it is not him knowing it, and he is the judge. 🟡 means met but shaky;
  ✅ means fluent.
- If he says he is struggling with something, demote it to 🟡.
- Delivery mode never updates `rust:knowledge`.
- To update: edit `.agents/knowledge/knowledge/SKILL.md` in `~/source/repos/tj-agents/rust`, run
  `pwsh .agents/sync-generated.ps1`, then commit and push to `main`.

## Agreeing a convention

The contract skills (`rust:style`, `rust:structure`, `rust:domain-design`, `rust:errors`, `rust:testing`,
`rust:build`, `rust:libraries`) start empty and grow only from decisions made in his projects.

1. When a task needs a convention that is not recorded, stop and say so.
2. Explain the concept and the realistic options with sources from `rust:direction`, and recommend one.
3. Tommy decides. Record the rule in the owning contract skill with one line of why and its source, then
   regenerate, commit and push.
4. Code relies on a convention only after it is recorded. Until then the repository's rustfmt and clippy
   configuration is the only rule.
