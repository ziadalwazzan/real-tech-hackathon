import { useState } from "react";

const CATEGORIES = [
  {
    id: "employment",
    label: "Employment",
    description: "Labor demand, wage momentum, and hiring depth.",
  },
  {
    id: "crime",
    label: "Crime & Safety",
    description: "Public safety signals and incident stability.",
  },
  {
    id: "geospatial",
    label: "Geospatial",
    description: "Physical exposure, access, and location buffers.",
  },
  {
    id: "housing",
    label: "Housing Market",
    description: "Inventory pressure, price traction, and leasing heat.",
  },
  {
    id: "climate",
    label: "Climate",
    description: "Weather volatility and environmental risk factors.",
  },
  {
    id: "other",
    label: "Other Signals",
    description: "Amenities, mobility, and demand momentum.",
  },
];

export default function ExploreCities() {
  const [activeCategory, setActiveCategory] = useState("employment");

  return (
    <section className="flex flex-1 flex-col gap-6">
      <div className="text-left">
        <p className="text-xs uppercase tracking-[0.4em] text-slate-500">
          Explore by category
        </p>
      </div>

      <div className="flex gap-3 overflow-x-auto pb-3">
        {CATEGORIES.map((category) => (
          <button
            key={category.id}
            type="button"
            onClick={() => setActiveCategory(category.id)}
            className={`flex min-w-max items-center gap-2 rounded-full border px-4 py-2 text-xs font-semibold uppercase tracking-[0.25em] transition ${
              activeCategory === category.id
                ? "border-ink bg-ink text-white shadow"
                : "border-slate-200 bg-white/70 text-slate-500 hover:border-slate-400 hover:text-ink"
            }`}
          >
            {category.label}
          </button>
        ))}
      </div>
    </section>
  );
}
