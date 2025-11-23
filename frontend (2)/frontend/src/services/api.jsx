import axios from "axios";

const baseURL =
  (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

const api = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function predictMemory(formData) {
  try {
    const response = await api.post("/api/predict/", formData);
    return response.data;
  } catch (error) {
    console.error("Prediction API error:", error);
    if (error.response) {
      throw new Error(error.response.data?.detail || error.response.data?.message || "Prediction service error");
    } else if (error.request) {
      throw new Error("Unable to connect to prediction service. Please check if the backend is running.");
    } else {
      throw new Error("An error occurred while making the prediction.");
    }
  }
}
