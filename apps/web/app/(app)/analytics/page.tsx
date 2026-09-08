const stats = [
  {
    label: "Total Inspections",
    value: "24",
    change: "+12%",
  },
  {
    label: "Compliant Products",
    value: "18",
    change: "+8%",
  },
  {
    label: "Violations Detected",
    value: "06",
    change: "-4%",
  },
  {
    label: "Avg. Compliance Score",
    value: "82%",
    change: "+6%",
  },
];

const violationTypes = [
  { name: "Missing declarations", count: 3 },
  { name: "Quantity mismatch", count: 2 },
  { name: "Manufacturer details", count: 1 },
];

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">
          Analytics
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          Monitor inspection activity and compliance trends.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <div
            key={stat.label}
            className="rounded-xl border border-slate-200 bg-white p-5"
          >
            <p className="text-sm text-slate-500">{stat.label}</p>

            <div className="mt-2 flex items-end justify-between">
              <p className="text-3xl font-bold text-slate-900">
                {stat.value}
              </p>

              <span className="text-xs font-semibold text-emerald-600">
                {stat.change}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Main Analytics */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Compliance Overview */}
        <div className="rounded-xl border border-slate-200 bg-white p-6">
          <h2 className="font-semibold text-slate-900">
            Compliance Overview
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Current inspection outcomes
          </p>

          <div className="mt-8 flex items-center justify-center">
            <div className="flex h-44 w-44 items-center justify-center rounded-full border-[18px] border-emerald-100">
              <div className="text-center">
                <p className="text-3xl font-bold text-slate-900">
                  75%
                </p>
                <p className="text-xs text-slate-500">
                  Compliant
                </p>
              </div>
            </div>
          </div>

          <div className="mt-8 grid grid-cols-2 gap-4 text-center">
            <div className="rounded-lg bg-emerald-50 p-4">
              <p className="text-2xl font-bold text-emerald-700">
                18
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Compliant
              </p>
            </div>

            <div className="rounded-lg bg-red-50 p-4">
              <p className="text-2xl font-bold text-red-700">
                6
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Violations
              </p>
            </div>
          </div>
        </div>

        {/* Violation Breakdown */}
        <div className="rounded-xl border border-slate-200 bg-white p-6">
          <h2 className="font-semibold text-slate-900">
            Violation Breakdown
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Most frequently detected issues
          </p>

          <div className="mt-7 space-y-6">
            {violationTypes.map((item) => (
              <div key={item.name}>
                <div className="mb-2 flex justify-between text-sm">
                  <span className="font-medium text-slate-700">
                    {item.name}
                  </span>

                  <span className="font-semibold text-slate-900">
                    {item.count}
                  </span>
                </div>

                <div className="h-2 rounded-full bg-slate-100">
                  <div
                    className="h-2 rounded-full bg-blue-600"
                    style={{
                      width: `${(item.count / 3) * 100}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="mt-8 rounded-lg bg-slate-50 p-4">
            <p className="text-sm font-semibold text-slate-800">
              Insight
            </p>

            <p className="mt-1 text-sm leading-6 text-slate-500">
              Missing or incomplete package declarations are currently
              the most frequently detected issue.
            </p>
          </div>
        </div>
      </div>

      {/* Activity */}
      <div className="rounded-xl border border-slate-200 bg-white p-6">
        <h2 className="font-semibold text-slate-900">
          Inspection Activity
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Recent inspection volume
        </p>

        <div className="mt-8 flex h-48 items-end gap-4">
          {[8, 12, 7, 15, 11, 18, 14].map((value, index) => (
            <div
              key={index}
              className="flex flex-1 flex-col items-center gap-2"
            >
              <div
                className="w-full rounded-t-lg bg-blue-100"
                style={{ height: `${value * 7}px` }}
              />

              <span className="text-xs text-slate-400">
                {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][index]}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}