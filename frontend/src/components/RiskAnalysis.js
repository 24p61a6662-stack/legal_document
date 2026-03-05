import React, { useState } from "react";
import { analyzeRisk } from "../api/api";

function RiskAnalysis() {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");

  const handleAnalyze = async () => {
    const res = await analyzeRisk(text);
    setResult(JSON.stringify(res.data, null, 2));
  };

  return (
    <div className="card">
      <h3>Risk Analysis</h3>
      <textarea rows="3" onChange={(e) => setText(e.target.value)} />
      <button onClick={handleAnalyze}>Analyze</button>
      <pre>{result}</pre>
    </div>
  );
}

export default RiskAnalysis;