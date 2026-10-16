---
name: scaffold
description: Create a new Rust package in the agreed `rust:structure` layout — a thin binary over a library, or a library alone — with the toolchain pin, lints, rustfmt, clippy, CI and agent files the Rust standards expect. Use when starting a Rust project; never run it over an existing tree.
kind: utility
domain: rust
profile: scaffold
applicability: new Rust projects
requires: rust
provenance: house
---

# Rust project scaffold

Creates a clean skeleton that passes the Rust gate, then stops: no sample logic and no empty modules
(`rust:learning`). `rust:structure` owns the layout it grows into.

## Create a project

```text
python -B <skill-directory>/scripts/new_rust_project.py --name my_tool --destination ~/source/repos
```

- The result is `<destination>/<name>`. The destination must exist and the project must not. `--dry-run` lists
  the files without writing. There is no overwrite mode and no `git init`.
- Default: an application, an empty `src/lib.rs` and `fn main() {}` in `src/main.rs`, pinned to an exact
  toolchain that rustup installs on first use.
- `--lib --description "…"`: a library. It tracks `stable`, documents its crate root and enables
  `missing_docs`.
- `--toolchain X.Y.Z` sets the version, otherwise the installed `rustc +stable`. Both kinds set `rust-version`
  to its minor (`rust:build`).

Requires Python 3.9+, and rustup when `--toolchain` is omitted.

The tier gate blocks `rust:*` where no `Cargo.toml` or `.rs` file exists, including an empty destination;
set `AGENTS_TIER_OVERRIDE=rust` for that session.

## Build and adapt

The project gets `Cargo.toml` with the agreed lints, `rust-toolchain.toml`, `rustfmt.toml`, `clippy.toml`,
`.gitattributes`, `.gitignore`, a Windows and Ubuntu CI workflow, and an `AGENTS.md`/`CLAUDE.md` pair. Templates
live in `templates/` beside this file and ship with the skill. Change them there, then regenerate.

## Validation and publication

```text
cargo fmt --all --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
```
