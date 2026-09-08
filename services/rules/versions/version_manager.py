"""
Loads rule sets from services/rules/sources/*.json and resolves which
individual Rule objects are active for a given "as of" date. This is what
lets the 2026 amendments layer on top of the base 2011 rules without
editing the original rule records.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import List

from services.rules.schemas.rule_schema import Rule, RuleSet

SOURCES_DIR = Path(__file__).resolve().parent.parent / "sources"


class VersionManager:
    def __init__(self, sources_dir: Path = SOURCES_DIR):
        self.sources_dir = sources_dir
        self._rule_sets: List[RuleSet] = []
        self._load_all()

    def _load_all(self) -> None:
        self._rule_sets = []
        for path in sorted(self.sources_dir.glob("*.json")):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._rule_sets.append(RuleSet(**data))

    def all_rules(self) -> List[Rule]:
        rules: List[Rule] = []
        for rs in self._rule_sets:
            rules.extend(rs.rules)
        return rules

    def active_rules(self, as_of: date | None = None) -> List[Rule]:
        """Return the rules that are legally in force on `as_of` (default: today)."""
        as_of = as_of or date.today()
        return [r for r in self.all_rules() if r.is_active_on(as_of)]

    def get_rule(self, rule_id: str) -> Rule | None:
        for r in self.all_rules():
            if r.rule_id == rule_id:
                return r
        return None


if __name__ == "__main__":
    vm = VersionManager()
    for r in vm.active_rules():
        print(f"{r.rule_id:20s} {r.version:20s} {r.title}")
