import React, { useEffect, useRef, useState } from "react";
import { fetchHistory, sendChat } from "../services/chatApi";

export default function Chat() {
  const [email, setEmail] = useState("");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");
  const historyRef = useRef(null);

  useEffect(() => {
    async function loadHistory() {
      if (!email) {
        setMessages([]);
        return;
      }
      try {
        setStatus("loading");
        setError("");
        const history = await fetchHistory(email);
        setMessages(
          history.map((item) => ({
            sender: item.sender,
            text: item.message,
          }))
        );
      } catch (err) {
        console.error("Failed to load chat history", err);
        // Don't show error for empty history, just log it
        if (err.response?.status !== 404) {
          setError("Unable to load previous messages.");
        }
      } finally {
        setStatus("idle");
      }
    }
    loadHistory();
  }, [email]);

  useEffect(() => {
    historyRef.current?.scrollTo({
      top: historyRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  async function handleSend() {
    if (!input.trim() || !email) {
      setError("Please enter both an email and a message.");
      return;
    }

    setError("");
    const userMsg = { sender: "user", text: input.trim() };
    setMessages((prev) => [...prev, userMsg]);
    const messageToSend = input.trim();
    setInput("");
    setStatus("sending");

    try {
      const res = await sendChat({ email, message: messageToSend });
      console.log("Chat response:", res);
      
      if (res && res.status === "error") {
        const botMsg = { sender: "bot", text: res.reply || "An error occurred." };
        setMessages((prev) => [...prev, botMsg]);
        setError(res.reply || "An error occurred.");
      } else if (res && res.reply) {
        const botMsg = { sender: "bot", text: res.reply };
        setMessages((prev) => [...prev, botMsg]);
        setError(""); // Clear any previous errors
      } else {
        throw new Error("Invalid response from chat service");
      }
    } catch (err) {
      console.error("Send chat failed", err);
      const errorMsg = err.message || "Couldn't reach the chatbot. Please check if the backend is running.";
      setError(errorMsg);
      // Add error message as bot response
      const errorBotMsg = { sender: "bot", text: `Error: ${errorMsg}` };
      setMessages((prev) => [...prev, errorBotMsg]);
    } finally {
      setStatus("idle");
    }
  }

  function handleKeyPress(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (input.trim() && email && status !== "sending") {
        handleSend();
      }
    }
  }

  return (
    <main className="page">
      <div className="page-header">
        <h1>AI Chatbot</h1>
        <p>Capture study notes or ask questions — your history stays tied to your email.</p>
      </div>

      <section className="card chat-card">
        <div className="form-grid">
          <div className="input-group" style={{ gridColumn: "1 / -1" }}>
            <label htmlFor="chat-email">Email for history</label>
            <input
              id="chat-email"
              className="input"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <span className="status-text">We use this to load your conversations.</span>
          </div>
        </div>

        {error && <p className="status-text status-text--error">{error}</p>}

        <div className="chat-history" ref={historyRef}>
          {messages.length === 0 && (
            <p className="status-text">No messages yet. Say hello to start the chat.</p>
          )}
          {messages.map((msg, i) => (
            <div key={`${msg.sender}-${i}`} className={`bubble bubble--${msg.sender}`}>
              <strong>{msg.sender === "user" ? "You" : "Bot"}:</strong> {msg.text}
            </div>
          ))}
        </div>

        <div className="chat-input-row">
          <input
            className="input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask anything..."
            disabled={status === "sending"}
          />
          <button className="btn" onClick={handleSend} disabled={status === "sending" || !input.trim() || !email}>
            {status === "sending" ? (
              <>
                <span className="loading"></span>
                Sending...
              </>
            ) : (
              "💬 Send"
            )}
          </button>
        </div>

        <p className="status-text">
          {status === "loading"
            ? "Loading your previous messages..."
            : "Powered by your local study assistant — responses appear instantly."}
        </p>
      </section>
    </main>
  );
}
