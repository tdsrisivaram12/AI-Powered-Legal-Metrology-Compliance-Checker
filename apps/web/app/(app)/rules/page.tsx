const rules = [
  {
    id: "LM-PC-001",
    title: "Declaration of Maximum Retail Price",
    category: "Price Declaration",
    description:
      "The package should clearly display the maximum retail price inclusive of applicable taxes.",
    status: "Active",
  },
  {
    id: "LM-PC-002",
    title: "Net Quantity Declaration",
    category: "Quantity",
    description:
      "The package should declare the net quantity using the appropriate unit of measurement.",
    status: "Active",
  },
  {
    id: "LM-PC-003",
    title: "Manufacturer Details",
    category: "Manufacturer",
    description:
      "The package should contain the required name and address details of the manufacturer or packer.",
    status: "Active",
  },
  {
    id: "LM-PC-004",
    title: "Date of Packing",
    category: "Date & Packaging",
    description:
      "The applicable date information should be declared clearly and legibly on the package.",
    status: "Active",
  },
  {
    id: "LM-PC-005",
    title: "Consumer Care Information",
    category: "Consumer Information",
    description:
      "Required consumer care contact information should be available on the package.",
    status: "Active",
  },
];

const categoryStyles = {
  "Price Declaration": "bg-blue-50 text-blue-700",
  Quantity: "bg-purple-50 text-purple-700",
  Manufacturer: "bg-emerald-50 text-emerald-700",
  "Date & Packaging": "bg-amber-50 text-amber-700",
  "Consumer Information": "bg-slate-100 text-slate-700",
};

export default function RulesPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">
            Compliance Rules
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Rules used to evaluate packaged commodities for compliance.
          </p>
        </div>

        <div className="rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700">
          5 Active Rules
        </div>
      </div>

      {/* Info */}
      <div className="rounded-xl border border-blue-100 bg-blue-50 p-5">
        <h2 className="font-semibold text-blue-900">
          Rule-Based Compliance Checking
        </h2>

        <p className="mt-1 text-sm leading-6 text-blue-800">
          Extracted information from product packaging is compared against
          applicable compliance rules. Each violation can then be traced
          back to the rule that was triggered.
        </p>
      </div>

      {/* Rules */}
      <div className="grid gap-5 md:grid-cols-2">
        {rules.map((rule) => (
          <div
            key={rule.id}
            className="rounded-xl border border-slate-200 bg-white p-6"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-blue-600">
                  {rule.id}
                </p>

                <h2 className="mt-2 text-lg font-semibold text-slate-900">
                  {rule.title}
                </h2>
              </div>

              <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                {rule.status}
              </span>
            </div>

            <div className="mt-4">
              <span
                className={`rounded-full px-3 py-1 text-xs font-semibold ${
                  categoryStyles[
                    rule.category as keyof typeof categoryStyles
                  ]
                }`}
              >
                {rule.category}
              </span>
            </div>

            <p className="mt-5 text-sm leading-6 text-slate-600">
              {rule.description}
            </p>

            <div className="mt-5 border-t border-slate-100 pt-4">
              <button className="text-sm font-semibold text-blue-600 hover:text-blue-700">
                View Rule Details →
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}