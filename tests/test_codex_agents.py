import json
from pathlib import Path
import sys
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import discover_codex_agents  # noqa: E402
import generate_codex_agents  # noqa: E402


class CodexAgentTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "worki/codex-agents.json").read_text())
        self.squad = json.loads((ROOT / "worki/squad.json").read_text())

    def test_generated_agents_are_current_and_discoverable(self):
        generated = generate_codex_agents.build(check=True)
        discovered = discover_codex_agents.discover()
        self.assertEqual(10, len(generated))
        self.assertEqual(10, len(discovered))
        expected = {self.manifest["orchestrator"]["name"]}
        expected.update(agent["name"] for agent in self.manifest["agents"])
        self.assertEqual(expected, {agent["name"] for agent in discovered})

    def test_every_stage_routes_to_one_installed_agent(self):
        stages = {stage["id"] for stage in self.squad["stages"]}
        routed = {agent["stage"] for agent in self.manifest["agents"]}
        self.assertEqual(stages, routed)

    def test_embedded_instructions_include_sources_skill_and_safety_contract(self):
        stages = {stage["id"]: stage for stage in self.squad["stages"]}
        for agent in self.manifest["agents"]:
            path = ROOT / self.manifest["output_dir"] / f'{agent["slug"]}.toml'
            data = tomllib.loads(path.read_text())
            instructions = data["developer_instructions"]
            for source in stages[agent["stage"]]["agents"]:
                self.assertIn(f"`{source}`", instructions)
            self.assertIn(stages[agent["stage"]]["skill"], instructions)
            self.assertIn("Não altere sites", instructions)
            self.assertIn("THIRD_PARTY_NOTICES.md", instructions)

    def test_orchestrator_contains_delegation_roster(self):
        orchestrator = self.manifest["orchestrator"]
        path = ROOT / self.manifest["output_dir"] / f'{orchestrator["slug"]}.toml'
        data = tomllib.loads(path.read_text())
        for agent in self.manifest["agents"]:
            self.assertIn(agent["name"], data["developer_instructions"])


if __name__ == "__main__":
    unittest.main()
