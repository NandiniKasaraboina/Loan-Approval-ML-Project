function PredictionCard({ prediction }) {
  const isApproved = prediction?.prediction === 0;

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
              isApproved ? "text-green-400" : "text-red-400"
            }`}
          >
            {isApproved ? "Approved ✅" : "Rejected ❌"}
          </div>

          {Array.isArray(prediction.suggestions) &&
            prediction.suggestions.length > 0 && (
              <div className="mt-6">
                <h3 className="text-lg font-semibold text-white mb-2">
                  Suggestions
                </h3>
                <ul className="list-disc pl-5 text-slate-300 space-y-1">
                  {prediction.suggestions.map((suggestion) => (
                    <li key={suggestion}>{suggestion}</li>
                  ))}
                </ul>
              </div>
            )}

        </div>
      )}
    </div>
  );
}

export default PredictionCard;