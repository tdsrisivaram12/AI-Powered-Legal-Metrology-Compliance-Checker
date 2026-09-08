"""
API-facing request/response models. Kept separate from services/rules and
services/compliance's internal dataclasses/pydantic models so the HTTP
contract can evolve independently of the domain logic.
"""
from __future__ import annotations

from datetime import date
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ProductContextIn(BaseModel):
    category: str = Field(..., examples=["grocery"])
    is_packaged_for_retail_sale: bool = True
    is_imported: bool = False
    extra_categories: List[str] = Field(default_factory=list)


class DeclarationIn(BaseModel):
    """Extracted-declaration fields, typically produced by services/ai's pipeline."""
    mrp: Optional[str] = None
    net_quantity: Optional[str] = None
    manufacturer_name: Optional[str] = None
    manufacturer_address: Optional[str] = None
    mfg_date: Optional[str] = None
    expiry_date: Optional[str] = None
    consumer_care: Optional[str] = None
    unit_sale_price: Optional[str] = None
    country_of_origin: Optional[str] = None
    commodity_name: Optional[str] = None

    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.model_dump().items() if v is not None}


class EvaluateComplianceIn(BaseModel):
    product_id: str
    declaration: DeclarationIn
    product_context: ProductContextIn
    as_of: Optional[date] = None
    manufacturer: Optional[str] = None
    notify_emails: List[str] = Field(default_factory=list)


class FindingOut(BaseModel):
    rule_id: str
    field: str
    severity: str
    message: str
    legal_reference: str


class ComplianceResultOut(BaseModel):
    product_id: str
    decision: str
    score: int
    findings: List[FindingOut]
    notified: bool = False


class RuleOut(BaseModel):
    rule_id: str
    title: str
    field: str
    severity: str
    legal_reference: str
    version: str
    required: bool


class SimilarCaseOut(BaseModel):
    product_id: str
    score: float
    decision: str
    manufacturer: Optional[str] = None
