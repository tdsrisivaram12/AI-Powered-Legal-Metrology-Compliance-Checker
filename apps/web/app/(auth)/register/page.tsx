import Link from "next/link";

export default function RegisterPage() {
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
              Get started
            </p>

            <h2 className="text-4xl font-bold leading-tight">
              Build faster,
              <br />
              inspect smarter.
            </h2>

            <p className="mt-5 leading-7 text-blue-100">
              Create your inspector account and access intelligent tools for
              packaged commodity inspections and compliance verification.
            </p>

            <div className="mt-8 space-y-4">
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-900">
                  ✓
                </div>
                <span className="text-sm text-blue-100">
                  AI-assisted product analysis
                </span>
              </div>

              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-900">
                  ✓
                </div>
                <span className="text-sm text-blue-100">
                  Automated compliance checks
                </span>
              </div>

              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-900">
                  ✓
                </div>
                <span className="text-sm text-blue-100">
                  Structured inspection records
                </span>
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
                Inspector Registration
              </p>

              <h2 className="mt-2 text-3xl font-bold text-slate-950">
                Create your account
              </h2>

              <p className="mt-2 text-slate-500">
                Set up your account to access the inspection workspace.
              </p>
            </div>

            <form className="space-y-5">

              {/* Full name */}
              <div>
                <label
                  htmlFor="name"
                  className="mb-2 block text-sm font-medium text-slate-700"
                >
                  Full name
                </label>

                <input
                  id="name"
                  type="text"
                  placeholder="Enter your full name"
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-900 focus:ring-2 focus:ring-blue-100"
                />
              </div>

              {/* Email */}
              <div>
                <label
                  htmlFor="email"
                  className="mb-2 block text-sm font-medium text-slate-700"
                >
                  Official email address
                </label>

                <input
                  id="email"
                  type="email"
                  placeholder="name@example.gov.in"
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-900 focus:ring-2 focus:ring-blue-100"
                />
              </div>

              {/* Role */}
              <div>
                <label
                  htmlFor="role"
                  className="mb-2 block text-sm font-medium text-slate-700"
                >
                  Role
                </label>

                <select
                  id="role"
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-700 outline-none transition focus:border-blue-900 focus:ring-2 focus:ring-blue-100"
                  defaultValue=""
                >
                  <option value="" disabled>
                    Select your role
                  </option>
                  <option value="inspector">Legal Metrology Inspector</option>
                  <option value="officer">Compliance Officer</option>
                  <option value="admin">Administrator</option>
                </select>
              </div>

              {/* Password */}
              <div>
                <label
                  htmlFor="password"
                  className="mb-2 block text-sm font-medium text-slate-700"
                >
                  Password
                </label>

                <input
                  id="password"
                  type="password"
                  placeholder="Create a password"
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-900 focus:ring-2 focus:ring-blue-100"
                />
              </div>

              {/* Confirm password */}
              <div>
                <label
                  htmlFor="confirm-password"
                  className="mb-2 block text-sm font-medium text-slate-700"
                >
                  Confirm password
                </label>

                <input
                  id="confirm-password"
                  type="password"
                  placeholder="Confirm your password"
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-900 focus:ring-2 focus:ring-blue-100"
                />
              </div>

              {/* Terms */}
              <label className="flex items-start gap-3 text-sm text-slate-500">
                <input
                  type="checkbox"
                  className="mt-1 h-4 w-4 rounded border-slate-300"
                />

                <span>
                  I agree to the platform's terms of use and understand that
                  this portal is intended for authorized compliance activities.
                </span>
              </label>

              <button
                type="submit"
                className="w-full rounded-xl bg-blue-900 py-3.5 font-semibold text-white shadow-sm transition hover:bg-blue-800"
              >
                Create account
              </button>
            </form>

            <p className="mt-7 text-center text-sm text-slate-500">
              Already have an account?{" "}
              <Link
                href="/login"
                className="font-semibold text-blue-900 hover:underline"
              >
                Sign in
              </Link>
            </p>

            <p className="mt-8 text-center text-xs leading-5 text-slate-400">
              Account access and permissions will be connected to the
              authentication service during backend integration.
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}