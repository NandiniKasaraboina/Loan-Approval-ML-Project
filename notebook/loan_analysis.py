import pandas as pd 

import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score

from sklearn.metrics import confusion_matrix




df = pd.read_csv("../dataset/loan_data.csv")



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

# remove the >100 personage from dataset
df = df[df["person_age"] <= 100]


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
print("CATEGORICAL COLUMNS")

# print(
#     df.select_dtypes(include="object").columns
# )
# print(df.select_dtypes(include=["object", "string"]).columns)


# home_encoded = pd.get_dummies(
#     df["person_home_ownership"],
#     dtype=int
# )

# print(home_encoded.head())



df_encoded = pd.get_dummies(
    df,
    drop_first=True,
    dtype=int
)

# print("\n")
# print("ENCODED DATASET SHAPE")
# print(df_encoded.shape)

# print("\n")
# print(df_encoded.head())



X = df_encoded.drop("loan_status", axis=1)

y = df_encoded["loan_status"]

# print("FEATURES SHAPE:")
# print(X.shape)

# print("\nTARGET SHAPE:")
# print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# print("X_train shape:", X_train.shape)
# print("X_test shape:", X_test.shape)
# print("y_train shape:", y_train.shape)
# print("y_test shape:", y_test.shape)


from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)


# model = LogisticRegression(max_iter=1000)
# model.fit(X_train, y_train)


model_scaled = LogisticRegression(max_iter=1000)
model_scaled.fit(X_train_scaled, y_train)
# print("Model Training Completed!")


# y_pred = model.predict(X_test)
y_pred_scaled = model_scaled.predict(X_test_scaled)
# print("First 10 Predictions:")
# print(y_pred[:10])



# accuracy = accuracy_score(
#     y_test,
#     y_pred
# )
# print("Accuracy:", accuracy)


accuracy = accuracy_score(
    y_test,
    y_pred_scaled
)
print("Accuracy:", accuracy)


# cm = confusion_matrix(
#     y_test,
#     y_pred
# )
# print("Confusion Matrix:")
# print(cm)

cm = confusion_matrix(
    y_test,
    y_pred_scaled
)
print("Confusion Matrix:")
print(cm)


# from sklearn.metrics import precision_score
# precision = precision_score(
#     y_test,
#     y_pred
# )
# print("Precision:", precision)



from sklearn.metrics import precision_score
precision = precision_score(
    y_test,
    y_pred_scaled
)

print("Precision:", precision)


# from sklearn.metrics import recall_score
# recall = recall_score(
#     y_test,
#     y_pred
# )
# print("Recall:", recall)



from sklearn.metrics import recall_score
recall = recall_score(
    y_test,
    y_pred_scaled
)
print("Recall:", recall)



# from sklearn.metrics import f1_score
# f1 = f1_score(
#     y_test,
#     y_pred
# )
# print("F1 Score:", f1)



from sklearn.metrics import f1_score
f1 = f1_score(
    y_test,
    y_pred_scaled
)
print("F1 Score:", f1)


feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": model_scaled.coef_[0]
})

feature_importance = feature_importance.sort_values(
    by="Coefficient",
    ascending=False
)

print(feature_importance.head(10))


# print("\n")
# print("MOST NEGATIVE FEATURES")

# print(
#     feature_importance.tail(10)
# )



import joblib
import joblib

joblib.dump(
    model_scaled,
    "loan_model.pkl"
)

print("Model Saved Successfully!")

joblib.dump(
    scaler,
    "scaler.pkl"
)

print("Scaler Saved Successfully!")

loaded_model = joblib.load(
    "loan_model.pkl"
)

print(type(loaded_model))


print(
    df.groupby("loan_status")["credit_score"].mean()
)