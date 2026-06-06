import { useState } from "react";
import axios from "axios";

function LoanForm({ setPrediction }) {
  const [formData, setFormData] = useState({
    age: "",
    income: "",
    experience: "",
    loan_amount: "",
    interest_rate: "",
    credit_history_length: "",
    credit_score: "",

    gender: "Male",
    education: "Bachelor",
    home_ownership: "Rent",
    loan_intent: "Personal",
    previous_default: "No",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        {
          age: Number(formData.age),
          income: Number(formData.income),
          experience: Number(formData.experience),
          loan_amount: Number(formData.loan_amount),
          interest_rate: Number(formData.interest_rate),
          credit_history_length: Number(
            formData.credit_history_length
          ),
          credit_score: Number(formData.credit_score),

          gender: formData.gender,
          education: formData.education,
          home_ownership: formData.home_ownership,
          loan_intent: formData.loan_intent,
          previous_default: formData.previous_default,
        }
      );

      setPrediction(response.data);
    } catch (error) {

      console.log("Full Error:", error);

      if (error.response) {

        console.log(
          "Backend Error:",
          error.response.data
        );

        alert(
          JSON.stringify(
            error.response.data,
            null,
            2
          )
        );

      } else {

        alert(error.message);

      }

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
          label="Age"
          name="age"
          value={formData.age}
          onChange={handleChange}
        />

        <InputField
          label="Income"
          name="income"
          value={formData.income}
          onChange={handleChange}
        />

        <InputField
          label="Experience"
          name="experience"
          value={formData.experience}
          onChange={handleChange}
        />

        <InputField
          label="Loan Amount"
          name="loan_amount"
          value={formData.loan_amount}
          onChange={handleChange}
        />

        <InputField
          label="Interest Rate"
          name="interest_rate"
          value={formData.interest_rate}
          onChange={handleChange}
        />

        <InputField
          label="Credit Score"
          name="credit_score"
          value={formData.credit_score}
          onChange={handleChange}
        />

        <InputField
          label="Credit History Length"
          name="credit_history_length"
          value={formData.credit_history_length}
          onChange={handleChange}
        />

        <SelectField
          label="Gender"
          name="gender"
          value={formData.gender}
          onChange={handleChange}
          options={["Male", "Female"]}
        />

        <SelectField
          label="Education"
          name="education"
          value={formData.education}
          onChange={handleChange}
          options={[
            "Associate",
            "Bachelor",
            "Master",
            "Doctorate",
            "High School",
          ]}
        />

        <SelectField
          label="Home Ownership"
          name="home_ownership"
          value={formData.home_ownership}
          onChange={handleChange}
          options={[
            "Rent",
            "Own",
            "Mortgage",
            "Other",
          ]}
        />

        <SelectField
          label="Loan Intent"
          name="loan_intent"
          value={formData.loan_intent}
          onChange={handleChange}
          options={[
            "Personal",
            "Education",
            "Medical",
            "Venture",
            "Home Improvement",
            "Debt Consolidation",
          ]}
        />

        <SelectField
          label="Previous Default"
          name="previous_default"
          value={formData.previous_default}
          onChange={handleChange}
          options={["Yes", "No"]}
        />

      </div>

      <button
        type="submit"
        className="mt-8 w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:scale-[1.02] transition-all duration-300 text-white font-semibold py-4 rounded-xl"
      >
        Predict Loan Approval
      </button>
    </form>
  );
}

function InputField({
  label,
  name,
  value,
  onChange,
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
        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-cyan-400"
      />
    </div>
  );
}

function SelectField({
  label,
  name,
  value,
  onChange,
  options,
}) {
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