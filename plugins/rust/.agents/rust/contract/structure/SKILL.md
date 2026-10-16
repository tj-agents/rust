---
name: structure
description: Tommy's agreed Rust project structure — workspace and crate layout, module tree, visibility and wiring. Read before writing or reviewing Rust that touches it; nothing applies until it is recorded here.
kind: contract
domain: rust
profile: core
applicability: Rust projects
requires: rust
provenance: house
---

# Rust structure

Owns workspace and crate layout, the module tree, visibility, and where dependencies are wired.

## File structure

```text
Cargo.toml
src/
  lib.rs          # declares the modules
  main.rs         # thin entry point: reads input and the clock, wires adapters, calls the domain
  domain.rs
  domain/
    id.rs         # Id<T>
    card.rs       # an area's model: Card, Title, Status, CardEvent
    card/
      ports.rs    # traits the area's use cases need
      service.rs  # the area's use cases
  cli.rs          # adapters, each named for what it adapts
  sqlite.rs
tests/
  it/
    main.rs       # the one integration-test binary (rust:testing)
```

Split for a concrete reason, the package becomes a workspace:

```text
Cargo.toml        # [workspace] only
crates/
  termboard/      # the binary
  board/          # a subsystem crate, folder named as the crate
```

## Agreed

- One package: logic in `lib.rs`, a thin `main.rs`. Split into a workspace only for a concrete reason (compile
  parallelism, isolating a heavy dependency, a second binary, publishing), by subsystem, never by layer. Why:
  a crate is the compile unit, and a layer chain builds serially. Source: the Book ch. 12; matklad, "Fast Rust
  Builds".
- Workspace crates sit flat in `crates/<crate-name>/`, each folder named exactly as its crate; only published
  crates take the project prefix. Why: Cargo's crate namespace is flat, and a folder tree drifts from it.
  Source: matklad, "Large Rust Workspaces"; rust-analyzer, zed.
- A crate with I/O boundaries has a `domain` module whose areas hold their model, port traits (`ports.rs`)
  and use cases (`service.rs`). Adapters are top-level modules named for what they adapt (`cli`, `sqlite`,
  `terminal`), never `application` or `infrastructure`. A pure library groups by concept. Why: `domain` is
  the one Rust layer word; everything else is named for what it is. Source: Zero To Production; How To Code
  It hexarch.
- Shared domain vocabulary is a domain module named for its concept (`domain::id`), never a `shared` or
  `common` bucket. Why: a bucket name says nothing about what it holds. Source: house, by the rule above.
- A module with children is `foo.rs` plus `foo/`, enforced by clippy `mod_module_files`. Why: every file is
  named for the module it holds. Source: the Book 7.5.
- Items are private by default, `pub(crate)` for sharing inside the crate, `pub` only for exported API, with
  rustc `unreachable_pub = "warn"`. Why: `pub` then means exported. Source: Effective Rust Item 22; matklad.
- An application gives each item one path, so it re-exports nothing. A library may `pub use` its API at the
  crate root and re-exports dependency types its API exposes. No glob imports except `use super::*` in test
  modules. Why: two paths to one item drift apart. Source: rust-analyzer style guide; the Book 7.4; Effective
  Rust Items 23–24.
- `main` (or one `run` function it calls) is the composition root: it reads input, configuration and the
  clock, constructs the adapters and passes them to the domain by reference or generic parameter. No
  dependency-injection container. Why: the compiler checks the wiring. Source: How To Code It hexarch.
- Adapters own their wire and row types and convert them into domain types with `TryFrom` or `From` at the
  edge; domain types derive no serde traits. Why: wire, storage and model evolve separately. Source: Zero To
  Production ch. 6; hexarch.
