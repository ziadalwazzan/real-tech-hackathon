import Icon from "./Icon";

export default function MetricCard({ metric, index }) {
  return (
    <div
      className="glass-panel flex flex-col gap-3 rounded-2xl p-4 text-slate-700 animate-floatIn"
      style={{ animationDelay: `${120 + index * 80}ms` }}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-100 text-slate-600">
            <Icon name={metric.icon} />
          </div>
          <span>{metric.name}</span>
        </div>
        <span className="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold text-white">
          {metric.score}
        </span>
      </div>
      <p className="text-xs leading-relaxed text-slate-500">{metric.description}</p>
    </div>
  );
}
