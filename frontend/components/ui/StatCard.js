export default function StatCard({ title, value, icon: Icon, trend, color = "brand" }) {
  const colorMap = {
    brand: "text-brand-400 bg-brand-500/10 border-brand-500/20",
    emerald: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
    amber: "text-amber-400 bg-amber-500/10 border-amber-500/20",
    purple: "text-purple-400 bg-purple-500/10 border-purple-500/20",
    rose: "text-rose-400 bg-rose-500/10 border-rose-500/20",
  };

  return (
    <div className="glass-panel p-5 rounded-xl border border-slate-800 flex items-center justify-between">
      <div>
        <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">{title}</p>
        <h3 className="text-2xl font-bold text-white mt-1">{value}</h3>
        {trend && <p className="text-xs text-emerald-400 mt-1 font-medium">{trend}</p>}
      </div>
      {Icon && (
        <div className={`p-3 rounded-xl border ${colorMap[color] || colorMap.brand}`}>
          <Icon className="w-6 h-6" />
        </div>
      )}
    </div>
  );
}
