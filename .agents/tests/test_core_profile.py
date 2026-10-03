from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("sync_generated", ROOT / ".agents" / "sync_generated.py")
sync_generated = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync_generated)


class RustCoreProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = sync_generated.load_config(ROOT)
        cls.plugins = sync_generated.discover(ROOT, cls.config["namespace"])
        cls.skills = cls.plugins["rust"]

    def test_required_stack_contracts_are_core_and_present(self) -> None:
        required = {"style", "structure", "domain-design", "errors", "testing", "build", "libraries"}
        self.assertTrue(required.issubset(self.skills))
        for name in required:
            self.assertEqual("contract", self.skills[name]["kind"])
            self.assertEqual("core", self.skills[name]["metadata"]["profile"])

    def test_core_is_exactly_the_contracts(self) -> None:
        core_names = {
            name for name, skill in self.skills.items() if skill["metadata"]["profile"] == "core"
        }
        self.assertEqual(
            {"style", "structure", "domain-design", "errors", "build", "libraries", "testing"},
            core_names,
        )

    def test_structure_declares_its_file_structure_section(self) -> None:
        body = self.skills["structure"]["body"]
        self.assertIn("## File structure", body)

    def test_scaffold_is_its_own_profile(self) -> None:
        self.assertEqual("scaffold", self.skills["scaffold"]["metadata"]["profile"])

    def test_knowledge_tier_keeps_its_own_profile(self) -> None:
        for name in ("learning", "knowledge", "direction"):
            self.assertEqual("knowledge", self.skills[name]["metadata"]["profile"])


if __name__ == "__main__":
    unittest.main()
