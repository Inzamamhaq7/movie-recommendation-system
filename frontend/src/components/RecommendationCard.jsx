function RecommendationCard({ movie, index }) {
  const score = movie.score;

  return (
    <article className="recommendation-card">
      {/* Movie Header */}

      <div className="movie-header">
        <div className="movie-title">
          <h3>
            {index + 1}. {movie.title}
          </h3>

          <span className="match-level">{movie.match_level}</span>
        </div>

        <div
          className="score-container"
          style={{
            "--score-angle": `${Math.min(score, 100) * 3.6}deg`,
          }}
        >
          <span className="score">{score.toFixed(1)}%</span>

          <span className="score-label">Match</span>
        </div>
      </div>

      {/* Score Progress Bar */}

      <div className="score-bar">
        <div
          className="score-fill"
          style={{
            width: `${Math.min(score, 100)}%`,
          }}
        />
      </div>

      {/* Matching Preferences */}

      {movie.summary.matches.length > 0 && (
        <div className="reason-section">
          <h4>✓ Matching Preferences</h4>

          <ul>
            {movie.summary.matches.map((item, itemIndex) => (
              <li key={itemIndex}>
                <span>{item.reason}</span>

                <strong>+{item.score}</strong>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* AI Rules */}

      {movie.summary.rules.length > 0 && (
        <div className="reason-section rule-section">
          <h4>🧠 Rules Fired</h4>

          <ul>
            {movie.summary.rules.map((item, itemIndex) => (
              <li key={itemIndex}>
                <span>{item.reason}</span>

                <strong>+{item.score}</strong>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Penalties */}

      {movie.summary.penalties.length > 0 && (
        <div className="reason-section penalty-section">
          <h4>⚠ Penalties</h4>

          <ul>
            {movie.summary.penalties.map((item, itemIndex) => (
              <li key={itemIndex}>
                <span>{item.reason}</span>

                <strong>{item.score}</strong>
              </li>
            ))}
          </ul>
        </div>
      )}
    </article>
  );
}

export default RecommendationCard;
