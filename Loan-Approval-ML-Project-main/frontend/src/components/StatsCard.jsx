function StatsCard({ title, value, icon }) {
  return (
    <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-6">

      <div className="flex justify-between items-center">

        <div>
          <p className="text-slate-400 text-sm">
            {title}
          </p>

          <h2 className="text-3xl font-bold mt-2">
            {value}
          </h2>
        </div>

        <div className="text-cyan-400">
          {icon}
        </div>

      </div>

    </div>
  );
}

export default StatsCard;