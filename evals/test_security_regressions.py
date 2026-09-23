"""Deterministic repository guardrails for the corporate hardened fork."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ARCHITECTURE_FILES = (
    SKILLS / "engineering" / "improve-codebase-architecture" / "SKILL.md",
    SKILLS / "engineering" / "improve-codebase-architecture" / "HTML-REPORT.md",
)


class SecurityPolicyTests(unittest.TestCase):
    def test_every_skill_points_to_security_policy(self) -> None:
        skill_files = sorted(SKILLS.glob("**/SKILL.md"))
        self.assertTrue(skill_files, "no skills discovered")
        missing = [
            str(path.relative_to(ROOT))
            for path in skill_files
            if "SECURITY.md" not in path.read_text(encoding="utf-8")
        ]
        self.assertEqual([], missing)

    def test_active_or_mutating_skills_are_explicit_only(self) -> None:
        explicit_only = (
            "engineering/diagnosing-bugs",
            "engineering/domain-modeling",
            "engineering/implement",
            "engineering/improve-codebase-architecture",
            "engineering/tdd",
            "engineering/to-spec",
            "engineering/to-tickets",
            "productivity/grill-me",
            "productivity/writing-for-agents",
        )
        for relative in explicit_only:
            metadata = SKILLS / relative / "agents" / "openai.yaml"
            with self.subTest(skill=relative):
                text = metadata.read_text(encoding="utf-8")
                self.assertRegex(
                    text,
                    r"(?m)^\s*allow_implicit_invocation:\s*false\s*$",
                )

    def test_architecture_reports_have_no_active_or_remote_dependencies(self) -> None:
        forbidden = {
            "script element": re.compile(r"<script\b", re.IGNORECASE),
            "external stylesheet": re.compile(
                r"<link\b[^>]*\brel=[\"']?stylesheet", re.IGNORECASE
            ),
            "remote URL": re.compile(r"https?://", re.IGNORECASE),
            "CSS import": re.compile(r"@import\b", re.IGNORECASE),
            "remote source attribute": re.compile(
                r"\b(?:src|href)\s*=\s*[\"']\s*//", re.IGNORECASE
            ),
        }
        for path in ARCHITECTURE_FILES:
            text = path.read_text(encoding="utf-8")
            for label, pattern in forbidden.items():
                with self.subTest(file=path.name, pattern=label):
                    self.assertIsNone(pattern.search(text))

    def test_core_policy_boundaries_are_present(self) -> None:
        policy = (ROOT / "SECURITY.md").read_text(encoding="utf-8").lower()
        required = (
            "untrusted input",
            "repository root",
            "environment-variable values",
            "external network access is denied by default",
            "production",
            "capability, not authorization",
            "gortex",
            "mcp beworks",
            "corporate mcp gateway",
            "inline static svg",
        )
        missing = [phrase for phrase in required if phrase not in policy]
        self.assertEqual([], missing)

    def test_supply_chain_instructions_do_not_use_latest(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotRegex(readme, r"npx\s+skills@latest")
        self.assertIn("git fetch upstream", readme)
        self.assertIn("v1.0.0-corp.1", readme)

    def test_adversarial_evals_cover_required_scenarios(self) -> None:
        cases = (ROOT / "evals" / "security-cases.md").read_text(
            encoding="utf-8"
        )
        for case_id in ("SEC1", "SEC2", "SEC3", "SEC4", "SEC5", "SEC6"):
            with self.subTest(case=case_id):
                self.assertIn(f"## {case_id}", cases)


if __name__ == "__main__":
    unittest.main()
