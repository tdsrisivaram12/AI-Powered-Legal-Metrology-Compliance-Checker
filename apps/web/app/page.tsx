import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-900 text-xl text-white">
              ⚖
            </div>

            <div>
              <h1 className="text-lg font-bold text-slate-900">
                LegalMetrix
              </h1>
              <p className="text-xs text-slate-500">
                Legal Metrology Compliance Checker
              </p>
            </div>
          </div>

          <Link
            href="/login"
            className="rounded-lg bg-blue-900 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-800"
          >
            Inspector Login
          </Link>
        </div>
      </header>

      {/* Hero */}
      <section className="mx-auto grid max-w-7xl gap-12 px-6 py-20 lg:grid-cols-2 lg:items-center">
        <div>
          <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900">
            <span>✦</span>
            AI-Powered Compliance
          </div>

          <h2 className="max-w-2xl text-5xl font-bold leading-tight tracking-tight text-slate-950">
            Smarter inspections.
            <br />
            <span className="text-blue-900">Stronger compliance.</span>
          </h2>

          <p className="mt-6 max-w-xl text-lg leading-8 text-slate-600">
            An intelligent platform that helps Legal Metrology inspectors
            analyze packaged commodities, identify violations, and generate
            compliance reports faster.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              href="/login"
              className="rounded-xl bg-blue-900 px-6 py-3.5 font-semibold text-white shadow-sm transition hover:bg-blue-800"
            >
              Start Inspection →
            </Link>

            <Link
              href="/scan"
              className="rounded-xl border border-slate-300 bg-white px-6 py-3.5 font-semibold text-slate-700 transition hover:bg-slate-100"
            >
              Try Product Scan
            </Link>
          </div>

          <div className="mt-10 flex flex-wrap gap-8 text-sm text-slate-500">
            <div>
              <p className="font-semibold text-slate-900">AI-assisted</p>
              <p>Inspection workflow</p>
            </div>

            <div>
              <p className="font-semibold text-slate-900">OCR powered</p>
              <p>Package information extraction</p>
            </div>

            <div>
              <p className="font-semibold text-slate-900">Rule based</p>
              <p>Compliance verification</p>
            </div>
          </div>
        </div>

        {/* Scan Preview */}
        <div className="relative">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-xl">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-500">
                  Compliance Check
                </p>
                <h3 className="mt-1 text-xl font-bold text-slate-900">
                  Product Analysis
                </h3>
              </div>

              <div className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700">
                ✓ Verified
              </div>
            </div>

            <div className="rounded-2xl bg-slate-100 p-8 text-center">
              <div className="mx-auto flex h-24 w-24 items-center justify-center rounded-2xl bg-white text-5xl shadow-sm">
                📦
              </div>

              <p className="mt-4 font-semibold text-slate-800">
                Packaged Commodity
              </p>

              <p className="mt-1 text-sm text-slate-500">
                AI analysis completed
              </p>
            </div>

            <div className="mt-6 space-y-3">
              <div className="flex justify-between rounded-xl bg-slate-50 p-4">
                <span className="text-sm text-slate-500">MRP</span>
                <span className="font-semibold text-slate-900">₹120</span>
              </div>

              <div className="flex justify-between rounded-xl bg-slate-50 p-4">
                <span className="text-sm text-slate-500">Net Quantity</span>
                <span className="font-semibold text-slate-900">500 g</span>
              </div>

              <div className="flex justify-between rounded-xl bg-slate-50 p-4">
                <span className="text-sm text-slate-500">Manufacturer</span>
                <span className="font-semibold text-slate-900">ABC Foods</span>
              </div>
            </div>

            <div className="mt-5 rounded-xl border border-emerald-200 bg-emerald-50 p-4">
              <p className="text-sm font-semibold text-emerald-800">
                ✓ No violations detected
              </p>
              <p className="mt-1 text-xs text-emerald-700">
                Package information meets the configured compliance rules.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white">
        <div className="mx-auto max-w-7xl px-6 py-6 text-center text-sm text-slate-500">
          AI-Powered Legal Metrology Compliance Checker
        </div>
      </footer>
    </main>
  );
}