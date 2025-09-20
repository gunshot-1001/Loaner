import React, { useState } from "react";
import LoanForm from "./components/Loanform";
import ResultCard from "./components/ResultCard";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="App" style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>Loan Eligibility Checker</h1>
      <LoanForm setResult={setResult} />
      <ResultCard result={result} />
    </div>
  );
}

export default App;
