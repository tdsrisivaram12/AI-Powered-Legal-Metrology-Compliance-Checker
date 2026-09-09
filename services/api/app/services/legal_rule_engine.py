from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LegalRule:
    rule_id: str
    rule_name: str
    category: str
    description: str
    source: str
    source_version: str
    effective_from: str
    check_type: str
    parameters: dict[str, Any]
