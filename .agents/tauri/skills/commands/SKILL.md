---
name: commands
description: Design Tauri 2 command payloads, native validation, serializable errors and IPC permissions. Use when exposing or calling commands, mapping command failures, or changing capabilities and command registration.
kind: standard
domain: rust
profile: core
applicability: Projects explicitly selecting tauri
requires: tauri-2, serde
provenance: framework
---

# Tauri commands

Owns Tauri command transport, validation at the native boundary, serialized errors and command access.
Product invariants remain application-owned; Rust error design remains with `rust:errors`.

```rust
#[derive(serde::Deserialize)]
struct ReadRecord { id: i64 }

#[derive(serde::Serialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
enum ReadRecordFailure { InvalidId }

#[tauri::command]
fn check_record_input(input: ReadRecord) -> Result<(), ReadRecordFailure> {
    if input.id <= 0 { return Err(ReadRecordFailure::InvalidId); }
    Ok(())
}
// Register this command through generate_handler!; the example validates input only.
```

Use explicit serializable transport shapes and verify their matching frontend representation. Command
argument names default to camelCase from JavaScript; test any rename configuration. A frontend generic
type annotation does not validate a native response at runtime. Validate untrusted values and construct
invariant-bearing domain values inside Rust even when the renderer already parsed them.

Return failures the renderer can distinguish, then map them to useful UI state. Preserve diagnostic causes
inside Rust; expose deliberate transport fields rather than serializing arbitrary internal/SQL errors or
using a panic for an expected failure. Check a rejected invoke as well as a successful one. Async work
should use an appropriate async command; move blocking operations off the UI thread using the supported
runtime facilities. Keep borrowed state/lifetime behavior compatible with the selected Tauri version.

Inspect actual Tauri 2 ACL configuration. Plugin commands require their plugin permissions in the calling
window/webview's capability. Application commands registered in invoke_handler are allowed by default
unless restricted through an application command manifest; do not claim an arbitrary permission file alone
restricts every application command. When access must be constrained, configure that manifest, permission
and capability together and test rejection from an ungranted caller. A granted command still validates its
inputs. Scope filesystem/shell operations to the application's intended authority rather than trusting
renderer-supplied paths or command strings.

Sources: [commands](https://v2.tauri.app/develop/calling-rust/),
[permissions](https://v2.tauri.app/security/permissions/),
[capabilities](https://v2.tauri.app/security/capabilities/).
