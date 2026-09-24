import { useState } from "react";

import PreferenceForm from "./components/PreferenceForm";
import RecommendationList from "./components/RecommendationList";

import "./App.css";

function App() {
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function getRecommendations(preferences) {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/recommend", {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(preferences),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong.");
      }

      setRecommendations(data.recommendations);
    } catch (error) {
      setError(error.message);

      setRecommendations(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header className="app-header">
        <h1>
          <span className="title-icon">🎬</span>
          <span className="title-text">Movie Recommendation System</span>
        </h1>

        <p>
          Tell us your preferences and discover movies that match your taste.
        </p>
      </header>

      <PreferenceForm onRecommend={getRecommendations} />

      {loading && <p className="loading">Finding the best movies for you...</p>}

      {error && <p className="error">Error: {error}</p>}

      {!loading && !error && (
        <RecommendationList recommendations={recommendations} />
      )}
    </main>
  );
}

export default App;
