---
name: structure
description: Own the Tauri 2 frontend/native boundary, command registration and managed application state. Use when arranging a Tauri application, registering commands or introducing shared native resources; frontend frameworks and database drivers are selected separately.
kind: convention
domain: rust
profile: core
applicability: Projects explicitly selecting tauri
requires: tauri-2
provenance: framework
---

# Tauri structure

Owns the Tauri frontend/native boundary, command registration and managed state. Select this capability
explicitly; neither React nor SQLx is a prerequisite. The application owns its concrete folder structure,
framework selection, domain operations and verification commands.

```rust
// In the application's Tauri builder, register the transport boundary once.
let builder = tauri::Builder::default()
    .manage(app_state)
    .invoke_handler(tauri::generate_handler![commands::read_record]);
```

Keep renderer code behind the IPC boundary: native resources and authoritative operations remain in Rust.
Register commands together in the invoke handler; do not scatter independent handler registrations that
replace one another. Keep command adapters distinct from reusable operations so native behavior can be
exercised without a renderer. See `tauri:commands` for payloads, errors and permissions.

Initialize long-lived resources through the application's startup path and manage their owning state.
Retrieve the same concrete managed type with `tauri::State`; a type mismatch does not find the resource.
Choose synchronization from the resource's actual API, avoid holding a blocking lock across await, and
report startup failure before exposing an unusable window. Do not mandate a database, global singleton or
one state container shape merely because Tauri supports managed state.

The app owns lifecycle/shutdown and user-data paths. Native tests and platform packaging become separate
capabilities when that work is entered; no placeholder testing or packaging skills are selected here.

Sources: [project structure](https://v2.tauri.app/start/project-structure/),
[state management](https://v2.tauri.app/develop/state-management/).
