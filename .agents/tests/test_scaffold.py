from __future__ import annotations

import contextlib
import importlib.util
import io
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents/rust/utility/scaffold/scripts/new_rust_project.py"
SPEC = importlib.util.spec_from_file_location("new_rust_project", SCRIPT)
scaffold = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scaffold)

COMMON = {
    "Cargo.toml",
    "rust-toolchain.toml",
    "rustfmt.toml",
    "clippy.toml",
    ".gitattributes",
    ".gitignore",
    ".github/workflows/ci.yml",
    "AGENTS.md",
    "CLAUDE.md",
    "src/lib.rs",
}


def generate(destination: Path, *args: str) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return scaffold.main(["--destination", str(destination), "--toolchain", "1.97.1", *args])


def files(project: Path) -> set[str]:
    return {path.relative_to(project).as_posix() for path in project.rglob("*") if path.is_file()}


class ScaffoldTests(unittest.TestCase):
    def test_application_is_a_clean_pinned_skeleton(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            self.assertEqual(0, generate(Path(temporary), "--name", "demo_app"))
            project = Path(temporary) / "demo_app"
            self.assertEqual(COMMON | {"src/main.rs"}, files(project))
            self.assertEqual("\n", (project / "src/lib.rs").read_text(encoding="utf-8"))
            self.assertEqual("fn main() {}\n", (project / "src/main.rs").read_text(encoding="utf-8"))
            self.assertIn('channel = "1.97.1"', (project / "rust-toolchain.toml").read_text(encoding="utf-8"))
            manifest = (project / "Cargo.toml").read_text(encoding="utf-8")
            self.assertIn('rust-version = "1.97"', manifest)
            self.assertNotIn("missing_docs", manifest)
            self.assertNotIn("description", manifest)
            self.assertEqual("@AGENTS.md\n", (project / "CLAUDE.md").read_text(encoding="utf-8"))

    def test_library_tracks_stable_and_documents_its_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            self.assertEqual(0, generate(Path(temporary), "--name", "demo-lib", "--lib", "--description", "Parses demo values"))
            project = Path(temporary) / "demo-lib"
            self.assertEqual(COMMON, files(project))
            self.assertEqual("//! Parses demo values\n", (project / "src/lib.rs").read_text(encoding="utf-8"))
            self.assertIn('channel = "stable"', (project / "rust-toolchain.toml").read_text(encoding="utf-8"))
            self.assertIn('missing_docs = "warn"', (project / "Cargo.toml").read_text(encoding="utf-8"))

    def test_every_placeholder_is_resolved_and_files_are_lf(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            generate(Path(temporary), "--name", "demo_app")
            generate(Path(temporary), "--name", "demo-lib", "--lib", "--description", "Parses demo values")
            for path in Path(temporary).rglob("*"):
                if path.is_file():
                    data = path.read_bytes()
                    self.assertNotIn(b"\r\n", data, path)
                    self.assertIsNone(re.search(rb"__[A-Z_]+__", data), path)

    def test_rejections_write_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "taken").mkdir()
            self.assertEqual(1, generate(root, "--name", "taken"))
            self.assertEqual(1, generate(root, "--name", "fn"))
            self.assertEqual(1, generate(root, "--name", "Bad_Name"))
            self.assertEqual(1, generate(root, "--name", "nodoc", "--lib"))
            self.assertEqual(1, generate(root / "missing", "--name", "demo"))
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(1, scaffold.main(["--name", "demo", "--destination", str(root), "--toolchain", "stable"]))
            self.assertEqual(0, generate(root, "--name", "preview", "--dry-run"))
            self.assertEqual({"taken"}, {path.name for path in root.iterdir()})

    @unittest.skipIf(shutil.which("cargo") is None, "cargo is not installed")
    def test_generated_projects_pass_the_rust_gate(self) -> None:
        stable = scaffold.installed_stable()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with contextlib.redirect_stdout(io.StringIO()):
                scaffold.create(root, "demo_app", "bin", None, stable, False)
                scaffold.create(root, "demo-lib", "lib", "Parses demo values", stable, False)
            for name in ("demo_app", "demo-lib"):
                for command in (
                    ["cargo", "fmt", "--all", "--check"],
                    ["cargo", "clippy", "--workspace", "--all-targets", "--all-features", "--", "-D", "warnings"],
                    ["cargo", "test", "--workspace", "--all-features"],
                ):
                    result = subprocess.run(
                        command, cwd=root / name, capture_output=True, text=True, env=os.environ | {"RUSTUP_TOOLCHAIN": "stable"}
                    )
                    self.assertEqual(0, result.returncode, f"{name}: {' '.join(command)}\n{result.stderr}")


if __name__ == "__main__":
    unittest.main()
