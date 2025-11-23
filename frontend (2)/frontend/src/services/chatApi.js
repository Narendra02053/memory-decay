import axios from "axios";

const baseURL =
  (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
const chatClient = axios.create({
  baseURL,
  headers: { "Content-Type": "application/json" },
});

export async function sendChat({ email, message }) {
  try {
    const res = await chatClient.post("/api/chat/", { email, message });
    return res.data;
  } catch (error) {
    console.error("Chat API error:", error);
    if (error.response) {
      throw new Error(error.response.data?.detail || error.response.data?.message || "Chat service error");
    } else if (error.request) {
      throw new Error("Unable to connect to chat service. Please check if the backend is running.");
    } else {
      throw new Error("An error occurred while sending the message.");
    }
  }
}

export async function fetchHistory(email) {
  if (!email) return [];
  try {
    const res = await chatClient.get(`/api/chat/${encodeURIComponent(email)}`);
    return res.data.history ?? [];
  } catch (error) {
    console.error("Fetch history error:", error);
    if (error.response && error.response.status === 404) {
      return []; // No history yet, return empty array
    }
    throw error;
  }
}
