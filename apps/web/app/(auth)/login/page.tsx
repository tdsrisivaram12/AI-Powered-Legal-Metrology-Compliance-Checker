import Link from "next/link";

export default function LoginPage() {
  return (
    <main className="min-h-screen bg-slate-50">
      <div className="grid min-h-screen lg:grid-cols-2">

        {/* Left side */}
        <section className="hidden bg-blue-950 p-12 text-white lg:flex lg:flex-col lg:justify-between">
          <div>
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white text-xl text-blue-950">
                ⚖
              </div>

              <div>
                <h1 className="font-bold">LegalMetrix</h1>
                <p className="text-xs text-blue-200">
                  Legal Metrology Compliance Checker
                </p>
              </div>
            </div>
          </div>

          <div className="max-w-lg">
            <p className="mb-4 text-sm font-medium uppercase tracking-widest text-blue-300">
              Inspector Portal
            </p>

            <h2 className="text-4xl font-bold leading-tight">
              Intelligent compliance,
              <br />
              simplified.
            </h2>

            <p className="mt-5 leading-7 text-blue-100">
              Analyze packaged commodities, identify potential violations,
              and streamline your inspection workflow with AI-assisted tools.
            </p>

            <div className="mt-8 grid grid-cols-3 gap-3">
              <div className="rounded-xl border border-blue-800 bg-blue-900/50 p-4">
                <p className="text-xl font-bold">AI</p>
                <p className="mt-1 text-xs text-blue-200">Assisted</p>
              </div>

              <div className="rounded-xl border border-blue-800 bg-blue-900/50 p-4">
                <p className="text-xl font-bold">OCR</p>
                <p className="mt-1 text-xs text-blue-200">Extraction</p>
              </div>

              <div className="rounded-xl border border-blue-800 bg-blue-900/50 p-4">
                <p className="text-xl font-bold">✓</p>
                <p className="mt-1 text-xs text-blue-200">Compliance</p>
              </div>
            </div>
          </div>

          <p className="text-xs text-blue-300">
            AI-Powered Legal Metrology Compliance Checker
          </p>
        </section>

        {/* Right side */}
        <section className="flex items-center justify-center px-6 py-12">
          <div className="w-full max-w-md">

            {/* Mobile logo */}
            <div className="mb-10 flex items-center gap-3 lg:hidden">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-900 text-xl text-white">
                ⚖
              </div>

              <div>
                <h1 className="font-bold text-slate-900">LegalMetrix</h1>
                <p className="text-xs text-slate-500">
                  Compliance Checker
                </p>
              </div>
            </div>

            <div className="mb-8">
              <p className="text-sm font-medium text-blue-900">
                Inspector Portal
              </p>

              <h2 className="mt-2 text-3xl font-bold text-slate-950">
                Welcome back
              </h2>

              <p className="mt-2 text-slate-500">
                Sign in to continue to your inspection workspace.
              </p>
            </div>

            <form className="space-y-5">

              <div>
                <label
                  htmlFor="email"
                  className="mb-2 block text-sm font-medium text-slate-700"
                >
                  Email address
                </label>

                <input
                  id="email"
                  type="email"
                  placeholder="inspector@example.gov.in"
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-900 focus:ring-2 focus:ring-blue-100"
                />
              </div>

              <div>
                <div className="mb-2 flex items-center justify-between">
                  <label
                    htmlFor="password"
                    className="block text-sm font-medium text-slate-700"
                  >
                    Password
                  </label>

                  <button
                    type="button"
                    className="text-sm font-medium text-blue-900 hover:underline"
                  >
                    Forgot password?
                  </button>
                </div>

                <input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-900 focus:ring-2 focus:ring-blue-100"
                />
              </div>

              <label className="flex items-center gap-2 text-sm text-slate-600">
                <input
                  type="checkbox"
                  className="h-4 w-4 rounded border-slate-300"
                />
                Remember me
              </label>

              <button
                type="submit"
                className="w-full rounded-xl bg-blue-900 py-3.5 font-semibold text-white shadow-sm transition hover:bg-blue-800"
              >
                Sign in
              </button>
            </form>

            <div className="my-7 flex items-center gap-4">
              <div className="h-px flex-1 bg-slate-200" />
              <span className="text-xs text-slate-400">OR</span>
              <div className="h-px flex-1 bg-slate-200" />
            </div>

            <p className="text-center text-sm text-slate-500">
              New to the platform?{" "}
              <Link
                href="/register"
                className="font-semibold text-blue-900 hover:underline"
              >
                Create an account
              </Link>
            </p>

            <p className="mt-8 text-center text-xs leading-5 text-slate-400">
              Authorized users only. This portal is intended for
              Legal Metrology inspection and compliance activities.
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}