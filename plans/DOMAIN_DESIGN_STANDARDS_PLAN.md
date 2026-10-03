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

## Findings

### Mapping table: C++ and .NET principles to Rust

Verdict: **carries** (same rule, Rust spelling), **changes** (Rust does it differently), **enforced** (the
compiler or clippy already guarantees it, so the rule shrinks to a reminder or disappears), **n/a** (does not
apply). `Q` is the open question in the list above that decides it. Sources: `cpp:` =
`tj-agents/cpp/.agents/base/contract/<skill>`, `net:` = `tj-agents/dotnet/.agents/contract/<skill>`.

| # | Principle (source) | Rust form | Verdict | Q |
|---|---|---|---|---|
| 1 | No domain layer just because the skill loaded; start from the problem's vocabulary (cpp:domain-design) | Same | carries | 9 |
| 2 | Passive record (public fields) vs invariant-bearing value (controlled construction) vs entity vs stateful adapter (cpp:domain-design) | pub-field struct; private-field struct or tuple newtype with a fallible associated fn; entity struct with an ID; adapter owning a resource with `Drop` | changes: no `struct`/`class` split, visibility is per field | 1 |
| 3 | Privacy protects an invariant at the type (cpp, C#) | Privacy is per **module**: any code in the same module can touch private fields, so the invariant holds only against code outside it | changes | 1, 9 |
| 4 | A value stays valid through construction, assignment and moves; specify a moved-from state (cpp:domain-design) | Moves are bitwise and the source becomes unusable; no moved-from state exists | enforced | — |
| 5 | Validation doesn't turn a record into a valid value (cpp:domain-design) | "Parse, don't validate": parse the raw input into a different, valid type | carries, stronger | 1 |
| 6 | DDD roles are vocabulary, not base classes, suffixes or folders (cpp:domain-design, net:ddd) | Same; Rust has no inheritance to tempt it | carries | — |
| 7 | Entity equality means same identity; don't default all-field equality without deciding (cpp:domain-design, net:ddd) | `#[derive(PartialEq)]` is all-field; decide whether an entity derives it, compares by ID, or has neither | carries | 2 |
| 8 | Aggregate = consistency boundary; children reached only through the root (net:ddd) | Owned children in private fields, `&mut self` operations; the borrow checker stops outside references | carries, partly enforced | 3 |
| 9 | Reference another aggregate by its ID, never a navigation property (net:ddd, net:module-structure) | ID newtypes; shared object graphs (`Rc<RefCell<_>>`) are unidiomatic, so ID references are the natural form | carries | 2, 3 |
| 10 | Put an invariant on the aggregate that owns every field it constrains; anemic model and God aggregate are anti-patterns (net:ddd) | Same | carries | 3 |
| 11 | Operations live with their owning type: instance methods and type-owned static functions; free functions for peer algorithms (cpp:domain-design house choice, net:csharp-naming evaluators) | Inherent `impl` methods and associated functions (`Title::parse`); free functions in the concept's module for peer algorithms | carries | 1, 6 |
| 12 | Validation and decoding sit on the type with its errors beside it; no generic `validation`/`errors` module (cpp:domain-design) | `Title::parse` / `FromStr` / `TryFrom` in the type's module; `TitleError` in the same module | carries | 1, 5 |
| 13 | Returned value owns its data unless the API promises a view with a documented lifetime (cpp:domain-design) | Owned vs borrowed is explicit (`String` vs `&'a str`) and lifetime-checked | enforced | 1 |
| 14 | Expose a separate `validate` only when callers need it (cpp:domain-design) | Same | carries | 1 |
| 15 | Binary/ABI records get size and offset assertions (cpp:domain-design, cpp:style) | `#[repr(C)]` plus `const _: () = assert!(size_of::<T>() == N)`; only FFI or wire work | n/a for generic standards | — |
| 16 | Fallible construction: `create`, or a specific verb `parse`/`decode`/`open`; no two-stage init or public default (cpp:domain-design) | No constructors; `new` is the convention for the primary one; fallible spellings `new -> Result`, `parse`, `try_new`, `TryFrom`, `FromStr`; `Default` only when derived or implemented | changes | 1, 10 |
| 17 | Immutable transformations named for meaning; `with_x` optional (cpp:domain-design) | Methods taking `self` or `&self` and returning a new value; `with_*` in Rust usually means a constructor variant (`Vec::with_capacity`) | changes | 10 |
| 18 | Mutable values are allowed; avoid `const` members (cpp:domain-design); value objects replaced, not mutated (net:ddd) | Mutability is per binding and per borrow (`let mut`, `&mut self`), not per type | changes, simpler | 1 |
| 19 | Decisions separate from effects; read the clock at the boundary and pass the instant in; an entity never holds a clock (cpp:domain-design, net:module-structure) | Same: pass `now` as a value | carries | 8 |
| 20 | Coarse boundaries; no service class per function or interface for a trivial operation (cpp:domain-design) | A trait only when it earns its place | carries | 8 |
| 21 | Expected failure is a typed result; closed enum or small struct error; never `bool`, strings or asserts (cpp:domain-design, net:result-carriers) | `Result<T, E>`, error enum or struct | carries, native | 5 |
| 22 | Smallest truthful carrier: Result, unit Result, Option, `Result<Option<T>, E>`, empty collection for none, set for uniqueness, `bool` only for predicates (net:result-carriers) | `Result<T, E>`, `Result<(), E>`, `Option<T>`, `Result<Option<T>, E>`, `Vec`, `HashSet`/`BTreeSet`, `bool` | carries, native | 5 |
| 23 | Programmer errors and violated invariants stay exceptions (net:result-carriers); `expected` doesn't make a call non-throwing (cpp:domain-design) | `panic!` for bugs; panics still possible inside `Result`-returning code | changes | 5 |
| 24 | Never introduce another Result/Option library (net:result-carriers) | std `Result`/`Option` only | carries | 5 |
| 25 | Result/Option never in wire, persistence or event DTOs (net:result-carriers) | `Option<T>` is the idiomatic optional field in a serde DTO; `Result` stays out | changes | 9 |
| 26 | Every error type is a closed operation-owned union; every outcome a named case; no shared catalog (net:result-errors) | Error enum per operation vs one per module or crate | carries or changes | 5 |
| 27 | Error placed beside its operation at its widest caller (net:result-errors) | Same | carries | 5 |
| 28 | Exhaustive switch, no discard arm (net:result-errors, net:keyed-unions) | `match` is exhaustive; avoid `_` on your own enums (clippy `wildcard_enum_match_arm`, restriction) | enforced | 4 |
| 29 | Never discard a returned result (net:result-carriers) | `Result` is `#[must_use]`; rustc warns | enforced | — |
| 30 | Case name agrees with its semantic kind (net:result-errors) | Same | carries | 5 |
| 31 | Validation accumulates independent field errors, then fail-fast (net:validation) | `?` is fail-fast; accumulation is a hand-collected `Vec` or a crate | changes | 5 |
| 32 | Map validation into the operation's own error, once (net:validation) | `map_err` or a `From` impl at the owning boundary | carries | 5 |
| 33 | Keyed union when variants differ in signature; strategy when they share one interface (net:keyed-unions, net:keyed-strategies) | Data-carrying `enum` vs a trait with several impls | carries, native | 4, 6 |
| 34 | Arms carry real payloads: no marker arms, no nullable stand-ins, no parameter object unifying arms (net:keyed-unions) | Same | carries | 4 |
| 35 | Adding a key fails composition, not production (net:keyed-unions) | Exhaustive `match` fails compilation | enforced | 4 |
| 36 | Data every case carries lives outside the union (net:keyed-unions) | A struct with common fields plus a `kind` enum | carries | 4 |
| 37 | Factory, resolver, keyed DI registration, no service location (net:keyed-strategies) | No DI container | n/a | 8 |
| 38 | Raise domain events on the entity; save dispatches them pre/post commit (net:domain-events) | No ORM interceptor; return events from the method, or not at all | changes or n/a | 7 |
| 39 | Mixins only for mechanical composition; prefer members and free functions (cpp:mixins) | No inheritance; traits with default methods, blanket impls, composition through fields | changes | 6 |
| 40 | Name the behaviour, not the mechanism; `-able` selectively (cpp:mixins, net:csharp-naming) | Trait names are capabilities (`Read`, `Display`, `Iterator`) | carries | 6, 10 |
| 41 | No mechanism-named folders (`mixins/`) (cpp:mixins) | No `traits/` folder | carries | 9 |
| 42 | `detail/` marks unsupported API but isn't access control (cpp:mixins) | Real access control (`pub(crate)`, private modules); `#[doc(hidden)]` for semver-exempt public items | changes | 9 |
| 43 | Contain macros (cpp:mixins) | `macro_rules!` scoping | n/a | — |
| 44 | Thin `app/`, logic in libraries (cpp:structure) | Thin `main.rs`, logic in `lib.rs` | carries | 9 |
| 45 | A single library stays at the root; `libs/<name>/` only for several (cpp:structure) | One package at the root; `crates/<name>/` only for several | carries | 9 |
| 46 | New library target when it gives a cohesive API, dependency control or independent testing; no empty directories (cpp:structure) | New crate for compile parallelism, dependency isolation, separate publishing or proc-macros | carries, Rust reasons | 9 |
| 47 | Preserve product boundaries (`client/`, `driver/`, `shared/`) (cpp:structure) | Workspace members | carries | 9 |
| 48 | A `domain` folder only when a distinct model needs that boundary (cpp:structure) | Same | carries | 9 |
| 49 | Folders and namespaces need not mirror each other (cpp:structure, cpp:style) | The module tree **is** the file tree; `pub use` re-exports let the public paths differ | changes | 9 |
| 50 | Layers Contracts/Domain/Application/Infrastructure/Api, arrows inward (net:module-structure) | Modules in one crate (convention only) or crates (compiler-enforced, but serial builds) | changes | 9 |
| 51 | Visibility cascade: public contracts, internal elsewhere, `InternalsVisibleTo` for tests (net:module-structure) | `pub`, `pub(crate)`, private; an in-file `#[cfg(test)]` module sees private items | changes | 9 |
| 52 | No cross-module queries; talk through a facade or event; primitive foreign keys (net:module-structure) | Same between subsystems | carries | 9 |
| 53 | Preserve the repository's established shape (cpp:structure) | Same | carries | 9 |
| 54 | Snake/Pascal case; trailing underscore on private members (cpp:style) | rustc enforces `snake_case`, `UpperCamelCase`, `SCREAMING_SNAKE_CASE`; no field prefix | enforced | 10 |
| 55 | Semantic type names; no `Record`/`Data`/`Info`/`Model`/`Fact` suffixes (cpp:style, net:csharp-naming) | Same | carries | 10 |
| 56 | Same concept keeps the same word; suffix from the type's shape (net:csharp-naming) | Same; `Builder` is idiomatic Rust (C-BUILDER); `Helper`/`Utility` disappear into module functions | carries | 10 |
| 57 | Interface and implementation share a name apart from `I` (net:csharp-naming) | No `I` prefix: trait for the capability (`CardStore`), impl for what it is (`SqliteCardStore`) | changes | 8, 10 |
| 58 | Type-to-type mapping in an `XMappers` class (net:csharp-naming) | `impl From<Row> for Card` | changes | 9 |
| 59 | Receiver-owned behaviour is an extension; peer decisions a named evaluator (net:csharp-naming) | Inherent method, or an extension trait (`FooExt`) on a foreign type; free function for peers | carries | 6 |
| 60 | Project namespace, nested only for meaningful boundaries; don't repeat the namespace in names (cpp:style) | Module-qualified names (`card::Title`, as `io::Error`); `module_name_repetitions` | carries | 9, 10 |
| 61 | Named constants at the narrowest boundary (cpp:style) | `const` in a fn, an `impl` or a module | carries | 10 |
| 62 | `{}` initialisation, brace omission, anonymous namespaces, `std::uintN_t` (cpp:style) | Not applicable or rustc-enforced | n/a | — |
| 63 | `///` API docs on public items; don't restate names (cpp:style) | rustdoc `///` and `//!`; `# Errors` and `# Panics` sections (clippy pedantic checks them) | carries | 10 |
| 64 | Lint triage: fix, or disable with a reason; the compiler wins (cpp:style) | `#[expect(clippy::x, reason = "…")]`; workspace `[lints]` | carries | 11 |
| 65 | Test the real target; no parallel copy of sources; no test-only production APIs (cpp:testing) | `#[cfg(test)] mod tests` beside the code has private access; `tests/` uses the public API | changes | testing |
| 66 | Honest tiers: unit tests touch no fs, network or process (cpp:testing) | Same | carries | testing |
| 67 | Inject interfaces; register in the composition root; no service locator (net:dependency-injection) | Wiring in `main` (or one `app` function); generics or `Box<dyn>`/`Arc<dyn>`; no container | changes | 8 |
| 68 | Third-party SDKs behind an adapter (net:dependency-injection) | Same | carries | 8 |
| 69 | Repository per entity; never leak `IQueryable`; unit of work, EF contexts (net:persistence) | A repository returns domain types, never rows or query builders; the rest is EF-specific | mostly n/a | 8 |
| 70 | One shared result carrier and error union contract test per union (net:result-errors) | Unit test over each error's `Display`/variant mapping where it is a contract | changes | testing |

Rust-only topics with no C++/.NET counterpart, to take to Tommy inside the questions above: `Copy` vs `Clone`
(Q1), `#[non_exhaustive]` (Q5, for published crates only), `#[must_use]` on pure functions (Q10), lifetimes in
domain types (prefer owned, Q1), the orphan rule for trait impls (Q6), and whether domain types derive serde
traits or stay separate from DTOs (Q9).

### Research: domain idioms (Q1–Q4, Q6), primary sources opened 2026-10-03

- Newtypes and validation: API Guidelines C-NEWTYPE, C-CUSTOM-TYPE ("convey interpretation and invariants"
  through a deliberate type), C-VALIDATE (static first, then `Result`/`Option`, opt-outs suffixed
  `_unchecked`), C-STRUCT-PRIVATE (public fields only for "compound, passive data structures"). Effective Rust
  Item 1 ("make invalid states inexpressible"), Item 6 (newtype), Item 22 ("Minimize visibility").
- Construction: C-CTOR says `new` is the primary constructor, `from_*` may take extra arguments, secondary
  ones are `with_foo`; it says nothing about fallible construction. Std's fallible primaries are `new`
  returning `Option`/`Result` (`NonZero::new`, `CString::new`) or `from_*` returning `Result`
  (`String::from_utf8`, `Layout::from_size_align`). `try_` marks a checked sibling of a panicking function
  (`Duration::try_from_secs_f64`); `try_new` exists in std only as nightly `Box::try_new` (arrow and nutype
  use it). `FromStr` is reached through `str::parse`.
- Zero To Production ch. 6: `pub struct SubscriberName(String)` with `parse(String) -> Result`, exposed via
  `AsRef<str>`; a later chapter adds `TryFrom<FormData>` that calls `parse`. How To Code It (newtypes guide):
  the constructor is the source of truth; `TryFrom` is a thin call to it; treat `Deref` "like … disarming a
  very small bomb".
- Conversions (C-CONV-TRAITS, Effective Rust Item 5): implement `From`/`TryFrom`/`AsRef`, never `Into`.
  `Deref` only for smart pointers (C-DEREF; rust-unofficial "Deref polymorphism" anti-pattern). nutype offers
  a `Deref` derive, so this is not unanimous.
- Common traits (C-COMMON-TRAITS, Effective Rust Item 10): implement std traits eagerly because of the orphan
  rule; `Eq` with every `PartialEq`; derive `Debug` broadly.
- Entities: std's `PartialEq` docs show identity equality (two books are the same if ISBNs match); `Hash` must
  agree with `Eq`. How To Code It's hexarch derives full structural equality on `Author` with a raw `Uuid`
  id. No authoritative Rust source mandates either.
- Aggregates: the Book 18.1 `AveragedCollection` (private fields kept in sync by `&mut self` methods); Book
  15.6 (a parent owns its children; back-references are `Weak`). How To Code It: a domain type holds "all
  entities that must change together as part of a single, atomic operation", even across several SQL tables.
- State: Cliffle "The Typestate Pattern in Rust" (state in the compile-time type, transitions consume `self`;
  rustdoc gets "harder to follow"). The Book 18.3 shows the same trade-off. kornel (users.rust-lang.org):
  run-time state needs an `enum`; doing both means "implementing everything almost twice".
- Shared behaviour: Book 18.1 ("If a language must have inheritance to be object oriented, then Rust is not
  such a language"; reuse via default trait methods). Effective Rust Item 12 (prefer generics to trait
  objects), Item 13 (default methods: minimal implementor surface, rich user surface). RFC 445: extension
  traits are named `FooExt`. C-SEALED: a private `Sealed` supertrait stops downstream impls.

### Research: errors, events and ports (Q5, Q7, Q8), primary sources opened 2026-10-03

- Error granularity: Sabrina Jewson, "Modular Errors in Rust" (2023): "error types should be located near to
  their unit of fallibility", which is the operation; a crate-wide enum loses context and "ties the crate
  together in a big knot"; verbosity is the main cost. Std has both: per-operation `ParseIntError`,
  `FromUtf8Error`; module-wide `io::Error` with a `kind()`. Palmieri ("Error Handling In Rust – A Deep
  Dive"): use an enum if the caller behaves differently per failure, otherwise an opaque error; avoid "Ball
  Of Mud" enums; log errors where they are handled.
- thiserror (2.0.21) and anyhow (1.0.104) READMEs: thiserror when you design the error type the caller
  receives ("most often … library-like code"), anyhow when you don't care which error a function returns
  ("application-like code"). Thiserror "does not appear in your public API".
- C-GOOD-ERR: implement `std::error::Error`, `Send` and `Sync`; `Display` "lowercase without trailing
  punctuation, and typically concise".
- Crossing layers: `?` applies `From` (Effective Rust Items 3, 4). thiserror `#[from]` implies `#[source]`
  and allows no other fields. Jewson: don't implement `From<io::Error>` because it "would implicitly add
  meaning"; wrap with `map_err` into a context-carrying variant.
- Panic vs Result (Book 9.3): `Result` is the default for anything that can fail; panic on a contract
  violation, which "always indicates a caller-side bug"; the `Guess` newtype puts validation in the
  constructor.
- Domain events: cqrs-es (`Aggregate::handle` emits events, `apply` mutates; ~25k recent downloads),
  disintegrate and fmodel-rust are event-sourcing crates and niche. Chassaing's Decider (`decide(command,
  state) -> events`, `evolve(state, event) -> state`) works without event sourcing; fmodel-rust has a
  state-stored aggregate. No verifiable Rust precedent for the .NET shape (the entity collects events and an
  ORM hook dispatches them on save); nothing in Rust would run that hook.
- Ports: Effective Rust Item 12 and Book 18.2 prefer generics; `dyn` for heterogeneous collections or type
  erasure. How To Code It hexarch: ports are traits in `domain/<area>/ports.rs`, used as generics bounded
  `Send + Sync + Clone + 'static`; one error type per operation with an `Unknown(anyhow::Error)` catch-all;
  "Apps that don't have any business logic don't need ports and adapters"; it slows you down when you can
  keep the codebase in your head. faux: single-implementation traits are "an undue burden"; mockall can mock
  structs. matklad, "How to Test": think in data, "let the caller do input and output, and let the callee do
  compute".
- Async traits: `async fn` in traits is stable since 1.75 but not dyn-compatible; a 2026 project goal has only
  a nightly preview. Generic async ports work natively; `Arc<dyn Port>` still needs `async-trait` or boxing.

### Research: structure, naming and tooling (Q9–Q11), primary sources opened 2026-10-03

- Clippy groups (clippy source and CHANGELOG): `module_name_repetitions` moved from pedantic to
  **restriction** in Rust 1.84, so it must be enabled by name. `mod_module_files` (bans `mod.rs`) and
  `self_named_module_files` (bans `foo.rs` + `foo/`) are restriction; cargo enforces `mod.rs` with the
  latter. `inline_modules` (restriction, 1.97) bans inline `mod x {}` except `#[cfg(test)]`.
  `module_inception` is style. Pedantic: `must_use_candidate`, `missing_errors_doc`, `missing_panics_doc`,
  `wildcard_imports`, `enum_glob_use`. `redundant_pub_crate` (nursery) conflicts with rustc's allow-by-default
  `unreachable_pub` (clippy #5369 open).
- Pedantic adoption: ruff and uv enable `pedantic` at warn with an allow-list (`missing_errors_doc`,
  `missing_panics_doc`, `must_use_candidate`, `similar_names`, `too_many_lines`, `match_same_arms`,
  `map_unwrap_or`, …) and warn on `unreachable_pub`. cargo, rust-analyzer, ripgrep, nushell, helix, zed,
  bevy and tokio do not enable the group (bevy cherry-picks; rust-analyzer and tokio warn on
  `unreachable_pub`).
- Naming (API Guidelines): C-CASE (acronyms are one word: `Uuid`); C-CONV (`as_` free borrow, `to_`
  expensive, `into_` consumes; wrappers expose `into_inner`); C-GETTER (no `get_` prefix; `get` only when
  one obvious thing is gotten); C-ITER; C-WORD-ORDER (`ParseAddrError`, verb-object-error, consistency
  matters more than the order); C-CTOR (`new` primary, `with_*` secondary, `from_*` conversion; `new` and
  `Default` must agree).
- Visibility: Effective Rust Item 22 (as little as possible; `pub(crate)` for crate-wide helpers), Item 23
  (avoid wildcard imports except `use super::*` in tests), Item 24 (re-export dependencies in your API).
  matklad recommends `unreachable_pub` so that `pub` means exported API. rust-analyzer's style guide: avoid
  re-exports in non-library code ("two ways to use something") and local `use MyEnum::*`.
- Module namespacing: RFC 356 ("items exported from a module should *never* be prefixed with that module
  name… `io::Error`"). The Book 7.4 idiom: import a function's parent module, import structs and enums by
  full path unless names collide (`fmt::Result`), and "There's no strong reason behind this idiom".
  rust-analyzer qualifies layer items (`hir::`, `ast::`) to make the layer clear.
- Tooling: stable is **1.99.0** (2026-10-01); local toolchain is 1.97.1. Edition 2024 is the default for
  `cargo new`; resolver `"3"` is its default (MSRV-aware) and must be explicit in a virtual workspace.
  `[lints]`/`[workspace.lints]` since 1.74. `build.warnings`/`CARGO_BUILD_WARNINGS=deny` since 1.97 (ruff CI
  uses it). Applications pin an exact toolchain (ruff, uv 1.99.0; zed 1.98.1); libraries such as tokio and
  bevy don't. `rust-version` is the MSRV. `cargo new` makes a bin, `git init`s, `.gitignore` = `/target`.
  `tests/it/main.rs` needs no Cargo config. CI: `dtolnay/rust-toolchain`, `Swatinem/rust-cache@v2`.
- Layer folders: hexarch (`3-simple-service` branch) uses `src/lib/{domain,inbound,outbound}` with
  `domain/blog/{models,ports,service}` and the `foo.rs` + `foo/` style. `mod domain;` is common (~15k code
  hits), `application` (~7.8k, often GTK's `Application`) and `infrastructure` (~3.8k) much less; none of
  the notable projects above use these layer names.

## Decisions

Tommy's decisions, recorded in the contract skills as they are made.

- 2026-10-03, Q1 value objects: construction `new -> Result` by default, a verb that names the work when
  apt (`parse`, `decode`, `open`), `FromStr`/`TryFrom` only as thin wrappers; read through a named getter
  (`as_str`, `get`, `into_inner`, `AsRef` where generic code needs it), never `Deref`; derive the eager set
  `Debug, Clone, PartialEq, Eq, Hash`, plus `Copy` when small and heap-free, `PartialOrd, Ord` only for a
  meaningful order, `Default` only for a meaningful default. → `rust:domain-design`.
- 2026-10-03, Q2 entities: private fields, `id()` getter, no `PartialEq` on the entity; compare IDs
  explicitly. IDs: Tommy challenged a newtype per entity ("surely define a struct of a reusable id"), so one
  generic `Id<T>` (`u64` + `PhantomData<fn() -> T>`, hand-written trait impls), entity holds `Id<Self>`.
  Where `Id<T>` lives is a Q9 structure decision. → `rust:domain-design`.
- 2026-10-03, Q3 aggregates: root owns children privately, read-only out, invariant changes are `&mut self
  -> Result` root methods, other aggregates by `Id<T>`, no `Rc`/`RefCell`. → `rust:domain-design`.
- 2026-10-03, Q4 state: data-carrying enum field, `&mut self -> Result` transitions; typestate only for
  builders and in-scope protocols. → `rust:domain-design`.
- 2026-10-03, Q6 shared behaviour (also settles Q8's generics-vs-`dyn` half): generics by default, `dyn`
  for mixed collections or type erasure; small traits with default methods; `FooExt` extension traits.
  → `rust:domain-design`.
- 2026-10-03, Q7 domain events: Tommy asked why "no events by default" given .NET modular monoliths, then
  whether "recommended" meant idiomatic or merely easy for small codebases. No Rust idiom exists for
  non-event-sourced events; re-judged at modular-monolith scale. Decided: events only where another module
  or published contract reacts; the entity collects them in a private buffer; the repository's `save` (the
  only write path) drains them into the outbox in its transaction. → `rust:domain-design`.

## Completion

Done when the mapping table and findings are recorded here; every question above is decided by Tommy or
explicitly deferred by him; the agreed rules are in the contract skills; `rust:scaffold` exists and its output
passes the Rust gate; the checks are green; and the work is pushed. Finish by listing which Termboard roadmap
candidate decisions the new rules settle, so the Termboard owner can apply them.

## Progress

- 2026-10-03: plan written and handed off. Launched on `claude-opus-5-5`, chosen by Tommy (the lane
  ladder would put this design work at L1).
- 2026-10-03: picked up by the launched session. The handoff prompt file was gone from its temp path, so this
  plan is the canonical goal. Read every input; mapping table recorded under Findings. Primary-source research
  running in three parallel threads (domain idioms; errors, events and ports; structure, naming and tooling).

## Next Steps

1. Read this plan and every input listed above.
2. Do steps 1–3 of the Method, then start step 4 with Tommy.
