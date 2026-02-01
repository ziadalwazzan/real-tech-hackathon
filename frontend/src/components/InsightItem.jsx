import Icon from "./Icon";

export default function InsightItem({ insight, index }) {
  return (
    <div
      className="flex items-start gap-3 rounded-2xl border border-slate-200 bg-white/70 p-4 text-sm text-slate-600 animate-floatIn"
      style={{ animationDelay: `${100 + index * 80}ms` }}
    >
      <div className="mt-1 flex h-9 w-9 items-center justify-center rounded-full bg-slate-100 text-slate-600">
        <Icon name={insight.icon} />
      </div>
      <p>{insight.text}</p>
    </div>
  );
}
