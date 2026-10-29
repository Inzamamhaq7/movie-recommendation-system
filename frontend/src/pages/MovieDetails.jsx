
import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import "./MovieDetails.css";

const API_URL = import.meta.env.VITE_API_URL;

function MovieDetails() {
  const { id } = useParams();
  const location = useLocation();

  const [movie, setMovie] = useState(location.state?.movie || null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadMovie() {
      setLoading(true);
      setError("");

      try {
        const response = await fetch(`${API_URL}/api/movies/${id}`);
        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.error || "Could not load movie details."
          );
        }

        if (!cancelled) {
          // Keep recommendation data from navigation state
          // while updating movie details from the API.
          setMovie((previousMovie) => ({
            ...previousMovie,
            ...data.movie,
            score: previousMovie?.score ?? data.movie.score,
            match_level:
              previousMovie?.match_level ?? data.movie.match_level,
            summary: previousMovie?.summary ?? data.movie.summary,
          }));
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadMovie();

    return () => {
      cancelled = true;
    };
  }, [id]);

  if (loading && !movie) {
    return (
      <main className="details-page">
        <p>Loading movie details...</p>
      </main>
    );
  }

  if (error && !movie) {
    return (
      <main className="details-page">
        <p>{error}</p>
        <Link to="/recommend">← Back to recommendations</Link>
      </main>
    );
  }

  if (!movie) return null;

  const summary = movie.summary;

  const fullDescription =
    movie.long_description ||
    movie.description ||
    "No description is available for this movie yet.";

  const hasRecommendationData =
    movie.score != null ||
    summary?.matches?.length > 0 ||
    summary?.rules?.length > 0 ||
    summary?.penalties?.length > 0;

  return (
    <main className="details-page">
      <Link className="details-back-link" to="/recommend">
        ← Back to recommendations
      </Link>

      <section className="details-hero">
        <div className="details-poster-wrap">
          {movie.poster_url ? (
            <img
              className="details-poster"
              src={movie.poster_url}
              alt={`${movie.title} poster`}
            />
          ) : (
            <div className="details-poster-placeholder">🎬</div>
          )}
        </div>

        <div className="details-main-info">
          <span className="details-eyebrow">MOVIE DETAILS</span>

          <h1>{movie.title}</h1>

          {movie.rating != null && (
            <p className="details-rating">
              ★ {movie.rating} <span>rating</span>
            </p>
          )}

          <div className="details-tags">
            {movie.genre && <span>{movie.genre}</span>}
            {movie.language && <span>{movie.language}</span>}
            {movie.duration && <span>{movie.duration} min</span>}
            {movie.mood && <span>{movie.mood} mood</span>}
          </div>

          {/* Full description stays in its original position */}
          <h2>About this movie</h2>

          <p className="details-description">
            {fullDescription}
          </p>

          {movie.score != null && (
            <div className="details-match">
              <span className="details-match-score">
                {Number(movie.score).toFixed(1)}%
              </span>

              <div>
                <strong>
                  {movie.match_level || "Your match score"}
                </strong>

                <p>
                  Compatibility with your selected preferences
                </p>
              </div>
            </div>
          )}

          <Link
            className="details-recommend-button"
            to="/recommend"
          >
            Find another movie →
          </Link>
        </div>
      </section>

      {hasRecommendationData && (
        <section className="details-explanation">
          <span className="details-eyebrow">
            RECOMMENDATION EXPLAINED
          </span>

          <h2>Why this movie?</h2>

          <p className="details-explanation-intro">
            Here's how this movie relates to your preferences.
          </p>

          {summary?.matches?.length > 0 && (
            <div className="details-reason-group">
              <h3>✓ Preference matches</h3>

              <ul>
                {summary.matches.map((item, index) => (
                  <li key={`${item.reason}-${index}`}>
                    {typeof item === "string"
                      ? item
                      : item.reason}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {summary?.rules?.length > 0 && (
            <div className="details-reason-group">
              <h3>✦ Recommendation insights</h3>

              <ul>
                {summary.rules.map((item, index) => (
                  <li key={`${item.reason}-${index}`}>
                    {typeof item === "string"
                      ? item
                      : item.reason}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {summary?.penalties?.length > 0 && (
            <div className="details-reason-group">
              <h3>Factors affecting the score</h3>

              <ul>
                {summary.penalties.map((item, index) => (
                  <li key={`${item.reason}-${index}`}>
                    {typeof item === "string"
                      ? item
                      : item.reason}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      )}
    </main>
  );
}

export default MovieDetails;
