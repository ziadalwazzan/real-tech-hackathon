export default function RiskGauge({ score, label, color }) {
  const radius = 72;
  const stroke = 12;
  const normalizedRadius = radius - stroke * 0.5;
  const circumference = normalizedRadius * 2 * Math.PI;
  const clampedScore = Math.max(0, Math.min(100, score));
  const offset = circumference - (clampedScore / 100) * circumference;

  const colorMap = {
    green: "text-lime",
    yellow: "text-amber",
    red: "text-rose",
  };

  return (
    <div className="flex flex-col items-center">
      <div className="relative">
        <svg height={radius * 2} width={radius * 2}>
          <circle
            stroke="#e2e8f0"
            fill="transparent"
            strokeWidth={stroke}
            r={normalizedRadius}
            cx={radius}
            cy={radius}
          />
          <circle
            stroke="currentColor"
            fill="transparent"
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={`${circumference} ${circumference}`}
            style={{ strokeDashoffset: offset }}
            r={normalizedRadius}
            cx={radius}
            cy={radius}
            className={`transition-all duration-700 ${colorMap[color] || "text-ink"}`}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center" />
      </div>
      <p className="mt-3 text-sm font-semibold text-slate-700">{label}</p>
    </div>
  );
}
