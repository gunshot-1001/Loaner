# backend/app/ml/predict.py
from pathlib import Path
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# --------------------------
# Paths
# --------------------------
BASE_DIR = Path(__file__).resolve().parents[0]
MODELS_DIR = BASE_DIR.parent / "models"
DATA_DIR = BASE_DIR.parent.parent / "data" / "raw"

eligibility_model_path = MODELS_DIR / "eligibility_model.joblib"
amount_model_path = MODELS_DIR / "amount_model.joblib"
csv_path = DATA_DIR / "loan_interest_rates.csv"

# --------------------------
# Load models
# --------------------------
eligibility_model = joblib.load(eligibility_model_path)
amount_model = joblib.load(amount_model_path)

# --------------------------
# Function to calculate CIBIL score
# --------------------------
def calculate_cibil_score(user_input: dict) -> int:
    base_score = 600

    # Positive factors
    if user_input.get("Credit_History", 0) == 1:
        base_score += 100
    if user_input.get("ApplicantIncome", 0) > 4000:
        base_score += 50
    if user_input.get("CoapplicantIncome", 0) > 2000:
        base_score += 25
    if user_input.get("Education", "").lower() == "graduate":
        base_score += 25
    if user_input.get("Property_Area", "").lower() == "urban":
        base_score += 25

    # Negative factors
    if user_input.get("Loan_Amount_Term", 360) > 360:
        base_score -= 25
    if user_input.get("Dependents", "0") not in ["0", "1"]:
        base_score -= 25
    if user_input.get("Self_Employed", "No").lower() == "yes":
        base_score -= 20
    if user_input.get("ApplicantIncome", 0) == 0:
        base_score -= 50
    if user_input.get("CoapplicantIncome", 0) == 0:
        base_score -= 20
    if user_input.get("Credit_History", 0) == 0:
        base_score -= 100

    return max(300, min(900, base_score))

# --------------------------
# Flask App
# --------------------------
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Flask API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        # Map frontend fields to backend model inputs
        user_input = {
            "Gender": data.get("Gender", "Male"),
            "Married": data.get("Married", "No"),
            "Dependents": data.get("Dependents", "0"),
            "Education": data.get("Education", "Graduate"),
            "Self_Employed": data.get("Self_Employed", "No"),
            "ApplicantIncome": int(data.get("ApplicantIncome", 0)),
            "CoapplicantIncome": int(data.get("CoapplicantIncome", 0)),
            "Loan_Amount_Term": int(data.get("Loan_Amount_Term", 360)),
            "Credit_History": int(data.get("Credit_History", 1)),
            "Property_Area": data.get("Property_Area", "Urban")
        }

        desired_loan_amount = int(data.get("DesiredLoanAmount", 0))
        X_user = pd.DataFrame([user_input])

        # Predictions
        predicted_amount = amount_model.predict(X_user)[0]
        ml_eligibility = eligibility_model.predict(X_user)[0]
        cibil_score = calculate_cibil_score(user_input)

        # Final eligibility decision
        eligible = ml_eligibility == 1 and cibil_score >= 650
        reason = "Approved" if eligible else "Rejected"

        # Loan offers if eligible
        offers = []
        if eligible and csv_path.exists():
            loans_df = pd.read_csv(csv_path)
            loan_choice = data.get("LoanType", "Home Loan")
            filtered = loans_df[loans_df["Loan Type"].str.contains(loan_choice, case=False, na=False)]
            offers = filtered.head(5).to_dict(orient="records")

        return jsonify({
            "cibil_score": cibil_score,
            "predicted_amount": float(predicted_amount),
            "eligible": eligible,
            "reason": reason,
            "loans": offers
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

