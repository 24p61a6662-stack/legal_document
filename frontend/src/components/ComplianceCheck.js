import React, { useState } from "react";
import { checkCompliance } from "../api/api";

function ComplianceCheck() {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");

  const handleCheck = async () => {
    const res = await checkCompliance(text);
    setResult(JSON.stringify(res.data, null, 2));
  };

  return (
    <div className="card">
      <h3>Compliance Check</h3>
      <textarea rows="3" onChange={(e) => setText(e.target.value)} />
      <button onClick={handleCheck}>Check</button>
      <pre>{result}</pre>
    </div>
  );
}

export default ComplianceCheck;