import { useState } from "react";
import axios from "axios";

function LoanForm({ setPrediction }) {
  const [errorMessage, setErrorMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    income: "",
    loan_amount: "",
    loan_term_years: "",
    other_monthly_debt: "",
    credit_score: "",
    credit_history_length: "",
    experience: "",
    interest_rate: "",
    previous_default_status: "None",
    loan_intent: "PERSONAL",
    home_ownership: "RENT",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setPrediction(null);
    setIsSubmitting(true);

    try {
      const apiUrl =
        import.meta.env.VITE_API_URL || "http://localhost:8000/predict";

      const response = await axios.post(apiUrl, {
          income: Number(formData.income),
          loan_amount: Number(formData.loan_amount),
          loan_term_years: Number(formData.loan_term_years),
          other_monthly_debt: Number(formData.other_monthly_debt),
          credit_score: Number(formData.credit_score),
          credit_history_length: Number(formData.credit_history_length),
          experience: Number(formData.experience),
          interest_rate: Number(formData.interest_rate),
          previous_default_status: formData.previous_default_status,
          loan_intent: formData.loan_intent,
          home_ownership: formData.home_ownership,
        });

      setPrediction(response.data);
    } catch (error) {
      if (error.response) {
        const detail = error.response.data?.detail;
        setErrorMessage(
          Array.isArray(detail)
            ? detail
                .map((item) => `${item.loc[item.loc.length - 1]}: ${item.msg}`)
                .join(". ")
            : detail || "The prediction request failed."
        );
      } else {
        setErrorMessage(
          `Could not connect to the prediction service: ${error.message}`
        );
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-3xl p-8"
    >
      <h2 className="text-3xl font-bold text-white mb-8">
        Loan Application
      </h2>

      <div className="grid md:grid-cols-2 gap-6">
        <InputField
          label="Annual Income"
          name="income"
          value={formData.income}
          onChange={handleChange}
          min="0.01"
          step="any"
        />

        <InputField
          label="Loan Amount"
          name="loan_amount"
          value={formData.loan_amount}
          onChange={handleChange}
          min="0.01"
          step="any"
        />

        <InputField
          label="Loan Term (years)"
          name="loan_term_years"
          value={formData.loan_term_years}
          onChange={handleChange}
          min="0.1"
          max="30"
          step="any"
        />

        <InputField
          label="Other Monthly Debt Payments"
          name="other_monthly_debt"
          value={formData.other_monthly_debt}
          onChange={handleChange}
          min="0"
          step="any"
        />

        <InputField
          label="Credit Score"
          name="credit_score"
          value={formData.credit_score}
          onChange={handleChange}
          min="300"
          max="850"
        />

        <InputField
          label="Credit History Length (years)"
          name="credit_history_length"
          value={formData.credit_history_length}
          onChange={handleChange}
          min="0"
          step="any"
        />

        <InputField
          label="Employment Experience (years)"
          name="experience"
          value={formData.experience}
          onChange={handleChange}
          min="0"
          step="any"
        />

        <InputField
          label="Interest Rate (%)"
          name="interest_rate"
          value={formData.interest_rate}
          onChange={handleChange}
          min="0"
          max="100"
          step="any"
        />

        <SelectField
          label="Previous Default Status"
          name="previous_default_status"
          value={formData.previous_default_status}
          onChange={handleChange}
          options={["None", "Resolved", "Unresolved"]}
        />

        <SelectField
          label="Loan Purpose"
          name="loan_intent"
          value={formData.loan_intent}
          onChange={handleChange}
          options={[
            "PERSONAL",
            "EDUCATION",
            "MEDICAL",
            "VENTURE",
            "HOMEIMPROVEMENT",
            "DEBTCONSOLIDATION",
          ]}
        />

        <SelectField
          label="Home Ownership"
          name="home_ownership"
          value={formData.home_ownership}
          onChange={handleChange}
          options={["RENT", "OWN", "MORTGAGE", "OTHER"]}
        />
      </div>

      {errorMessage && (
        <p className="mt-6 text-red-300" role="alert">
          {errorMessage}
        </p>
      )}

      <button
        type="submit"
        disabled={isSubmitting}
        className="mt-8 w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:scale-[1.02] transition-all duration-300 text-white font-semibold py-4 rounded-xl disabled:cursor-wait disabled:opacity-70"
      >
        {isSubmitting ? "Predicting..." : "Predict Loan Approval"}
      </button>
    </form>
  );
}

function InputField({
  label,
  name,
  value,
  onChange,
  min,
  max,
  step,
}) {
  return (
    <div>
      <label className="block text-slate-300 mb-2">
        {label}
      </label>

      <input
        type="number"
        name={name}
        value={value}
        onChange={onChange}
        required
        min={min}
        max={max}
        step={step ?? "1"}
        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-cyan-400"
      />
    </div>
  );
}

function SelectField({ label, name, value, onChange, options }) {
  return (
    <div>
      <label className="block text-slate-300 mb-2">
        {label}
      </label>

      <select
        name={name}
        value={value}
        onChange={onChange}
        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-cyan-400"
      >
        {options.map((option) => (
          <option
            key={option}
            value={option}
            className="bg-slate-900"
          >
            {option}
          </option>
        ))}
      </select>
    </div>
  );
}

export default LoanForm;