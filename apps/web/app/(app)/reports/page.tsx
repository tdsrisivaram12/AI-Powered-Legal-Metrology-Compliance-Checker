const reports = [
  {
    id: "RPT-2026-024",
    inspection: "INS-2026-024",
    product: "Packaged Rice",
    date: "07 Sep 2026",
    status: "Compliant",
  },
  {
    id: "RPT-2026-023",
    inspection: "INS-2026-023",
    product: "Cooking Oil",
    date: "07 Sep 2026",
    status: "Violation",
  },
  {
    id: "RPT-2026-022",
    inspection: "INS-2026-022",
    product: "Packaged Biscuits",
    date: "06 Sep 2026",
    status: "Compliant",
  },
];

function StatusBadge({ status }: { status: string }) {
  const styles = {
    Compliant: "bg-emerald-50 text-emerald-700",
    Violation: "bg-red-50 text-red-700",
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

export default function ReportsPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">
            Reports
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            View and generate compliance inspection reports.
          </p>
        </div>

        <button className="rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-700">
          + Generate Report
        </button>
      </div>

      {/* Report Summary */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <p className="text-sm text-slate-500">Total Reports</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">24</p>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <p className="text-sm text-slate-500">Generated This Month</p>
          <p className="mt-2 text-3xl font-bold text-blue-600">18</p>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <p className="text-sm text-slate-500">Violation Reports</p>
          <p className="mt-2 text-3xl font-bold text-red-600">06</p>
        </div>
      </div>

      {/* Reports Table */}
      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
        <div className="border-b border-slate-200 px-6 py-4">
          <h2 className="font-semibold text-slate-900">
            Recent Reports
          </h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-6 py-4 font-semibold">Report ID</th>
                <th className="px-6 py-4 font-semibold">
                  Inspection ID
                </th>
                <th className="px-6 py-4 font-semibold">Product</th>
                <th className="px-6 py-4 font-semibold">Date</th>
                <th className="px-6 py-4 font-semibold">Status</th>
                <th className="px-6 py-4 font-semibold">Action</th>
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100">
              {reports.map((report) => (
                <tr
                  key={report.id}
                  className="hover:bg-slate-50"
                >
                  <td className="px-6 py-4 font-medium text-blue-600">
                    {report.id}
                  </td>

                  <td className="px-6 py-4 text-slate-600">
                    {report.inspection}
                  </td>

                  <td className="px-6 py-4 font-medium text-slate-900">
                    {report.product}
                  </td>

                  <td className="px-6 py-4 text-slate-600">
                    {report.date}
                  </td>

                  <td className="px-6 py-4">
                    <StatusBadge status={report.status} />
                  </td>

                  <td className="px-6 py-4">
                    <button className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-700 hover:bg-slate-50">
                      View Report
                    </button>
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