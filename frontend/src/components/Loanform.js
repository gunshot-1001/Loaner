import React, { useState } from "react";
import { predictLoan } from "../api";
import "./ResultCard.css";

function LoanForm({ setResult }) {
  const [form, setForm] = useState({
    Gender: "Male",
    Married: "No",
    Dependents: "0",
    Education: "Graduate",
    Self_Employed: "No",
    Property_Area: "Urban",
    Credit_History: "1",
    ApplicantIncome: "",
    CoapplicantIncome: "",
    Loan_Amount_Term: "360",
    DesiredLoanAmount: "",
  });

  const [showLoanType, setShowLoanType] = useState(false);
  const [loanType, setLoanType] = useState("Home Loan");

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...form,
        ApplicantIncome: parseInt(form.ApplicantIncome) || 0,
        CoapplicantIncome: parseInt(form.CoapplicantIncome) || 0,
        Loan_Amount_Term: parseInt(form.Loan_Amount_Term) || 360,
        Credit_History: parseInt(form.Credit_History) || 1,
        DesiredLoanAmount: parseInt(form.DesiredLoanAmount) || 0,
      };
      const res = await predictLoan(payload);
      setResult(res.data);
      if (res.data.eligible) setShowLoanType(true);
    } catch (err) {
      console.error(err.response?.data || err.message);
    }
  };

  const handleLoanTypeSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...form,
        ApplicantIncome: parseInt(form.ApplicantIncome) || 0,
        CoapplicantIncome: parseInt(form.CoapplicantIncome) || 0,
        Loan_Amount_Term: parseInt(form.Loan_Amount_Term) || 360,
        Credit_History: parseInt(form.Credit_History) || 1,
        DesiredLoanAmount: parseInt(form.DesiredLoanAmount) || 0,
        LoanType: loanType,
      };
      const res = await predictLoan(payload);
      setResult(res.data);
    } catch (err) {
      console.error(err.response?.data || err.message);
    }
  };

  return (
    <div className="loan-form-container">
      <form onSubmit={handleSubmit} className="loan-form">
          {/* Main heading */}
          <h2 style={{
              textAlign: "center",
              color: "#1a73e8",
              marginBottom: "10px",
              fontSize: "1.8rem",
              fontWeight: 600
               }}>
              Check Your Loan Eligibility</h2>

        {["Gender", "Married", "Dependents", "Education", "Self_Employed", "Property_Area", "Credit_History"].map((field) => (
          <div className="input-group" key={field}>
            <label>{field.replace("_", " ")}</label>
            <select name={field} value={form[field]} onChange={handleChange}>
              {field === "Gender" && <>
                <option>Male</option>
                <option>Female</option>
              </>}
              {field === "Married" && <>
                <option>No</option>
                <option>Yes</option>
              </>}
              {field === "Dependents" && <>
                <option>0</option>
                <option>1</option>
                <option>2</option>
                <option>3+</option>
              </>}
              {field === "Education" && <>
                <option>Graduate</option>
                <option>Not Graduate</option>
              </>}
              {field === "Self_Employed" && <>
                <option>No</option>
                <option>Yes</option>
              </>}
              {field === "Property_Area" && <>
                <option>Urban</option>
                <option>Semiurban</option>
                <option>Rural</option>
              </>}
              {field === "Credit_History" && <>
                <option>1</option>
                <option>0</option>
              </>}
            </select>
          </div>
        ))}

        {["ApplicantIncome","CoapplicantIncome","Loan_Amount_Term","DesiredLoanAmount"].map((field) => (
          <div className="input-group" key={field}>
            <label>{field.replace("_", " ")}</label>
            <input type="number" name={field} value={form[field]} onChange={handleChange} placeholder="0" />
          </div>
        ))}

        <button type="submit" className="primary-btn">Check Eligibility</button>
      </form>

      {showLoanType && (
        <form onSubmit={handleLoanTypeSubmit} className="loan-type-form">
          <select value={loanType} onChange={(e) => setLoanType(e.target.value)} style={{ padding: "10px 15px", borderRadius: "8px", border: "1px solid #ccc" }}>
            <option>Home Loan</option>
            <option>Car Loan</option>
            <option>Personal Loan</option>
          </select>
          <button type="submit" className="secondary-btn">Get Loan Offers</button>
        </form>
      )}
    </div>
  );
}

export default LoanForm;
