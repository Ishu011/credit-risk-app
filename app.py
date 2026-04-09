import streamlit as st
import pandas as pd
import pickle


#LOAD MODEL
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Credit Risk Predictor", layout="centered")

st.title("💳 Credit Risk Prediction App")
st.write("Enter customer details to predict default risk")


#USER INPUTS

age = st.slider("Age", 18, 70)

gender = st.selectbox("Gender", ["Male", "Female"])
owns_car = st.selectbox("Owns Car", ["Yes", "No"])
owns_house = st.selectbox("Owns House", ["Yes", "No"])

income = st.number_input("Annual Income", min_value=0.0)
credit_score = st.slider("Credit Score", 300, 900)

credit_limit = st.number_input("Credit Limit", min_value=0.0)
credit_used = st.slider("Credit Used (%)", 0, 100)

debt = st.number_input("Yearly Debt Payments", min_value=0.0)
days_employed = st.number_input("Days Employed", min_value=0.0)

prev_defaults = st.selectbox("Previous Defaults", [0, 1])
recent_default = st.selectbox("Default in last 6 months", [0, 1])

#ENCODING
gender = 1 if gender == "Male" else 0
owns_car = 1 if owns_car == "Yes" else 0
owns_house = 1 if owns_house == "Yes" else 0

#FEATURE ENGINEERING

credit_utilization = credit_used / 100
debt_to_income = debt / income if income != 0 else 0
income_per_family = income / 1


#PREDICTION BUTTON
# =========================
# PREDICTION BUTTON
# =========================
if st.button("Predict Risk"):

    input_data = pd.DataFrame({
    "age": [age],
    "gender": [gender],
    "owns_car": [owns_car],
    "owns_house": [owns_house],
    "no_of_children": [0],
    "net_yearly_income": [income],
    "no_of_days_employed": [days_employed],
    "occupation_type": [0],
    "total_family_members": [1],
    "migrant_worker": [0],
    "yearly_debt_payments": [debt],
    "credit_limit": [credit_limit],
    "credit_limit_used(%)": [credit_used],
    "credit_score": [credit_score],
    "prev_defaults": [prev_defaults],
    "default_in_last_6months": [recent_default],
    "credit_utilization": [credit_utilization],
    "debt_to_income": [debt_to_income],
    "income_per_family": [income_per_family]
})

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    def risk_category(prob):
        if prob < 0.3:
            return "Low Risk"
        elif prob < 0.7:
            return "Medium Risk"
        else:
            return "High Risk"

    risk = risk_category(probability)

    st.subheader("Result")

    if prediction == 1:
        st.error(" High Risk Customer")
    else:
        st.success(" Low Risk Customer")

    st.write(f" Default Probability: {probability:.2f}")
    st.write(f" Risk Category: {risk}")