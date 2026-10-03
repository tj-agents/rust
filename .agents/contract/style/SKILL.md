---
name: style
description: Tommy's agreed Rust style — naming, formatting, comments and lint policy. Read before writing or reviewing Rust that touches it; nothing applies until it is recorded here.
kind: contract
domain: rust
profile: contract
applicability: Rust projects
requires: rust
provenance: house
---

# Rust style

Owns naming, formatting, comments, and the lint policy above the repository's clippy configuration.

## Agreed

- A type does not repeat its module's name (`card::Title`, `card::Status`, `card::FinishError`); the main
  type may equal it (`card::Card`). Import types by path, call functions through their module
  (`service::finish_card`), and qualify a generic or clashing name (`card::Status`). Enforced by clippy
  `module_name_repetitions = "warn"`. Source: RFC 356 (`io::Error`); the Book 7.4.
- Names follow the API Guidelines naming chapter whole: acronyms are one word (`Uuid`); `as_` is a free borrow,
  `to_` builds a value, `into_` consumes; getters take no `get_` prefix; `iter`, `iter_mut`, `into_iter`;
  `new` is the primary constructor, `with_*` a variant, `from_*` a conversion. Source: API Guidelines C-CASE,
  C-CONV, C-GETTER, C-ITER, C-CTOR.
- Clippy runs `all` and `pedantic` at warn, allowing `must_use_candidate`, `missing_errors_doc`,
  `missing_panics_doc`, `similar_names` and `too_many_lines`; warnings fail CI. Why: pedantic teaches idioms
  once its noisiest lints are off. Source: ruff and uv `[workspace.lints]`.
- A library documents every exported item with a one-line summary, plus `# Errors` and `# Panics` where not
  obvious, under `missing_docs = "warn"`. An application documents only what needs it. No doc restates a
  name. Source: API Guidelines documentation chapter.
