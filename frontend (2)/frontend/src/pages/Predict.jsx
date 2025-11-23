import React, { useMemo, useState } from "react";
import { predictMemory } from "../services/api";

const numericFields = [
  "study_time",
  "review_count",
  "confidence",
  "stress_level",
  "sleep_hours",
  "distraction_level",
  "attention_level",
];

// Valid options for categorical fields
const domainOptions = ["school", "pu", "college", "university", "online", "self-study"];
const categoryOptions = ["science", "mathematics", "history", "literature", "language", "arts", "technology", "business", "other"];
const categoryTypeOptions = ["concept", "formula", "fact", "procedure", "principle", "theory", "other"];
const difficultyOptions = ["easy", "medium", "hard", "very hard"];
const moodOptions = ["calm", "stressed", "excited", "tired", "focused", "anxious", "confident", "neutral"];
const recentEventOptions = ["none", "exam", "test", "presentation", "assignment", "deadline", "holiday", "illness", "other"];

const fieldMeta = {
  topic_name: { label: "Topic name", placeholder: "Neuroplasticity", type: "text" },
  category: { label: "Category", type: "select", options: categoryOptions },
  domain: { label: "Domain", type: "select", options: domainOptions },
  category_type: { label: "Category type", type: "select", options: categoryTypeOptions },
  study_time: { label: "Study time (hours)", placeholder: "1.5", type: "number" },
  review_count: { label: "Review count", placeholder: "2", type: "number" },
  confidence: { label: "Confidence (1-5)", placeholder: "4", type: "number" },
  difficulty: { label: "Difficulty", type: "select", options: difficultyOptions },
  stress_level: { label: "Stress level (1-5)", placeholder: "2", type: "number" },
  sleep_hours: { label: "Sleep hours", placeholder: "7.5", type: "number" },
  mood: { label: "Mood", type: "select", options: moodOptions },
  distraction_level: { label: "Distraction level (1-5)", placeholder: "1", type: "number" },
  recent_event: { label: "Recent event", type: "select", options: recentEventOptions },
  attention_level: { label: "Attention level (1-5)", placeholder: "4", type: "number" },
};

const initialState = Object.keys(fieldMeta).reduce(
  (acc, key) => ({
    ...acc,
    [key]: key === "recent_event" ? "none" : "",
  }),
  {}
);

export default function Predict() {
  const [formData, setFormData] = useState(initialState);
  const [status, setStatus] = useState("idle");
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  }

  function handleReset() {
    setFormData(initialState);
    setPrediction(null);
    setError("");
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setStatus("loading");
    setError("");

    // Create payload with proper type conversion
    const payload = Object.fromEntries(
      Object.entries(formData).map(([key, value]) => {
        if (numericFields.includes(key)) {
          const numValue = value === "" ? 0 : Number(value);
          return [key, isNaN(numValue) ? 0 : numValue];
        }
        return [key, value || ""];
      })
    );

    // Validate required fields
    const requiredFields = Object.keys(fieldMeta).filter(
      (key) => !["recent_event", "topic_name"].includes(key)
    );
    const missingFields = requiredFields.filter((key) => !payload[key] || payload[key] === "");
    
    if (missingFields.length > 0) {
      setError(`Please fill in all required fields: ${missingFields.join(", ")}`);
      setStatus("idle");
      return;
    }

    try {
      const result = await predictMemory(payload);
      if (result && result.status === "success" && result.prediction !== undefined && result.prediction !== null) {
        setPrediction(result.prediction);
        setError("");
      } else if (result && result.status === "error") {
        throw new Error(result.message || "Prediction failed");
      } else {
        throw new Error("Invalid response from prediction service");
      }
    } catch (err) {
      console.error("Prediction request failed", err);
      const errorMsg = err.message || "Prediction failed. Please check your inputs and try again.";
      setError(errorMsg);
      setPrediction(null);
    } finally {
      setStatus("idle");
    }
  }

  const predictionCopy = useMemo(() => {
    if (prediction === null) {
      return "Complete the form on the left and we’ll estimate how long it might take before this topic starts to fade.";
    }
    if (prediction <= 3) {
      return "Review this topic soon! Spaced repetition in the next day or two will keep it fresh.";
    }
    if (prediction <= 7) {
      return "Nice work — you’ve got a few days before forgetting kicks in. Schedule a reminder mid-week.";
    }
    return "Your memory looks strong. Plan a quick recap next week to lock it in.";
  }, [prediction]);

  return (
    <main className="page">
      <div className="page-header">
        <h1>Memory Decay Predictor</h1>
        <p>Understand when to review a topic so your study sessions stay efficient.</p>
      </div>

      <div className="grid-two">
        <form className="card" onSubmit={handleSubmit}>
          <div className="toolbar">
            <span className="badge">Step 1: Learning context</span>
            <button
              type="button"
              className="btn btn--ghost"
              onClick={handleReset}
              disabled={status === "loading"}
            >
              Reset
            </button>
          </div>

          <div className="form-grid">
            {Object.entries(fieldMeta).map(([key, meta]) => (
              <div className="input-group" key={key}>
                <label htmlFor={key}>{meta.label}</label>
                {meta.type === "select" ? (
                  <select
                    className="input"
                    id={key}
                    name={key}
                    value={formData[key]}
                    onChange={handleChange}
                    required={!["recent_event", "topic_name"].includes(key)}
                  >
                    <option value="">Select {meta.label.toLowerCase()}</option>
                    {meta.options.map((option) => (
                      <option key={option} value={option}>
                        {option.charAt(0).toUpperCase() + option.slice(1)}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    className="input"
                    id={key}
                    name={key}
                    type={meta.type ?? (numericFields.includes(key) ? "number" : "text")}
                    placeholder={meta.placeholder}
                    value={formData[key]}
                    onChange={handleChange}
                    required={!["recent_event", "topic_name"].includes(key)}
                    step={numericFields.includes(key) ? "any" : undefined}
                    min={numericFields.includes(key) && (key.includes("level") || key === "confidence") ? 1 : undefined}
                    max={numericFields.includes(key) && (key.includes("level") || key === "confidence") ? 5 : undefined}
                  />
                )}
              </div>
            ))}
          </div>

          <div className="toolbar" style={{ justifyContent: "flex-end" }}>
            <button className="btn" type="submit" disabled={status === "loading"}>
              {status === "loading" ? (
                <>
                  <span className="loading"></span>
                  Calculating...
                </>
              ) : (
                "🚀 Predict Retention"
              )}
            </button>
          </div>
          {error && <p className="status-text status-text--error">{error}</p>}
        </form>

        <aside className="card highlight-card">
          <span className="badge">✨ Prediction Result</span>
          <div className="highlight-value">
            {prediction !== null ? (
              <>
                <div style={{ fontSize: "2.5rem", fontWeight: "800", display: "block", lineHeight: "1" }}>
                  {Math.round(prediction * 10) / 10}
                </div>
                <div style={{ fontSize: "1rem", color: "var(--text-secondary)", marginTop: "4px", fontWeight: "500" }}>
                  days until review
                </div>
              </>
            ) : (
              <div style={{ fontSize: "1.5rem", color: "var(--muted)", opacity: 0.5 }}>
                --
              </div>
            )}
          </div>
          <p className="status-text" style={{ fontSize: "1rem", lineHeight: "1.6" }}>{predictionCopy}</p>
          {prediction !== null && (
            <div className="status-text status-text--success" style={{ marginTop: "8px" }}>
              💡 <strong>Tip:</strong> Add this review to your spaced-repetition queue.
            </div>
          )}
        </aside>
      </div>
    </main>
  );
}
