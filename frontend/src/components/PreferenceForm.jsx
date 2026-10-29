
import { useState } from "react";

function PreferenceForm({ onRecommend }) {
  const [genre, setGenre] = useState("Action");
  const [mood, setMood] = useState("Suspenseful");
  const [language, setLanguage] = useState("English");
  const [maxDuration, setMaxDuration] = useState(120);
  const [rating, setRating] = useState("R");

  function handleSubmit(event) {
    event.preventDefault();

    onRecommend({
      genre,
      mood,
      language,
      max_duration: Number(maxDuration),
      rating,
    });
  }

  return (
    <form className="preference-form" onSubmit={handleSubmit}>
      <div className="preference-heading">
        <span className="preference-kicker">
          PERSONALIZE YOUR PICKS
        </span>

        <h2>Find your next movie</h2>
      </div>

      <div className="form-grid">
        <div className="form-group">
          <label htmlFor="genre">Genre</label>
          <select
            id="genre"
            value={genre}
            onChange={(event) => setGenre(event.target.value)}
          >
            <option value="Action">Action</option>
            <option value="Comedy">Comedy</option>
            <option value="Horror">Horror</option>
            <option value="Romance">Romance</option>
            <option value="Sci-Fi">Sci-Fi</option>
            <option value="Drama">Drama</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="mood">Mood</label>
          <select
            id="mood"
            value={mood}
            onChange={(event) => setMood(event.target.value)}
          >
            <option value="Exciting">Exciting</option>
            <option value="Suspenseful">Suspenseful</option>
            <option value="Funny">Funny</option>
            <option value="Relaxed">Relaxed</option>
            <option value="Emotional">Emotional</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="language">Language</label>
          <select
            id="language"
            value={language}
            onChange={(event) => setLanguage(event.target.value)}
          >
            <option value="English">English</option>
            <option value="Hindi">Hindi</option>
            <option value="Marathi">Marathi</option>
            <option value="Japanese">Japanese</option>
            <option value="Korean">Korean</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="duration">Maximum duration</label>
          <div className="duration-input-wrap">
            <input
              id="duration"
              type="number"
              min="1"
              max="600"
              value={maxDuration}
              onChange={(event) => setMaxDuration(event.target.value)}
              required
            />
            <span>min</span>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="rating">Age rating</label>
          <select
            id="rating"
            value={rating}
            onChange={(event) => setRating(event.target.value)}
          >
            <option value="G">G — General</option>
            <option value="PG">PG — Parental guidance</option>
            <option value="PG-13">PG-13 — Teens</option>
            <option value="R">R — Restricted</option>
          </select>
        </div>
      </div>

      <div className="preference-footer">
        <p>
          <span className="preference-status-dot" />
          Tailored to your taste
        </p>

        <button className="recommend-button" type="submit">
          Find My Movies <span aria-hidden="true">→</span>
        </button>
      </div>
    </form>
  );
}

export default PreferenceForm;
