---
name: domain-design
description: Tommy's agreed Rust domain modelling — values, newtypes, entities, enums, state transitions and shared behaviour through traits. Read before writing or reviewing Rust that touches it; nothing applies until it is recorded here.
kind: contract
domain: rust
profile: contract
applicability: Rust projects
requires: rust
provenance: house
---

# Rust domain design

Owns how values, newtypes, entities, enums and state transitions are modelled, and how traits carry shared behaviour.

## Agreed

### Values

- An invariant-bearing value is a newtype with a private field, built only through a fallible associated
  function: `new -> Result<Self, XError>`, or a verb naming the work (`parse` for text, `decode` for bytes,
  `open` for a resource). `FromStr` and `TryFrom` are thin wrappers, added only when a caller needs them.
  Why: the invariant has one source of truth. Source: API Guidelines C-VALIDATE, C-CTOR; std `CString::new`.
- Read the inner value through a getter named for what it returns (`as_str`, `get`), `into_inner` to give up
  ownership, `AsRef` only for generic callers. Never `Deref`. Why: `Deref` leaks the inner type's whole API.
  Source: C-DEREF, C-CONV.
- Derive `Debug, Clone, PartialEq, Eq, Hash` on every value type; add `Copy` when it is small and owns no heap
  data, `PartialOrd, Ord` only when the order means something, `Default` only when a meaningful default
  exists. Why: other crates cannot add them later, and a derived `Default` can bypass `new`. Source:
  C-COMMON-TRAITS, Effective Rust Item 10.

### Entities

- Entity IDs share one generic `Id<T>`: a `u64` plus `PhantomData<fn() -> T>`, with `Debug`, `Clone`,
  `Copy`, `PartialEq`, `Eq` and `Hash` implemented by hand, since derive would bound `T`. An entity holds
  `Id<Self>`. Why: one definition, and IDs of different entities cannot be swapped. Source: `la_arena::Idx`,
  the Rustonomicon's `PhantomData` table.
- An entity has private fields and an `id()` getter. It does not implement `PartialEq`; compare
  `a.id() == b.id()`. Why: structural equality calls two states of one entity different. Source: std
  `PartialEq` docs (books equal by ISBN), C-STRUCT-PRIVATE.
