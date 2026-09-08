"""
Pydantic schemas describing a single Legal Metrology rule and its versions.

A "rule" here is one checkable requirement under the Legal Metrology
(Packaged Commodities) Rules, e.g. "MRP must be declared inclusive of taxes".
"""
from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class RuleSeverity(str, Enum):
    CRITICAL = "critical"      # e.g. missing MRP -> auto SUSPECTED_NON_COMPLIANCE
    MAJOR = "major"             # e.g. font size violation
    MINOR = "minor"             # e.g. formatting inconsistency


class DeclarationField(str, Enum):
    MRP = "mrp"
    NET_QUANTITY = "net_quantity"
    MANUFACTURER_NAME = "manufacturer_name"
    MANUFACTURER_ADDRESS = "manufacturer_address"
    MFG_DATE = "mfg_date"
    EXPIRY_DATE = "expiry_date"
    CONSUMER_CARE = "consumer_care"
    UNIT_SALE_PRICE = "unit_sale_price"
    COUNTRY_OF_ORIGIN = "country_of_origin"
    COMMODITY_NAME = "commodity_name"
    NOT_FOR_RETAIL_SALE = "not_for_retail_sale"


class ApplicabilityCriteria(BaseModel):
    """Which products a rule applies to."""
    product_categories: List[str] = Field(default_factory=list)  # empty = all
    packaged_for_retail_sale: bool = True
    exempt_categories: List[str] = Field(default_factory=list)


class Rule(BaseModel):
    rule_id: str
    title: str
    description: str
    field: DeclarationField
    severity: RuleSeverity
    legal_reference: str          # e.g. "Rule 6(1)(b), Legal Metrology (Packaged Commodities) Rules, 2011"
    effective_from: date
    effective_to: Optional[date] = None
    version: str                  # e.g. "2011", "2026-amendment-1"
    applicability: ApplicabilityCriteria = Field(default_factory=ApplicabilityCriteria)
    validation_regex: Optional[str] = None
    min_font_size_mm: Optional[float] = None
    required: bool = True

    def is_active_on(self, check_date: date) -> bool:
        if check_date < self.effective_from:
            return False
        if self.effective_to and check_date > self.effective_to:
            return False
        return True


class RuleSet(BaseModel):
    source: str
    version: str
    published_on: date
    rules: List[Rule]
