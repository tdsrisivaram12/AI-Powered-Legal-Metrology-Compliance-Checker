"""
Given a product's category/attributes, filter the list of legally-active
rules down to the ones that actually apply to that product.
"""
from __future__ import annotations

from typing import List

from services.rules.schemas.rule_schema import Rule


class ProductContext:
    def __init__(
        self,
        category: str,
        is_packaged_for_retail_sale: bool = True,
        is_imported: bool = False,
        extra_categories: List[str] | None = None,
    ):
        self.category = category
        self.is_packaged_for_retail_sale = is_packaged_for_retail_sale
        self.is_imported = is_imported
        # tags used for matching, e.g. ["grocery", "imported"]
        self.tags = set(extra_categories or [])
        self.tags.add(category)
        if is_imported:
            self.tags.add("imported")


def rule_applies(rule: Rule, product: ProductContext) -> bool:
    crit = rule.applicability

    if crit.packaged_for_retail_sale and not product.is_packaged_for_retail_sale:
        return False

    if product.tags & set(crit.exempt_categories):
        return False

    # empty product_categories list means "applies to everything"
    if crit.product_categories:
        if not (product.tags & set(crit.product_categories)):
            return False

    return True


def applicable_rules(rules: List[Rule], product: ProductContext) -> List[Rule]:
    return [r for r in rules if rule_applies(r, product)]
