#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import sys

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
NAME = re.compile(r"^[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*$")
VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
PLACEHOLDER = re.compile(r"__[A-Z_]+__")
RESERVED = {
    "abstract", "alloc", "as", "async", "await", "become", "box", "break", "const", "continue", "core", "crate",
    "do", "dyn", "else", "enum", "extern", "false", "final", "fn", "for", "gen", "if", "impl", "in", "let", "loop",
    "macro", "match", "mod", "move", "mut", "override", "priv", "proc_macro", "pub", "ref", "return", "self", "static",
    "std", "struct", "super", "test", "trait", "true", "try", "type", "typeof", "unsafe", "unsized", "use", "virtual",
    "where", "while", "yield",
}
FILES = (
    ("Cargo.toml.in", "Cargo.toml", None),
    ("rust-toolchain.toml.in", "rust-toolchain.toml", None),
    ("rustfmt.toml.in", "rustfmt.toml", None),
    ("clippy.toml.in", "clippy.toml", None),
    ("gitattributes.in", ".gitattributes", None),
    ("gitignore.in", ".gitignore", None),
    ("ci.yml.in", ".github/workflows/ci.yml", None),
    ("AGENTS.md.in", "AGENTS.md", None),
    ("CLAUDE.md.in", "CLAUDE.md", None),
    ("lib.rs.in", "src/lib.rs", None),
    ("main.rs.in", "src/main.rs", "bin"),
)


class ScaffoldError(Exception):
    pass


def installed_stable() -> str:
    try:
        result = subprocess.run(["rustc", "+stable", "--version"], capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        raise ScaffoldError("cannot read the installed stable toolchain; install rustup or pass --toolchain") from error
    match = re.match(r"rustc (\d+\.\d+\.\d+)", result.stdout)
    if match is None:
        raise ScaffoldError(f"unrecognised rustc version output: {result.stdout.strip()}")
    return match.group(1)


def render(template: str, values: dict[str, str | None], kind: str) -> str:
    lines: list[str] = []
    for line in template.splitlines():
        for marker in ("__LIB__", "__BIN__"):
            if line.startswith(marker):
                if marker != f"__{kind.upper()}__":
                    line = None
                    break
                line = line[len(marker):]
        if line is None:
            continue
        if any(values.get(token) is None and token in values for token in PLACEHOLDER.findall(line)):
            continue
        for token in PLACEHOLDER.findall(line):
            if token not in values:
                raise ScaffoldError(f"template uses unknown placeholder {token}")
            line = line.replace(token, values[token])
        lines.append(line)
    text = "\n".join(lines) + "\n"
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text


def plan(name: str, kind: str, description: str | None, toolchain: str) -> dict[str, str]:
    if not NAME.fullmatch(name) or name in RESERVED or name.replace("-", "_") in RESERVED:
        raise ScaffoldError(f"invalid package name: {name}")
    version = VERSION.fullmatch(toolchain)
    if version is None:
        raise ScaffoldError(f"toolchain must be an exact version such as 1.99.0, not {toolchain}")
    if kind == "lib" and not description:
        raise ScaffoldError("a library needs --description for its crate documentation")
    if description is not None and ('"' in description or "\\" in description or "\n" in description):
        raise ScaffoldError("description must be one line without quotes or backslashes")
    values = {
        "__NAME__": name,
        "__KIND__": "library" if kind == "lib" else "application",
        "__DESCRIPTION__": description,
        "__CHANNEL__": "stable" if kind == "lib" else toolchain,
        "__RUST_VERSION__": f"{version.group(1)}.{version.group(2)}",
    }
    files: dict[str, str] = {}
    for source, destination, only in FILES:
        if only is not None and only != kind:
            continue
        files[destination] = render((TEMPLATES / source).read_text(encoding="utf-8"), values, kind)
    return files


def create(destination: Path, name: str, kind: str, description: str | None, toolchain: str, dry_run: bool) -> Path:
    if not destination.is_dir():
        raise ScaffoldError(f"destination does not exist: {destination}")
    project = destination / name
    if project.exists():
        raise ScaffoldError(f"project already exists: {project}")
    files = plan(name, kind, description, toolchain)
    if dry_run:
        for relative in files:
            print(project / relative)
        return project
    for relative, text in files.items():
        path = project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
    print(f"created {project}")
    return project


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a Rust package in the agreed rust:structure layout.")
    parser.add_argument("--name", required=True, help="package name, lowercase with - or _ separators")
    parser.add_argument("--destination", required=True, type=Path, help="existing parent directory")
    parser.add_argument("--lib", action="store_true", help="a library package instead of an application")
    parser.add_argument("--description", help="one-line description; required with --lib")
    parser.add_argument("--toolchain", help="exact Rust version; defaults to the installed stable")
    parser.add_argument("--dry-run", action="store_true", help="list the files without writing them")
    args = parser.parse_args(argv)
    try:
        toolchain = args.toolchain or installed_stable()
        create(args.destination, args.name, "lib" if args.lib else "bin", args.description, toolchain, args.dry_run)
    except ScaffoldError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
