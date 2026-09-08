const violations = [
  {
    id: "VIO-2026-006",
    product: "Cooking Oil",
    issue: "Mandatory declarations incomplete",
    severity: "High",
    date: "07 Sep 2026",
    status: "Open",
  },
  {
    id: "VIO-2026-005",
    product: "Packaged Flour",
    issue: "Net quantity declaration mismatch",
    severity: "Medium",
    date: "05 Sep 2026",
    status: "Open",
  },
  {
    id: "VIO-2026-004",
    product: "Bath Soap",
    issue: "Manufacturer details require review",
    severity: "Low",
    date: "06 Sep 2026",
    status: "Under Review",
  },
];

function SeverityBadge({ severity }: { severity: string }) {
  const styles = {
    High: "bg-red-50 text-red-700",
    Medium: "bg-orange-50 text-orange-700",
    Low: "bg-amber-50 text-amber-700",
  };

  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-semibold ${
        styles[severity as keyof typeof styles]
      }`}
    >
      {severity}
    </span>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles = {
    Open: "bg-red-50 text-red-700",
    "Under Review": "bg-amber-50 text-amber-700",
  };

  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-semibold ${
        styles[status as keyof typeof styles]
      }`}
    >
      {status}
    </span>
  );
}

export default function ViolationsPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">
          Violations
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          Review compliance violations detected during inspections.
        </p>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <p className="text-sm text-slate-500">Total Violations</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">06</p>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <p className="text-sm text-slate-500">High Severity</p>
          <p className="mt-2 text-3xl font-bold text-red-600">02</p>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <p className="text-sm text-slate-500">Under Review</p>
          <p className="mt-2 text-3xl font-bold text-amber-600">01</p>
        </div>
      </div>

      {/* Violations Table */}
      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
        <div className="border-b border-slate-200 px-6 py-4">
          <h2 className="font-semibold text-slate-900">
            Detected Violations
          </h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-6 py-4 font-semibold">Violation ID</th>
                <th className="px-6 py-4 font-semibold">Product</th>
                <th className="px-6 py-4 font-semibold">Detected Issue</th>
                <th className="px-6 py-4 font-semibold">Severity</th>
                <th className="px-6 py-4 font-semibold">Date</th>
                <th className="px-6 py-4 font-semibold">Status</th>
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100">
              {violations.map((violation) => (
                <tr
                  key={violation.id}
                  className="hover:bg-slate-50"
                >
                  <td className="px-6 py-4 font-medium text-blue-600">
                    {violation.id}
                  </td>

                  <td className="px-6 py-4 font-medium text-slate-900">
                    {violation.product}
                  </td>

                  <td className="px-6 py-4 text-slate-600">
                    {violation.issue}
                  </td>

                  <td className="px-6 py-4">
                    <SeverityBadge severity={violation.severity} />
                  </td>

                  <td className="px-6 py-4 text-slate-600">
                    {violation.date}
                  </td>

                  <td className="px-6 py-4">
                    <StatusBadge status={violation.status} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}