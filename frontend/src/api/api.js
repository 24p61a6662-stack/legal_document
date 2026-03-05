import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const uploadContract = (formData) =>
  API.post("/upload-contract", formData);

export const chatQuery = (query) =>
  API.post("/chat", { query });

export const analyzeRisk = (text) =>
  API.post("/analyze-risk", { text });

export const compareContracts = (formData) =>
  API.post("/compare-contracts", formData);

export const checkCompliance = (text) =>
  API.post("/check-compliance", { text });