import React from "react";
import "./ResultCard.css";

function ResultCard({ result }) {
  if (!result) return null;

  const loans = result.loans || [];

  return (
    <div className="result-card">
      <h3>Loan Eligibility Result</h3>
      <p><strong>Status:</strong> {result.eligible ? "✅ Eligible" : "❌ Not Eligible"}</p>
      <p><strong>CIBIL Score:</strong> {result.cibil_score}</p>
      <p><strong>Predicted Max Loan:</strong> ₹{result.predicted_amount}</p>

      <h4>Available Loan Offers:</h4>
      {loans.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Bank</th>
              <th>Loan Type</th>
              <th>Interest Rate (%)</th>
              <th>Apply</th>
            </tr>
          </thead>
          <tbody>
            {loans.map((loan, idx) => (
              <tr key={idx}>
                <td>{loan.Bank}</td>
                <td>{loan["Loan Type"]}</td>
                <td>{loan["Interest Rate"]}</td>
                <td><a href={loan.Link} target="_blank" rel="noreferrer">Apply</a></td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No loan offers available.</p>
      )}
    </div>
  );
}

export default ResultCard;
