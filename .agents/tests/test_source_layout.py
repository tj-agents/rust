from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from unittest import mock
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("sync_generated", ROOT / ".agents" / "sync_generated.py")
sync_generated = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync_generated)


class SourceLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads((ROOT / ".agents/plugins/sources.json").read_text(encoding="utf-8"))
        cls.payloads = json.loads((ROOT / ".agents/plugins/payloads.json").read_text(encoding="utf-8"))
        cls.skills = sync_generated.discover(ROOT, cls.config)

    def test_inventory_is_the_knowledge_and_contract_tiers(self) -> None:
        kinds = {name: skill["metadata"]["kind"] for name, skill in self.skills.items()}
        self.assertEqual({"learning", "knowledge", "direction"}, {name for name, kind in kinds.items() if kind == "knowledge"})
        self.assertEqual(
            {"style", "structure", "domain-design", "errors", "testing", "build", "libraries"},
            {name for name, kind in kinds.items() if kind == "contract"},
        )
        self.assertFalse((ROOT / ".agents/skills").exists())

    def test_every_skill_is_in_exactly_one_profile(self) -> None:
        assigned = [name for names in self.payloads["profiles"].values() for name in names]
        self.assertEqual(len(assigned), len(set(assigned)))
        self.assertEqual(set(self.skills), set(assigned))

    def test_generated_adapters_reference_canonical_and_package_is_self_contained(self) -> None:
        for name, skill in self.skills.items():
            source = ROOT / skill["relative"]
            package = ROOT / "plugins/rust/skills" / name / "SKILL.md"
            self.assertEqual(source.read_bytes(), package.read_bytes())
            for adapter_root in (".codex/skills", ".claude/skills"):
                adapter = (ROOT / adapter_root / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("canonical shared definition", adapter)
                self.assertNotEqual(source.read_text(encoding="utf-8"), adapter)

    def test_bare_and_qualified_skill_references_resolve(self) -> None:
        for suffix, message in (
            ("\nSee the `missing-capability` skill.\n", "missing bare skill reference"),
            ("\nSee `rust:missing-capability`.\n", "missing local skill reference"),
        ):
            broken = dict(self.skills["learning"])
            broken["body"] = broken["body"] + suffix
            copied = dict(self.skills)
            copied["learning"] = broken
            with self.assertRaisesRegex(ValueError, message):
                sync_generated.validate(ROOT, self.config, self.payloads, copied)

    def test_tier_applies_only_where_cargo_is_present(self) -> None:
        tier = json.loads((ROOT / ".agents/tiers/rust.json").read_text(encoding="utf-8"))
        self.assertEqual("stack-present", tier["applies"])
        self.assertIn("Cargo.toml", tier["detect"]["files"])
        changed = dict(tier, applies="always")
        with mock.patch.object(sync_generated, "load", return_value=changed):
            with self.assertRaisesRegex(ValueError, "stack tier"):
                sync_generated.validate_tier(ROOT)

    def test_host_manifests_reject_drift_and_cache_pinning(self) -> None:
        codex = json.loads((ROOT / ".agents/plugins/manifests/codex/rust.json").read_text(encoding="utf-8"))
        claude = json.loads((ROOT / ".agents/plugins/manifests/claude/rust.json").read_text(encoding="utf-8"))
        codex_marketplace = json.loads((ROOT / ".agents/plugins/manifests/codex/marketplace.json").read_text(encoding="utf-8"))
        claude_marketplace = json.loads((ROOT / ".agents/plugins/manifests/claude/marketplace.json").read_text(encoding="utf-8"))
        sync_generated.validate_host_metadata(codex, claude, codex_marketplace, claude_marketplace)
        changed = dict(claude)
        changed["description"] = "drifted"
        with self.assertRaisesRegex(ValueError, "disagree on description"):
            sync_generated.validate_host_metadata(codex, changed, codex_marketplace, claude_marketplace)
        changed = dict(claude)
        changed["version"] = None
        with self.assertRaisesRegex(ValueError, "omit version"):
            sync_generated.validate_host_metadata(codex, changed, codex_marketplace, claude_marketplace)
        changed_codex, changed_claude = dict(codex), dict(claude)
        changed_codex["name"] = changed_claude["name"] = "other"
        with self.assertRaisesRegex(ValueError, "rust identity"):
            sync_generated.validate_host_metadata(changed_codex, changed_claude, codex_marketplace, claude_marketplace)

    def test_canonical_definitions_have_no_embedded_bom(self) -> None:
        for skill in self.skills.values():
            self.assertNotIn("﻿", skill["body"])

    def test_generated_selection_matches_metadata(self) -> None:
        selection = json.loads((ROOT / "plugins/rust/selection.json").read_text(encoding="utf-8"))
        self.assertEqual(self.payloads["profiles"], selection["profiles"])
        by_name = {item["name"]: item for item in selection["skills"]}
        self.assertEqual(set(self.skills), set(by_name))


if __name__ == "__main__":
    unittest.main()
