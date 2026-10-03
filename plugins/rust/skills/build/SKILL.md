---
name: build
description: Tommy's agreed Rust build — toolchain pin, edition, cargo profiles and features, the verification gate and CI. Read before writing or reviewing Rust that touches it; nothing applies until it is recorded here.
kind: contract
domain: rust
profile: contract
applicability: Rust projects
requires: rust
provenance: house
---

# Rust build

Owns the toolchain pin, edition, cargo profiles and features, the fmt, clippy and test gate, and CI.

## Agreed

- Edition 2024. An application pins an exact toolchain in `rust-toolchain.toml` (`clippy` and `rustfmt`,
  profile `minimal`); a library tracks `channel = "stable"`. Both set `rust-version` to the minor they target.
  Source: ruff, uv and zed pin exactly; tokio and bevy track stable.
- The gate runs locally and in CI on Windows and Ubuntu: `cargo fmt --all --check`, `cargo clippy --workspace
  --all-targets --all-features -- -D warnings` and `cargo test --workspace --all-features`. Source: house,
  per `rust:style`'s lint level.
- Crates forbid `unsafe_code`. Source: house.
- A new project starts from `rust:scaffold`. Source: house.
