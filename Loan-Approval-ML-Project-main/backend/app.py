from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

MAX_MONTHLY_OBLIGATIONS_RATIO_FOR_AUTO_APPROVAL = 0.30
MIN_APPROVAL_CREDIT_SCORE = 700

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoanData(BaseModel):
    income: float = Field(gt=0, allow_inf_nan=False)
    loan_amount: float = Field(gt=0, allow_inf_nan=False)
    loan_term_years: float = Field(gt=0, le=30, allow_inf_nan=False)
    other_monthly_debt: float = Field(ge=0, allow_inf_nan=False)
    credit_score: int = Field(ge=300, le=850)
    experience: float = Field(ge=0, allow_inf_nan=False)
    interest_rate: float = Field(ge=0, le=100, allow_inf_nan=False)
    credit_history_length: float = Field(ge=0, allow_inf_nan=False)
    previous_default_status: Literal["None", "Resolved", "Unresolved"]
    loan_intent: Literal[
        "DEBTCONSOLIDATION",
        "EDUCATION",
        "HOMEIMPROVEMENT",
        "MEDICAL",
        "PERSONAL",
        "VENTURE",
    ]
    home_ownership: Literal["MORTGAGE", "OTHER", "OWN", "RENT"]


def calculate_monthly_payment(
    loan_amount: float,
    annual_interest_rate: float,
    term_years: float,
) -> float:
    number_of_payments = term_years * 12
    monthly_interest_rate = annual_interest_rate / 100 / 12
    if monthly_interest_rate == 0:
        return loan_amount / number_of_payments
    rate_factor = (1 + monthly_interest_rate) ** number_of_payments
    return loan_amount * (
        monthly_interest_rate * rate_factor / (rate_factor - 1)
    )


model_artifact = joblib.load(Path(__file__).with_name("loan_model.pkl"))
model = model_artifact["model"]
feature_columns = model_artifact["feature_columns"]


@app.get("/")
def home():
    return {
        "message": "Loan Approval API Running"
    }


@app.post("/predict")
def predict(data: LoanData):
    loan_percent_income = data.loan_amount / data.income
    monthly_payment = calculate_monthly_payment(
        data.loan_amount,
        data.interest_rate,
        data.loan_term_years,
    )
    monthly_gross_income = data.income / 12
    monthly_obligations_ratio = (
        monthly_payment + data.other_monthly_debt
    ) / monthly_gross_income
    payment_suggestion = (
        f"Estimated monthly payment: ${monthly_payment:,.2f}. "
        "Check that it fits your monthly budget."
    )
    features = pd.DataFrame(
        [
            {
                "person_income": data.income,
                "loan_amnt": data.loan_amount,
                "loan_term_years": data.loan_term_years,
                "other_monthly_debt": data.other_monthly_debt,
                "credit_score": data.credit_score,
                "cb_person_cred_hist_length": data.credit_history_length,
                "person_emp_exp": data.experience,
                "loan_int_rate": data.interest_rate,
                "previous_default_status": data.previous_default_status,
                "loan_intent": data.loan_intent,
                "person_home_ownership": data.home_ownership,
                "loan_percent_income": loan_percent_income,
            }
        ],
        columns=feature_columns,
    )
    prediction = int(model.predict(features)[0])
    rule_approved = (
        monthly_obligations_ratio
        <= MAX_MONTHLY_OBLIGATIONS_RATIO_FOR_AUTO_APPROVAL
        and data.credit_score >= MIN_APPROVAL_CREDIT_SCORE
        and data.previous_default_status == "None"
    )
    if data.previous_default_status == "Unresolved":
        prediction = 1
    elif rule_approved:
        prediction = 0

    if data.previous_default_status == "Unresolved":
        suggestions = [
            payment_suggestion,
            "Contact the lender to resolve the account and update your credit record; "
            "dispute any inaccurate information.",
        ]
    elif prediction == 1:
        suggestions = [
            payment_suggestion,
            "Consider a lower loan amount, a longer term, or reducing other monthly "
            "debt before applying again.",
        ]
    else:
        suggestions = [
            payment_suggestion,
            "Continue making payments on time and review the repayment terms with "
            "your lender.",
        ]

    print("\n===================")
    print("Loan-to-income ratio:", loan_percent_income)
    print("Monthly obligations ratio:", monthly_obligations_ratio)
    print("Prediction:", prediction)
    print("===================\n")

    # Return Result
    return {
        "prediction": prediction,
        "result": (
            "Approved"
            if prediction == 0
            else "Rejected"
        ),
        "suggestions": suggestions,
    }

