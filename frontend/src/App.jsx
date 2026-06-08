import { useState } from "react";
import LoanForm from "./components/LoanForm";
import PredictionCard from "./components/PredictionCard";

function App() {
  const [prediction, setPrediction] = useState(null);

  return (
    <div className="min-h-screen bg-slate-950">

      <div className="fixed inset-0 overflow-hidden">
        <div className="absolute top-0 left-0 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10">

        <section className="max-w-7xl mx-auto px-6 pt-16 pb-12">

          <div className="text-center">

            <h1 className="text-5xl md:text-6xl font-black text-white">
              Loan Approval
              <span className="block bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 bg-clip-text text-transparent">
                Prediction System
              </span>
            </h1>

          </div>

        </section>

        <section className="max-w-7xl mx-auto px-6 pb-16">

          <div className="grid lg:grid-cols-3 gap-8">

            <div className="lg:col-span-2">
              <LoanForm setPrediction={setPrediction} />
            </div>

            <PredictionCard prediction={prediction} />

          </div>

        </section>

      </div>

    </div>
  );
}

export default App;