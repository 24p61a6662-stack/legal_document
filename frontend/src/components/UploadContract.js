import React, { useState } from "react";
import { uploadContract } from "../api/api";

function UploadContract() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await uploadContract(formData);
    setMessage(res.data.message);
  };

  return (
    <div className="card">
      <h3>Upload Contract</h3>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
      <p>{message}</p>
    </div>
  );
}

export default UploadContract;