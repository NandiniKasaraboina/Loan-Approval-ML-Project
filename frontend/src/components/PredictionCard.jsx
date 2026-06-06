function PredictionCard({ prediction }) {
  return (
    <div className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-3xl p-8">

      <h2 className="text-3xl font-bold text-white mb-6">
        Prediction Result
      </h2>

      {!prediction ? (
        <div className="text-slate-400">
          Fill the form and click Predict.
        </div>
      ) : (
        <div>

          <div
            className={`text-4xl font-bold mb-4 ${
              prediction.prediction === 0
                ? "text-green-400"
                : "text-red-400"
            }`}
          >
            {prediction.prediction === 0
              ? "Approved ✅"
              : "Rejected ❌"}
          </div>

          <div className="text-slate-300">
            {prediction.result}
          </div>

        </div>
      )}
    </div>
  );
}

export default PredictionCard;