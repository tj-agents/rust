---
name: direction
description: Where Tommy is headed with Rust — the goal, the skill tree he is working through, and the reference books every explanation and convention cites. Use when choosing or sequencing what to learn next, or when sourcing a Rust explanation or a proposed convention.
kind: knowledge
domain: rust
profile: knowledge
applicability: Rust projects and learning
requires: rust
provenance: house
---

# Where Tommy is headed with Rust

`rust:knowledge` tracks where he is now; this tracks where he is going.

## The goal

Write Rust himself, well, and own the standards he writes it by. Termboard is the vehicle: a deliberately
small terminal tool where each milestone teaches one slice of the language, and every convention in the
contract skills comes from a decision made while building it.

## The skill tree

| # | Area | Status |
|---|------|--------|
| 1 | Ownership, borrowing and lifetimes | not started |
| 2 | Structs, enums and pattern matching | not started |
| 3 | Errors: `Result`, `Option` and `?` | not started |
| 4 | Traits and generics | not started |
| 5 | Modules, crates and cargo workspaces | not started |
| 6 | Testing | not started |
| 7 | Tooling: cargo, rustfmt, clippy, rust-analyzer, debugger | not started |
| 8 | CLI and TUI crates | not started |
| 9 | Cross-platform: `cfg`, processes, Windows and Linux | not started |
| 10 | Async | later |

Update a row's status when he levels up an area.

## The rule

These projects are for learning, not output. A slower path where he understands it beats a fast one where
he does not. Check that it landed: ask him to explain it back, or to write the next piece before you show
yours.

## References

Explanations and conventions cite these:

- *The Rust Programming Language* (the Book) — fundamentals.
- *Rust API Guidelines* — naming and API shape.
- *Effective Rust* — idioms.
- *Rust for Rustaceans* — intermediate depth.
- *Zero To Production in Rust* — domain newtypes and application structure.
- Alexis King, "Parse, don't validate" — type-driven validation.
- The Clippy lint list and `rustc --explain`.
