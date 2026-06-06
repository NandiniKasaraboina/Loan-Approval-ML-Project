from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoanData(BaseModel):
    age: float
    income: float
    experience: int
    loan_amount: float
    interest_rate: float
    credit_history_length: float
    credit_score: int

    gender: str
    education: str
    home_ownership: str
    loan_intent: str
    previous_default: str


model = joblib.load("loan_model.pkl")
scaler = joblib.load("scaler.pkl")


@app.get("/")
def home():
    return {
        "message": "Loan Approval API Running"
    }


@app.post("/predict")
def predict(data: LoanData):

    # Calculate Loan Percent Income
    loan_percent_income = (
        data.loan_amount / data.income
    )

    # Gender Encoding
    person_gender_male = (
        1 if data.gender.lower() == "male" else 0
    )

    # Education Encoding
    person_education_Bachelor = (
        1 if data.education == "Bachelor" else 0
    )

    person_education_Doctorate = (
        1 if data.education == "Doctorate" else 0
    )

    person_education_High_School = (
        1 if data.education == "High School" else 0
    )

    person_education_Master = (
        1 if data.education == "Master" else 0
    )

    # Home Ownership Encoding
    person_home_ownership_OTHER = (
        1 if data.home_ownership == "Other" else 0
    )

    person_home_ownership_OWN = (
        1 if data.home_ownership == "Own" else 0
    )

    person_home_ownership_RENT = (
        1 if data.home_ownership == "Rent" else 0
    )

    # Loan Intent Encoding
    loan_intent_EDUCATION = (
        1 if data.loan_intent == "Education" else 0
    )

    loan_intent_HOMEIMPROVEMENT = (
        1 if data.loan_intent == "Home Improvement" else 0
    )

    loan_intent_MEDICAL = (
        1 if data.loan_intent == "Medical" else 0
    )

    loan_intent_PERSONAL = (
        1 if data.loan_intent == "Personal" else 0
    )

    loan_intent_VENTURE = (
        1 if data.loan_intent == "Venture" else 0
    )

    # Previous Default Encoding
    previous_loan_defaults_on_file_Yes = (
        1 if data.previous_default == "Yes" else 0
    )

    # Create Feature Array
    features = [[
        data.age,
        data.income,
        data.experience,
        data.loan_amount,
        data.interest_rate,
        loan_percent_income,
        data.credit_history_length,
        data.credit_score,

        person_gender_male,

        person_education_Bachelor,
        person_education_Doctorate,
        person_education_High_School,
        person_education_Master,

        person_home_ownership_OTHER,
        person_home_ownership_OWN,
        person_home_ownership_RENT,

        loan_intent_EDUCATION,
        loan_intent_HOMEIMPROVEMENT,
        loan_intent_MEDICAL,
        loan_intent_PERSONAL,
        loan_intent_VENTURE,

        previous_loan_defaults_on_file_Yes
    ]]

    # Scale Data
    scaled_data = scaler.transform(
        features
    )

    # Prediction
    prediction = model.predict(
        scaled_data
    )

    print("\n===================")
    print("Features:")
    print(features)
    print("Prediction:", prediction)
    print("===================\n")

    # Return Result
    return {
        "prediction": int(prediction[0]),
        "result": (
            "Approved"
            if prediction[0] == 0
            else "Rejected"
        )
    }

