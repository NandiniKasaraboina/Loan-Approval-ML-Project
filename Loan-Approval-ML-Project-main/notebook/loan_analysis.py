from pathlib import Path
import warnings

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler



PROJECT_ROOT = Path(__file__).resolve().parent.parent
template_path = PROJECT_ROOT / "dataset" / "loan_training_template.csv"
legacy_data_path = PROJECT_ROOT / "dataset" / "loan_data.csv"

if template_path.exists():
    template_df = pd.read_csv(template_path)
else:
    template_df = pd.DataFrame()

use_enhanced_dataset = not template_df.empty
if use_enhanced_dataset:
    df = template_df.copy()
    training_source = "loan_training_template.csv"
else:
    df = pd.read_csv(legacy_data_path)
    training_source = "loan_data.csv"
    warnings.warn(
        "The enhanced training template is empty; using the original dataset. "
        "Loan term, existing monthly debt, and resolved-default status will not "
        "be learned by this model.",
        stacklevel=1,
    )



# print("First five rows are:")
# print(df.head())
# print("\n")


# print("Dataset shape:")
# print(df.shape)

# print("dataset information:")
# df.info()

# print("col names")
# print(df.columns)

# print("statistical summary:")
# print(df.describe())

# print("missing values")
# print(df.isnull().sum())


# print("Loan Counts")
# print(df["loan_status"].value_counts())


# print("loan percentages:")
# print(df["loan_status"].value_counts(normalize=True))



# print("gender count")
# print(df["person_gender"].value_counts())



# print("unique values")
# print(df["person_gender"].unique())

# print("\n")
# print("EDUCATION COUNTS")
# print(df["person_education"].value_counts())


# print("\n")
# print("EDUCATION VS LOAN APPROVAL")
# print(
#     df.groupby("person_education")["loan_status"].mean()
# )


# print("credit score:")
# print(df["credit_score"].describe())


# print("\n")
# print("AVERAGE CREDIT SCORE BY LOAN STATUS")
# print(
#     df.groupby("loan_status")["credit_score"].mean()
# )


# print("\n")
# print("AVERAGE INCOME BY LOAN STATUS")
# print(
#     df.groupby("loan_status")["person_income"].mean()
# )


# print("\n")
# print("PREVIOUS DEFAULTS VS LOAN STATUS")

# print(
#     df.groupby("loan_status")["previous_loan_defaults_on_file"]
#     .value_counts(normalize=True)
# )


# print("\n")
# print("AVERAGE LOAN PERCENT INCOME BY LOAN STATUS")
# print(
#     df.groupby("loan_status")["loan_percent_income"].mean()
# )


# plt.figure(figsize=(6,4))

# sns.countplot(
#     x="loan_status",
#     data=df
# )

# plt.title("Loan Status Distribution")

# plt.show()



# plt.figure(figsize=(8,5))

# plt.hist(df["person_age"])

# plt.title("Age Distribution")

# plt.xlabel("Age")

# plt.ylabel("Count")

# plt.show()


# plt.figure(figsize=(8,5))

# sns.boxplot(
#     x=df["person_age"]
# )

# plt.title("Age Box Plot")

# plt.show()


# print("\n")
# print("AGES GREATER THAN 100")

# print(
#     df[df["person_age"] > 100]
# )

# print("\n")
# print("NEW DATASET SHAPE")
# print(df.shape)



# print("\n")
# print("CHECKING AGES ABOVE 100")

# print(
#     df[df["person_age"] > 100]
# )


# print("\n")
# print("HOME OWNERSHIP VALUES")

# print(
#     df["person_home_ownership"].unique()
# )


print("\n")
if use_enhanced_dataset:
    required_columns = [
        "person_income",
        "loan_amnt",
        "loan_term_years",
        "other_monthly_debt",
        "credit_score",
        "cb_person_cred_hist_length",
        "person_emp_exp",
        "loan_int_rate",
        "previous_default_status",
        "loan_intent",
        "person_home_ownership",
        "loan_status",
    ]
    missing_columns = sorted(set(required_columns) - set(df.columns))
    if missing_columns:
        raise ValueError(
            "Enhanced training data is missing columns: "
            + ", ".join(missing_columns)
        )

    numeric_features = [
        "person_income",
        "loan_amnt",
        "loan_term_years",
        "other_monthly_debt",
        "credit_score",
        "cb_person_cred_hist_length",
        "person_emp_exp",
        "loan_int_rate",
    ]
    for column in numeric_features + ["loan_status"]:
        df[column] = pd.to_numeric(df[column], errors="raise")

    if df[required_columns].isnull().any().any():
        raise ValueError("Enhanced training data must not contain blank cells.")
    if not np.isfinite(df[numeric_features + ["loan_status"]].to_numpy()).all():
        raise ValueError("Enhanced training data must contain only finite numbers.")
    if (
        (df["person_income"] <= 0).any()
        or (df["loan_amnt"] <= 0).any()
        or (df["loan_term_years"] <= 0).any()
        or (df["loan_term_years"] > 30).any()
        or (df["other_monthly_debt"] < 0).any()
        or (~df["credit_score"].between(300, 850)).any()
        or (df["cb_person_cred_hist_length"] < 0).any()
        or (df["person_emp_exp"] < 0).any()
        or (~df["loan_int_rate"].between(0, 100)).any()
        or (~df["loan_status"].isin([0, 1])).any()
    ):
        raise ValueError("Enhanced training data contains out-of-range values.")

    allowed_categories = {
        "previous_default_status": {"None", "Resolved", "Unresolved"},
        "loan_intent": {
            "DEBTCONSOLIDATION",
            "EDUCATION",
            "HOMEIMPROVEMENT",
            "MEDICAL",
            "PERSONAL",
            "VENTURE",
        },
        "person_home_ownership": {"MORTGAGE", "OTHER", "OWN", "RENT"},
    }
    for column, allowed_values in allowed_categories.items():
        unexpected_values = set(df[column].unique()) - allowed_values
        if unexpected_values:
            raise ValueError(
                f"Invalid values in {column}: {sorted(unexpected_values)}"
            )
    if df["loan_status"].value_counts().min() < 2:
        raise ValueError(
            "Enhanced training data needs at least two records for each outcome "
            "(approved and rejected) to create a stratified test split."
        )

    feature_columns = [
        "person_income",
        "loan_amnt",
        "loan_term_years",
        "other_monthly_debt",
        "credit_score",
        "cb_person_cred_hist_length",
        "person_emp_exp",
        "loan_int_rate",
        "previous_default_status",
        "loan_intent",
        "person_home_ownership",
        "loan_percent_income",
    ]
    categorical_features = [
        "previous_default_status",
        "loan_intent",
        "person_home_ownership",
    ]
else:
    default_outcomes = pd.crosstab(
        df["previous_loan_defaults_on_file"],
        df["loan_status"],
    )
    print("Previous-default status by target:")
    print(default_outcomes)
    if (default_outcomes == 0).any(axis=None):
        warnings.warn(
            "Some previous-default groups have no examples for one loan outcome. "
            "The default field is excluded from model training to avoid learning "
            "an unsupported relationship.",
            stacklevel=1,
        )

    feature_columns = [
        "person_income",
        "loan_amnt",
        "credit_score",
        "cb_person_cred_hist_length",
        "person_emp_exp",
        "loan_int_rate",
        "loan_intent",
        "person_home_ownership",
        "loan_percent_income",
    ]
    categorical_features = [
        "loan_intent",
        "person_home_ownership",
    ]
    numeric_features = [
        "person_income",
        "loan_amnt",
        "credit_score",
        "cb_person_cred_hist_length",
        "person_emp_exp",
        "loan_int_rate",
    ]

df["loan_percent_income"] = df["loan_amnt"] / df["person_income"]
numeric_features.append("loan_percent_income")
X = df[feature_columns]
y = df["loan_status"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", StandardScaler(), numeric_features),
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                drop="first",
                sparse_output=False,
            ),
            categorical_features,
        ),
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            HistGradientBoostingClassifier(
                max_iter=150,
                learning_rate=0.08,
                l2_regularization=1.0,
                random_state=42,
            ),
        ),
    ]
)
model.fit(X_train, y_train)

max_train_loan_percent_income = float(X_train["loan_percent_income"].max())
y_pred = model.predict(X_test)

print("Training source:", training_source)
print("Training rows:", len(df))
print("Training features:", feature_columns)
print("Maximum training loan-to-income ratio:", max_train_loan_percent_income)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision (rejected):", precision_score(y_test, y_pred))
print("Recall (rejected):", recall_score(y_test, y_pred))
print("F1 (rejected):", f1_score(y_test, y_pred))
print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred))

joblib.dump(
    {
        "model": model,
        "feature_columns": feature_columns,
        "max_train_loan_percent_income": max_train_loan_percent_income,
        "training_source": training_source,
    },
    PROJECT_ROOT / "backend" / "loan_model.pkl",
)
print("Selected-feature model saved.")