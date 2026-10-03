---
name: errors
description: Tommy's agreed Rust error handling — Result and Option use, error types, propagation and panics. Read before writing or reviewing Rust that touches it; nothing applies until it is recorded here.
kind: contract
domain: rust
profile: core
applicability: Rust projects
requires: rust
provenance: house
---

# Rust errors

Owns `Result` and `Option` use, error types in libraries and at the binary edge, propagation, and when a panic is acceptable.

## Agreed

- Each fallible operation returns its own error enum, defined beside it and naming only the outcomes it can
  produce (`FinishError`, `TitleError`). Operations share one only when their outcomes are identical. Why:
  callers see exactly what can fail. Source: Sabrina Jewson, "Modular Errors in Rust"; std `ParseIntError`.
- Error types derive `thiserror::Error`; `anyhow` appears only at the binary's top level (`main`, command
  dispatch) to add context and report. Every error type is `Error + Send + Sync`, with a lowercase `Display`
  message and no trailing punctuation. Why: callers get a designed type; reporting stays at the edge. Source:
  the thiserror and anyhow READMEs, API Guidelines C-GOOD-ERR.
- A lower error crosses a layer inside a variant naming what failed, keeping the cause as `#[source]`, via
  `map_err`. Use `#[from]` only when a single call site can produce that source error. Why: a blanket `From`
  adds meaning implicitly and loses which call failed. Source: Jewson; thiserror docs.
- A failure a correct program can meet returns `Result`. A panic is only for a state that cannot occur
  unless the code is wrong, written `expect("why it cannot fail")` or `unreachable!("…")`. `clippy::unwrap_used`
  is denied, with `allow-unwrap-in-tests`. Why: the message records why the state is impossible. Source: the
  Book 9.3.
