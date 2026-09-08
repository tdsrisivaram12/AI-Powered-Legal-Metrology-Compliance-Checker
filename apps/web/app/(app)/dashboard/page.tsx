import Link from "next/link";

const stats = [
  {
    label: "Inspections Today",
    value: "24",
    change: "+12%",
    description: "vs. yesterday",
  },
  {
    label: "Compliant",
    value: "18",
    change: "75%",
    description: "of today's inspections",
  },
  {
    label: "Violations Found",
    value: "06",
    change: "3 High",
    description: "priority violations",
  },
  {
    label: "Pending Review",
    value: "04",
    change: "Action needed",
    description: "cases awaiting review",
  },
];

const recentInspections = [
  {
    id: "INS-2026-024",
    product: "Packaged Rice",
    manufacturer: "ABC Foods",
    date: "Today, 11:42 AM",
    status: "Compliant",
  },
  {
    id: "INS-2026-023",
    product: "Cooking Oil",
    manufacturer: "FreshDrop Foods",
    date: "Today, 10:18 AM",
    status: "Violation",
  },
  {
    id: "INS-2026-022",
    product: "Packaged Biscuits",
    manufacturer: "Daily Foods",
    date: "Today, 09:54 AM",
    status: "Compliant",
  },
  {
    id: "INS-2026-021",
    product: "Bath Soap",
    manufacturer: "PureCare",
    date: "Yesterday, 04:32 PM",
    status: "Review",
  },
];

const complianceTrend = [
  { day: "Mon", value: 62 },
  { day: "Tue", value: 70 },
  { day: "Wed", value: 68 },
  { day: "Thu", value: 76 },
  { day: "Fri", value: 72 },
  { day: "Sat", value: 81 },
  { day: "Sun", value: 75 },
];

export default function DashboardPage() {
  return (
    <div className="space-y-8">

      {/* Page heading */}
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div>
          <p className="text-sm font-medium text-[#0F2742]">
            Inspection Dashboard
          </p>

          <h1 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
            Inspection Activity
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            Review inspection activity and compliance issues.
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

      {/* Stats */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <div
            key={stat.label}
            className="border border-slate-200 bg-white px-5 py-5"
          >
            <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
              {stat.label}
            </p>

            <p className="mt-3 text-3xl font-semibold tracking-tight text-[#172033]">
              {stat.value}
            </p>

            <div className="mt-2 flex items-center gap-2">
              <span className="text-xs font-medium text-[#0F766E]">
                {stat.change}
              </span>

              <span className="text-xs text-slate-400">
                {stat.description}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Main content */}
      <div className="grid gap-6 xl:grid-cols-3">

        {/* Recent Inspections */}
        <div className="xl:col-span-2 border border-slate-200 bg-white">

          {/* Header */}
          <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
            <div>
              <h2 className="text-sm font-semibold text-slate-900">
                Recent Inspections
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                Latest inspection activity
              </p>
            </div>

            <Link
              href="/inspections"
              className="text-xs font-medium text-[#0F2742] hover:underline"
            >
              View all →
            </Link>
          </div>

          {/* Inspection list */}
          <div className="divide-y divide-slate-100">
            {recentInspections.map((inspection) => (
              <div
                key={inspection.id}
                className="flex flex-col gap-4 px-5 py-4 sm:flex-row sm:items-center sm:justify-between"
              >
                <div className="flex items-center gap-3">

                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-slate-100 text-sm text-slate-500">
                    ▣
                  </div>

                  <div>
                    <p className="text-sm font-medium text-slate-900">
                      {inspection.product}
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      {inspection.manufacturer}
                    </p>

                    <p className="mt-1 text-[11px] text-slate-400">
                      {inspection.id} · {inspection.date}
                    </p>
                  </div>
                </div>

                <span
                  className={`w-fit text-xs font-semibold ${
                    inspection.status === "Compliant"
                      ? "text-[#15803D]"
                      : inspection.status === "Violation"
                        ? "text-[#B91C1C]"
                        : "text-[#B45309]"
                  }`}
                >
                  {inspection.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Priority Violations */}
        <div className="border border-slate-200 bg-white p-5">

          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-sm font-semibold text-slate-900">
                Priority Violations
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                Issues requiring attention
              </p>
            </div>

            <Link
              href="/violations"
              className="text-xs font-medium text-[#0F2742] hover:underline"
            >
              View all →
            </Link>
          </div>

          <div className="mt-5 space-y-3">

            {/* High severity */}
            <div className="border-l-2 border-red-600 bg-slate-50 p-4">
              <div className="flex items-start gap-3">

                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-red-50 text-sm font-semibold text-red-700">
                  !
                </div>

                <div className="min-w-0">
                  <p className="text-sm font-medium text-slate-800">
                    MRP declaration issue
                  </p>

                  <p className="mt-1 text-xs text-slate-500">
                    Packaged Food · INS-2026-023
                  </p>

                  <span className="mt-2 inline-block text-[10px] font-bold uppercase tracking-wide text-red-700">
                    High severity
                  </span>
                </div>
              </div>
            </div>

            {/* Medium severity */}
            <div className="border-l-2 border-amber-500 bg-slate-50 p-4">
              <div className="flex items-start gap-3">

                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-amber-50 text-sm font-semibold text-amber-700">
                  !
                </div>

                <div className="min-w-0">
                  <p className="text-sm font-medium text-slate-800">
                    Manufacturer details incomplete
                  </p>

                  <p className="mt-1 text-xs text-slate-500">
                    Cooking Oil · INS-2026-020
                  </p>

                  <span className="mt-2 inline-block text-[10px] font-bold uppercase tracking-wide text-amber-700">
                    Medium severity
                  </span>
                </div>
              </div>
            </div>

            {/* Medium severity */}
            <div className="border-l-2 border-amber-500 bg-slate-50 p-4">
              <div className="flex items-start gap-3">

                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-amber-50 text-sm font-semibold text-amber-700">
                  !
                </div>

                <div className="min-w-0">
                  <p className="text-sm font-medium text-slate-800">
                    Net quantity declaration
                  </p>

                  <p className="mt-1 text-xs text-slate-500">
                    Biscuits · INS-2026-019
                  </p>

                  <span className="mt-2 inline-block text-[10px] font-bold uppercase tracking-wide text-amber-700">
                    Medium severity
                  </span>
                </div>
              </div>
            </div>

          </div>
        </div>

        {/* Quick Actions */}
        <div className="border border-slate-200 bg-white p-5">

          <h2 className="text-sm font-semibold text-slate-900">
            Quick Actions
          </h2>

          <p className="mt-1 text-xs text-slate-500">
            Common inspector tasks
          </p>

          <div className="mt-5 space-y-3">

            {/* Scan */}
            <Link
              href="/scan"
              className="flex items-center gap-3 rounded-md border border-slate-200 p-3.5 transition hover:border-slate-300 hover:bg-slate-50"
            >
              <div className="flex h-9 w-9 items-center justify-center rounded-md bg-slate-100 text-sm text-slate-700">
                ⌕
              </div>

              <div>
                <p className="text-sm font-medium text-slate-800">
                  Scan Product
                </p>

                <p className="mt-0.5 text-xs text-slate-500">
                  Analyze a product package
                </p>
              </div>
            </Link>

            {/* Inspections */}
            <Link
              href="/inspections"
              className="flex items-center gap-3 rounded-md border border-slate-200 p-3.5 transition hover:border-slate-300 hover:bg-slate-50"
            >
              <div className="flex h-9 w-9 items-center justify-center rounded-md bg-slate-100 text-sm text-slate-700">
                ✓
              </div>

              <div>
                <p className="text-sm font-medium text-slate-800">
                  View Inspections
                </p>

                <p className="mt-0.5 text-xs text-slate-500">
                  Review inspection history
                </p>
              </div>
            </Link>

            {/* Violations */}
            <Link
              href="/violations"
              className="flex items-center gap-3 rounded-md border border-slate-200 p-3.5 transition hover:border-slate-300 hover:bg-slate-50"
            >
              <div className="flex h-9 w-9 items-center justify-center rounded-md bg-red-50 text-sm text-red-700">
                !
              </div>

              <div>
                <p className="text-sm font-medium text-slate-800">
                  Review Violations
                </p>

                <p className="mt-0.5 text-xs text-slate-500">
                  Check flagged products
                </p>
              </div>
            </Link>

          </div>
        </div>

      </div>

      {/* Compliance Trend */}
      <div className="border border-slate-200 bg-white p-5">

        <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-start">
          <div>
            <h2 className="text-sm font-semibold text-slate-900">
              Compliance Trend
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Compliance rate over the last 7 days
            </p>
          </div>

          <span className="text-xs font-medium text-slate-500">
            Last 7 days
          </span>
        </div>

        <div className="mt-6 flex h-48 items-end gap-3">

          {complianceTrend.map((item) => (
            <div
              key={item.day}
              className="flex h-full flex-1 flex-col items-center justify-end gap-2"
            >

              <span className="text-[10px] font-medium text-slate-500">
                {item.value}%
              </span>

              <div className="flex h-32 w-full items-end bg-slate-100">
                <div
                  className="w-full bg-[#0F2742]"
                  style={{ height: `${item.value}%` }}
                />
              </div>

              <span className="text-[11px] text-slate-400">
                {item.day}
              </span>

            </div>
          ))}

        </div>
      </div>

      {/* Compliance Overview */}
      <div className="border border-slate-200 bg-white p-5">

        <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">

          <div>
            <h2 className="text-sm font-semibold text-slate-900">
              Compliance Overview
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Today's inspection performance
            </p>
          </div>

          <span className="text-xs font-semibold text-[#15803D]">
            75% compliant
          </span>

        </div>

        {/* Progress */}
        <div className="mt-5 h-2 overflow-hidden bg-slate-100">
          <div
            className="h-full bg-[#15803D]"
            style={{ width: "75%" }}
          />
        </div>

        {/* Breakdown */}
        <div className="mt-4 flex flex-col gap-2 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">

          <span>
            <span className="font-medium text-[#15803D]">
              18
            </span>{" "}
            compliant
          </span>

          <span>
            <span className="font-medium text-[#B91C1C]">
              6
            </span>{" "}
            violations
          </span>

          <span>
            <span className="font-medium text-slate-700">
              24
            </span>{" "}
            total inspections
          </span>

        </div>

      </div>

    </div>
  );
}