export async function analyzeProduct(image: string) {
  // Backend API will be connected here later.

  // For now, return demo data.
  return {
    product: "Packaged Rice",
    mrp: "₹120",
    quantity: "500 g",
    manufacturer: "ABC Foods Pvt. Ltd.",
    packedDate: "08/2026",
    bestBefore: "12 months from packing",
    status: "Violation" as const,
    complianceScore: 72,
    confidence: 96,
    violations: [
      {
        rule: "Net Quantity Declaration",
        reason:
          "The declared quantity requires further verification against the applicable Legal Metrology rules.",
        severity: "Medium" as const,
      },
    ],
  };
}