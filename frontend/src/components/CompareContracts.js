import React, { useState } from "react";
import { compareContracts } from "../api/api";

function CompareContracts() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [result, setResult] = useState("");

  const handleCompare = async () => {
    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);
    const res = await compareContracts(formData);
    setResult(JSON.stringify(res.data, null, 2));
  };

  return (
    <div className="card">
      <h3>Compare Contracts</h3>
      <input type="file" onChange={(e) => setFile1(e.target.files[0])} />
      <input type="file" onChange={(e) => setFile2(e.target.files[0])} />
      <button onClick={handleCompare}>Compare</button>
      <pre>{result}</pre>
    </div>
  );
}

export default CompareContracts;