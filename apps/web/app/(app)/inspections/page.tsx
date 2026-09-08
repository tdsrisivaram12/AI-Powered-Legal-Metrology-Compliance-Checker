import Link from "next/link";

const inspections = [
  {
    id: "INS-2026-024",
    product: "Packaged Rice",
    manufacturer: "ABC Foods",
    date: "07 Sep 2026",
    status: "Compliant",
  },
  {
    id: "INS-2026-023",
    product: "Cooking Oil",
    manufacturer: "FreshDrop Foods",
    date: "07 Sep 2026",
    status: "Violation",
  },
  {
    id: "INS-2026-022",
    product: "Packaged Biscuits",
    manufacturer: "Daily Foods",
    date: "06 Sep 2026",
    status: "Compliant",
  },
  {
    id: "INS-2026-021",
    product: "Bath Soap",
    manufacturer: "PureCare",
    date: "06 Sep 2026",
    status: "Review",
  },
  {
    id: "INS-2026-020",
    product: "Packaged Flour",
    manufacturer: "Golden Grain",
    date: "05 Sep 2026",
    status: "Violation",
  },
];

function StatusText({ status }: { status: string }) {
  const styles = {
    Compliant: "text-[#15803D]",
    Violation: "text-[#B91C1C]",
    Review: "text-[#B45309]",
  };

  return (
    <span
      className={`text-xs font-semibold ${
        styles[status as keyof typeof styles]
      }`}
    >
      {status}
    </span>
  );
}

export default function InspectionsPage() {
  return (
    <div className="space-y-8">

      {/* Page heading */}
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div>
          <p className="text-sm font-medium text-[#0F2742]">
            Inspection Workspace
          </p>

          <h1 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
            Inspections
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            View and manage product compliance inspections.
          </p>
        </div>

        <Link
          href="/scan"
          className="inline-flex items-center gap-2 rounded-md bg-[#0F2742] px-4 py-2.5 text-sm font-medium text-white transition hover:bg-[#173B61]"
        >
          <span className="text-base">+</span>
          New Inspection
        </Link>
      </div>

      {/* Summary */}
      <div className="grid gap-4 sm:grid-cols-3">

        <div className="border border-slate-200 bg-white px-5 py-5">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
            Total Inspections
          </p>

          <p className="mt-3 text-3xl font-semibold tracking-tight text-[#172033]">
            24
          </p>

          <p className="mt-2 text-xs text-slate-400">
            All recorded inspections
          </p>
        </div>

        <div className="border border-slate-200 bg-white px-5 py-5">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
            Compliant
          </p>

          <p className="mt-3 text-3xl font-semibold tracking-tight text-[#15803D]">
            18
          </p>

          <p className="mt-2 text-xs text-slate-400">
            75% of total inspections
          </p>
        </div>

        <div className="border border-slate-200 bg-white px-5 py-5">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
            Violations
          </p>

          <p className="mt-3 text-3xl font-semibold tracking-tight text-[#B91C1C]">
            06
          </p>

          <p className="mt-2 text-xs text-slate-400">
            Cases requiring attention
          </p>
        </div>

      </div>

      {/* Inspection registry */}
      <div className="border border-slate-200 bg-white">

        {/* Table header */}
        <div className="flex flex-col justify-between gap-4 border-b border-slate-200 px-5 py-4 md:flex-row md:items-center">

          <div>
            <h2 className="text-sm font-semibold text-slate-900">
              Inspection Records
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Latest product inspection activity
            </p>
          </div>

          {/* Filters */}
          <div className="flex gap-2">

            <button className="rounded-md border border-slate-200 bg-white px-3 py-2 text-xs font-medium text-slate-600 transition hover:bg-slate-50">
              All Statuses
              <span className="ml-2 text-slate-400">⌄</span>
            </button>

            <button className="rounded-md border border-slate-200 bg-white px-3 py-2 text-xs font-medium text-slate-600 transition hover:bg-slate-50">
              Recent
              <span className="ml-2 text-slate-400">⌄</span>
            </button>

          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left">

            <thead>
              <tr className="border-b border-slate-200 bg-slate-50">

                <th className="px-5 py-3 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
                  Inspection ID
                </th>

                <th className="px-5 py-3 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
                  Product
                </th>

                <th className="px-5 py-3 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
                  Manufacturer
                </th>

                <th className="px-5 py-3 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
                  Date
                </th>

                <th className="px-5 py-3 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
                  Status
                </th>

                <th className="px-5 py-3 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
                  Action
                </th>

              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100">

              {inspections.map((inspection) => (
                <tr
                  key={inspection.id}
                  className="transition hover:bg-slate-50"
                >

                  {/* ID */}
                  <td className="whitespace-nowrap px-5 py-4">
                    <span className="text-xs font-semibold text-[#0F2742]">
                      {inspection.id}
                    </span>
                  </td>

                  {/* Product */}
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-3">

                      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-slate-100 text-xs text-slate-500">
                        ▣
                      </div>

                      <span className="text-sm font-medium text-slate-900">
                        {inspection.product}
                      </span>

                    </div>
                  </td>

                  {/* Manufacturer */}
                  <td className="whitespace-nowrap px-5 py-4 text-sm text-slate-600">
                    {inspection.manufacturer}
                  </td>

                  {/* Date */}
                  <td className="whitespace-nowrap px-5 py-4 text-sm text-slate-500">
                    {inspection.date}
                  </td>

                  {/* Status */}
                  <td className="px-5 py-4">
                    <StatusText status={inspection.status} />
                  </td>

                  {/* Action */}
                  <td className="px-5 py-4">
                    <button className="text-xs font-medium text-[#0F2742] hover:underline">
                      View
                    </button>
                  </td>

                </tr>
              ))}

            </tbody>

          </table>
        </div>

        {/* Table footer */}
        <div className="flex flex-col justify-between gap-3 border-t border-slate-200 px-5 py-4 sm:flex-row sm:items-center">

          <p className="text-xs text-slate-500">
            Showing{" "}
            <span className="font-medium text-slate-700">
              5
            </span>{" "}
            of{" "}
            <span className="font-medium text-slate-700">
              24
            </span>{" "}
            inspections
          </p>

          <div className="flex items-center gap-1">

            <button
              disabled
              className="rounded-md border border-slate-200 px-3 py-1.5 text-xs text-slate-400"
            >
              Previous
            </button>

            <button className="rounded-md bg-[#0F2742] px-3 py-1.5 text-xs font-medium text-white">
              1
            </button>

            <button className="rounded-md border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-50">
              2
            </button>

            <button className="rounded-md border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-50">
              3
            </button>

            <button className="rounded-md border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-50">
              Next
            </button>

          </div>
        </div>

      </div>

    </div>
  );
}