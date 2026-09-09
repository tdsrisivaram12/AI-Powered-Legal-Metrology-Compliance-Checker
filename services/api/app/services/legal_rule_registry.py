from dataclasses import asdict

from app.services.legal_rule_engine import LegalRule


RULE_REGISTRY: tuple[LegalRule, ...] = (
    LegalRule(
        rule_id="PCR-6-MANUFACTURER",
        rule_name="Manufacturer/Packer/Importer Declaration",
        category="Food",
        description="Package should declare the name and address of the manufacturer, packer or importer, as applicable.",
        source="Legal Metrology (Packaged Commodities) Rules, 2011 - Rule 6",
        source_version="2011-consolidated",
        effective_from="2011-04-01",
        check_type="required_field",
        parameters={
            "field": "manufacturer_name",
        },
    ),
    LegalRule(
        rule_id="PCR-6-NET-QUANTITY",
        rule_name="Net Quantity Declaration",
        category="Food",
        description="Package should declare net quantity in the applicable standard unit of weight or measure or in number.",
        source="Legal Metrology (Packaged Commodities) Rules, 2011 - Rule 6",
        source_version="2011-consolidated",
        effective_from="2011-04-01",
        check_type="required_field",
        parameters={
            "field": "net_quantity",
        },
    ),
    LegalRule(
        rule_id="PCR-6-MRP",
        rule_name="Maximum Retail Price Declaration",
        category="Food",
        description="Retail sale price should be declared in the form of Maximum Retail Price (MRP) inclusive of all taxes.",
        source="Legal Metrology (Packaged Commodities) Rules, 2011 - Rule 6",
        source_version="2011-consolidated",
        effective_from="2011-04-01",
        check_type="required_field",
        parameters={
            "field": "mrp",
        },
    ),
)


def get_applicable_rules(
    category: str,
) -> list[LegalRule]:
    return [
        rule
        for rule in RULE_REGISTRY
        if rule.category.lower() == category.lower()
    ]


def rules_as_dict() -> list[dict]:
    return [asdict(rule) for rule in RULE_REGISTRY]
