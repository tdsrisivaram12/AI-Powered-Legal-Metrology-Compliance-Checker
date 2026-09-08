const products = [
  {
    name: "Packaged Rice",
    manufacturer: "ABC Foods Pvt. Ltd.",
    mrp: "₹120",
    quantity: "500 g",
    status: "Compliant",
  },
  {
    name: "Cooking Oil",
    manufacturer: "FreshDrop Foods",
    mrp: "₹185",
    quantity: "1 L",
    status: "Violation",
  },
  {
    name: "Packaged Biscuits",
    manufacturer: "Daily Foods",
    mrp: "₹40",
    quantity: "200 g",
    status: "Compliant",
  },
  {
    name: "Bath Soap",
    manufacturer: "PureCare",
    mrp: "₹55",
    quantity: "100 g",
    status: "Review",
  },
  {
    name: "Packaged Flour",
    manufacturer: "Golden Grain",
    mrp: "₹65",
    quantity: "1 kg",
    status: "Violation",
  },
];

function StatusBadge({ status }: { status: string }) {
  const styles = {
    Compliant: "bg-emerald-50 text-emerald-700",
    Violation: "bg-red-50 text-red-700",
    Review: "bg-amber-50 text-amber-700",
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

export default function ProductsPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">
          Products
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          View products analyzed by the compliance checker.
        </p>
      </div>

      {/* Search */}
      <div className="rounded-xl border border-slate-200 bg-white p-4">
        <input
          type="text"
          placeholder="Search products or manufacturers..."
          className="w-full rounded-lg border border-slate-200 px-4 py-2.5 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        />
      </div>

      {/* Product Table */}
      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
        <div className="border-b border-slate-200 px-6 py-4">
          <h2 className="font-semibold text-slate-900">
            Product Records
          </h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-6 py-4 font-semibold">Product</th>
                <th className="px-6 py-4 font-semibold">Manufacturer</th>
                <th className="px-6 py-4 font-semibold">MRP</th>
                <th className="px-6 py-4 font-semibold">Quantity</th>
                <th className="px-6 py-4 font-semibold">Status</th>
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100">
              {products.map((product) => (
                <tr
                  key={product.name}
                  className="hover:bg-slate-50"
                >
                  <td className="px-6 py-4 font-medium text-slate-900">
                    {product.name}
                  </td>

                  <td className="px-6 py-4 text-slate-600">
                    {product.manufacturer}
                  </td>

                  <td className="px-6 py-4 font-medium text-slate-900">
                    {product.mrp}
                  </td>

                  <td className="px-6 py-4 text-slate-600">
                    {product.quantity}
                  </td>

                  <td className="px-6 py-4">
                    <StatusBadge status={product.status} />
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