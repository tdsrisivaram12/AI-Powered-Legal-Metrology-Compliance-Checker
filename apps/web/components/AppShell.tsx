"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: "▦" },
  { name: "Scan Product", href: "/scan", icon: "⌕" },
  { name: "Inspections", href: "/inspections", icon: "✓" },
  { name: "Products", href: "/products", icon: "▣" },
  { name: "Violations", href: "/violations", icon: "!" },
  { name: "Evidence", href: "/evidence", icon: "◫" },
  { name: "Reports", href: "/reports", icon: "▤" },
  { name: "Rules", href: "/rules", icon: "⚖" },
  { name: "Analytics", href: "/analytics", icon: "↗" },
];

export default function AppShell({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <div className="flex min-h-screen bg-slate-50">
      {/* Sidebar */}
      <aside className="flex w-64 flex-col border-r border-slate-200 bg-white">
        {/* Logo */}
        <div className="border-b border-slate-200 px-5 py-5">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-md bg-[#0F2742] text-lg text-white">
              ⚖
            </div>

            <div>
              <div className="text-lg font-semibold tracking-tight text-[#0F2742]">
                LegalMetrix
              </div>

              <p className="text-xs text-slate-500">
                Inspection & Compliance
              </p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-5">
          <p className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-widest text-slate-400">
            Workspace
          </p>

          <div className="space-y-1">
            {navigation.map((item) => {
              const active = pathname === item.href;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-3 rounded-md px-3 py-2.5 text-sm transition ${
                    active
                      ? "bg-slate-100 font-medium text-[#0F2742]"
                      : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                  }`}
                >
                  <span
                    className={`flex h-7 w-7 items-center justify-center rounded-md text-sm ${
                      active
                        ? "bg-[#0F2742] text-white"
                        : "bg-slate-100 text-slate-500"
                    }`}
                  >
                    {item.icon}
                  </span>

                  {item.name}
                </Link>
              );
            })}
          </div>
        </nav>

        {/* User */}
        <div className="border-t border-slate-200 p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-100 text-sm font-medium text-[#0F2742]">
              IN
            </div>

            <div className="min-w-0">
              <p className="truncate text-sm font-medium text-slate-800">
                Inspector
              </p>

              <p className="truncate text-xs text-slate-500">
                Legal Metrology
              </p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main area */}
      <div className="flex min-w-0 flex-1 flex-col">
        {/* Header */}
        <header className="flex h-20 items-center justify-between border-b border-slate-200 bg-white px-6">
          <div>
            <p className="text-xs text-slate-400">
              Legal Metrology
            </p>

            <p className="font-semibold text-slate-800">
              Inspection Workspace
            </p>
          </div>

          <div className="flex items-center gap-4">
            <button className="relative flex h-9 w-9 items-center justify-center rounded-md border border-slate-200 text-slate-600 transition hover:bg-slate-50">
              🔔

              <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-red-500" />
            </button>

            <div className="hidden h-8 w-px bg-slate-200 sm:block" />

            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#0F2742] text-sm font-medium text-white">
                IN
              </div>

              <div className="hidden sm:block">
                <p className="text-sm font-medium text-slate-800">
                  Inspector
                </p>

                <p className="text-xs text-slate-500">
                  Authorized User
                </p>
              </div>
            </div>
          </div>
        </header>

        {/* Page */}
        <main className="flex-1 p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}