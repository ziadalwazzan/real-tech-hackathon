export default function SegmentedToggle({ value, onChange }) {
  return (
    <div className="inline-flex rounded-full bg-slate-100 p-1 text-sm">
      {[
        { label: "City", value: "city" },
        { label: "ZIP code", value: "zip" },
      ].map((option) => (
        <button
          key={option.value}
          type="button"
          onClick={() => onChange(option.value)}
          className={`rounded-full px-4 py-2 transition ${
            value === option.value
              ? "bg-ink text-white shadow"
              : "text-slate-600 hover:text-ink"
          }`}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}
