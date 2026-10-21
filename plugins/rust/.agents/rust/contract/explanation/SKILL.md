---
name: explanation
description: How Rust is quoted when explaining Rust code. Use when an explanation shows Rust source.
kind: contract
domain: rust
profile: explanation
applicability: Rust projects
requires: rust
provenance: house
---

# Explaining Rust code

Owns how Rust is quoted in an explanation.

Quote each file in its own top-level `rust` block, never indented inside a list item, under a
`path:line` line. Copy the code verbatim and replace `use` lists, derive and attribute noise,
error-conversion boilerplate and other lines the point does not need with `...`.

`src/card/service.rs:42`

````rust
...
pub fn finish_card(card: &mut Card) -> Result<(), FinishError> {
    card.status = Status::Done;
    ...
}
````
