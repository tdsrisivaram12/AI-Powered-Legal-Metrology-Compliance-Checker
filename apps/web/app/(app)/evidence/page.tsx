const evidence = [
  {
    id: "EVD-2026-006",
    product: "Cooking Oil",
    violation: "Mandatory declarations incomplete",
    source: "Front label image",
    confidence: "96%",
    date: "07 Sep 2026",
  },
  {
    id: "EVD-2026-005",
    product: "Packaged Flour",
    violation: "Net quantity declaration mismatch",
    source: "Package label + OCR",
    confidence: "91%",
    date: "05 Sep 2026",
  },
  {
    id: "EVD-2026-004",
    product: "Bath Soap",
    violation: "Manufacturer details require review",
    source: "Back label image",
    confidence: "87%",
    date: "06 Sep 2026",
  },
];

export default function EvidencePage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">
          Evidence
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          Review the evidence supporting detected compliance violations.
        </p>
      </div>

      {/* Explanation */}
      <div className="rounded-xl border border-blue-100 bg-blue-50 p-5">
        <h2 className="font-semibold text-blue-900">
          Explainable Compliance
        </h2>
        <p className="mt-1 text-sm leading-6 text-blue-800">
          Each detected violation is linked to evidence from the product
          image, OCR output, and extracted information. This helps
          inspectors understand why a product was flagged.
        </p>
      </div>

      {/* Evidence Cards */}
      <div className="grid gap-5 lg:grid-cols-2">
        {evidence.map((item) => (
          <div
            key={item.id}
            className="rounded-xl border border-slate-200 bg-white p-6"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-blue-600">
                  {item.id}
                </p>

                <h2 className="mt-2 text-lg font-semibold text-slate-900">
                  {item.product}
                </h2>
              </div>

              <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                {item.confidence} confidence
              </span>
            </div>

            <div className="mt-5 space-y-4">
              <div>
                <p className="text-xs font-medium uppercase text-slate-400">
                  Detected Violation
                </p>
                <p className="mt-1 text-sm font-medium text-red-700">
                  {item.violation}
                </p>
              </div>

              <div>
                <p className="text-xs font-medium uppercase text-slate-400">
                  Evidence Source
                </p>
                <p className="mt-1 text-sm text-slate-700">
                  {item.source}
                </p>
              </div>

              <div>
                <p className="text-xs font-medium uppercase text-slate-400">
                  Inspection Date
                </p>
                <p className="mt-1 text-sm text-slate-700">
                  {item.date}
                </p>
              </div>
            </div>

            <button className="mt-6 w-full rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50">
              View Evidence
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}