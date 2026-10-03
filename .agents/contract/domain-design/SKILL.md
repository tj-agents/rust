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

### Aggregates

- The root owns its children by value in private fields and exposes them read-only (`&[T]` or an iterator).
  Every change that can break an invariant is a `&mut self -> Result` method on the root. Other aggregates
  are held as `Id<T>`; no `Rc` or `RefCell` inside. Why: only the root can enforce a rule spanning its
  children. Source: the Book 18.1 (`AveragedCollection`) and 15.6.

### State

- Lifecycle state is a data-carrying enum field whose variants hold only their own data. Transitions are
  `&mut self -> Result<(), XError>` methods that match the current variant. Typestate is only for builders
  and protocols driven within one scope. Why: stored state is a runtime value, and the enum makes invalid
  combinations unrepresentable. Source: kornel on users.rust-lang.org, Cliffle's typestate post.

### Shared behaviour

- Accept a capability through generics (`impl Trait`, `<T: Trait>`); use `dyn Trait` only for a mixed
  collection or to erase a type at a boundary. Share behaviour through small traits with default methods, and
  add methods to a foreign type with an extension trait named `FooExt`. Why: generics inline and allocate
  nothing, and Rust has no inheritance. Source: Effective Rust Items 12–13, the Book 18.1–18.2, RFC 445.
- A port trait exists only for an external boundary (storage, terminal, network) or several real
  implementations, never only to mock. Values such as the current time are read at the entry point and
  passed in; tests use real adapters or in-memory fakes. Why: a core that takes data needs no mocks. Source:
  matklad, "How to Test"; the faux README.

### Domain events

- Only a state change another module or a published contract reacts to raises a domain event. An
  intent-named method pushes it onto the entity's private event buffer; the repository's `save`, the
  aggregate's only write path, drains the buffer into the outbox inside its transaction. Why: dispatch cannot
  be forgotten and composes across nested methods, with no ORM hook to do it. Source: house decision,
  mirroring the .NET `domain-events` contract.
