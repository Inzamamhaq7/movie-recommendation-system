
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./Home.css";

const API_URL = import.meta.env.VITE_API_URL;

function Home() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMovies() {
      try {
        const response = await fetch(`${API_URL}/api/movies`);

        if (!response.ok) {
          throw new Error("Could not load movies.");
        }

        const data = await response.json();
        setMovies(data.movies || []);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    loadMovies();
  }, []);

  return (
    <main className="home-page">
      <section className="home-hero">
        <div className="home-hero-content">
          <span className="home-eyebrow">
            YOUR NEXT FAVORITE FILM AWAITS
          </span>

          <h1>
            Every mood
            <br />
            has a <span>movie.</span>
          </h1>

          <p>
            Discover films picked for your taste with
            explainable, personalized AI recommendations.
          </p>

          <div className="home-actions">
            <Link
              className="home-primary-button"
              to="/recommend"
            >
              Find my movie <span aria-hidden="true">→</span>
            </Link>

            <a
              className="home-secondary-button"
              href="#discover"
            >
              Explore collection
            </a>
          </div>
        </div>

        <div className="home-hero-visual" aria-hidden="true">
          <img
            src="/images/movie-night-scene.png"
            alt=""
            fetchPriority="high"
          />
        </div>
      </section>

      <section className="home-discover" id="discover">
        <div className="home-section-heading">
          <div>
            <span className="home-eyebrow">
              THE MOVIE COLLECTION
            </span>

            <h2>Discover something good</h2>
          </div>

          <span className="home-movie-count">
            {movies.length} movies
          </span>
        </div>

        {loading ? (
          <p className="home-status">Loading movies...</p>
        ) : movies.length === 0 ? (
          <p className="home-status">
            Movies couldn't be loaded. Check that your Flask API is running.
          </p>
        ) : (
          <div className="home-movie-grid">
            {movies.slice(0, 8).map((movie) => (
              <Link
                className="home-movie-card"
                to={`/movies/${movie.id}`}
                state={{ movie }}
                key={movie.id}
              >
                {movie.poster_url ? (
                  <img
                    src={movie.poster_url}
                    alt={`${movie.title} poster`}
                    loading="lazy"
                  />
                ) : (
                  <div className="home-poster-placeholder">
                    🎬
                  </div>
                )}

                <div className="home-movie-info">
                  <h3>{movie.title}</h3>

                  <p>
                    {movie.genre || "Movie"} ·{" "}
                    {movie.language || "Language unavailable"}
                  </p>

                  {movie.rating != null && (
                    <span>★ {movie.rating}</span>
                  )}
                </div>
              </Link>
            ))}
          </div>
        )}

        <div className="home-bottom-action">
          <Link to="/recommend">
            Get personalized recommendations →
          </Link>
        </div>
      </section>
    </main>
  );
}

export default Home;
