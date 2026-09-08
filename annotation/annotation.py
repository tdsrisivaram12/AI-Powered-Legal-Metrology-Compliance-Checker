"""
Annotations link a Finding (from services/compliance) to a region of an
evidence image -- e.g. "the MRP text box is missing here" -- so the officer
and the PDF report can show exactly where on the package the problem is.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BoundingBox:
    x: float  # normalized 0-1, relative to image width
    y: float  # normalized 0-1, relative to image height
    width: float
    height: float

    def to_pixels(self, image_width: int, image_height: int) -> tuple[int, int, int, int]:
        return (
            int(self.x * image_width),
            int(self.y * image_height),
            int(self.width * image_width),
            int(self.height * image_height),
        )


@dataclass
class Annotation:
    evidence_id: str
    label: str
    rule_id: Optional[str] = None
    box: Optional[BoundingBox] = None
    note: str = ""


@dataclass
class AnnotatedEvidence:
    evidence_id: str
    annotations: List[Annotation] = field(default_factory=list)

    def add(self, annotation: Annotation) -> None:
        self.annotations.append(annotation)

    def for_rule(self, rule_id: str) -> List[Annotation]:
        return [a for a in self.annotations if a.rule_id == rule_id]
