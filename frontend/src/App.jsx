
import { useState } from "react";
import { Link, NavLink, Navigate, Route, Routes } from "react-router-dom";

import PreferenceForm from "./components/PreferenceForm";
import RecommendationList from "./components/RecommendationList";
import Home from "./pages/Home";
import MovieDetails from "./pages/MovieDetails";

import "./App.css";

function RecommendPage() {
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_URL = import.meta.env.VITE_API_URL;

  async function getRecommendations(preferences) {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/api/recommend`, {
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
    } catch (err) {
      setError(err.message);
      setRecommendations(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header className="app-header">
        <h1>
          <span className="title-icon"><img
            src="/images/movie-recommendation-logo.svg"
            alt=""
            className="site-brand-logo-recommend"
          /></span>
          <span className="title-text">
            Movie Recommendation System
          </span>
        </h1>

        <p>
          Tell us your preferences and discover movies that match your taste.
        </p>
      </header>

      <PreferenceForm onRecommend={getRecommendations} />

      {loading && (
        <p className="loading">
          Finding the best movies for you...
        </p>
      )}

      {error && (
        <p className="error">
          Error: {error}
        </p>
      )}

      {!loading && !error && (
        <RecommendationList recommendations={recommendations} />
      )}
    </main>
  );
}

function App() {
  return (
    <>
      <header className="site-nav">
          <img
            src="/images/movie-recommendation-logo.svg"
            alt=""
            className="site-brand-logo"
          />

          <span className="site-brand-text">
            Movie <span>Recommendation</span> System
          </span>

        <nav
          className="site-nav-links"
          aria-label="Main navigation"
        >
          <NavLink to="/" end>
            Home
          </NavLink>

          <a href="/#discover">
            Discover
          </a>

          <NavLink to="/recommend">
            Recommend
          </NavLink>
        </nav>
      </header>

      <Routes>
        <Route path="/" element={<Home />} />

        <Route
          path="/recommend"
          element={<RecommendPage />}
        />

        <Route
          path="/movies/:id"
          element={<MovieDetails />}
        />

        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />
      </Routes>
    </>
  );
}

export default App;
