import styles from "./RecommendationCard.module.css";

function RecommendationCard({ movie, index }) {
  // =========================================
  // BASIC MOVIE DATA
  // =========================================

  const title = movie?.title || "Untitled Movie";

  const score = Number(movie?.score ?? 0);

  const matchLevel =
    movie?.match_level || "Recommended";

  const genre =
    movie?.genre || "Genre not available";

  const mood =
    movie?.mood || "Mood not available";

  const language =
    movie?.language || "Language not available";

  const duration =
    movie?.duration != null
      ? `${movie.duration} min`
      : "Duration unavailable";

  const rating =
    movie?.rating || "Not Rated";

  const description =
    movie?.description ||
    "Recommended based on your selected preferences.";

  // =========================================
  // SUMMARY DATA
  // =========================================

  const summary = movie?.summary || {};

  const matches = Array.isArray(summary.matches)
    ? summary.matches
    : [];

  const rules = Array.isArray(summary.rules)
    ? summary.rules
    : [];

  const penalties = Array.isArray(summary.penalties)
    ? summary.penalties
    : [];

  // =========================================
  // MATCHING FACTORS
  // =========================================

  const matchFactors = [
    {
      name: "Genre",
      value: genre,
      icon: "🎭",
      className: styles.genreIcon,
    },
    {
      name: "Mood",
      value: mood,
      icon: "😊",
      className: styles.moodIcon,
    },
    {
      name: "Language",
      value: language,
      icon: "🌐",
      className: styles.languageIcon,
    },
    {
      name: "Duration",
      value: duration,
      icon: "⏱️",
      className: styles.durationIcon,
    },
    {
      name: "Rating",
      value: rating,
      icon: "⭐",
      className: styles.ratingIcon,
    },
  ];

  // =========================================
  // SCORE
  // =========================================

  const safeScore = Math.max(
    0,
    Math.min(score, 100)
  );

  const scoreAngle =
    `${safeScore * 3.6}deg`;

  // =========================================
  // RENDER
  // =========================================

  return (
    <article
      className={styles.recommendationCard}
    >

      {/* =====================================
          MATCH SCORE
          ===================================== */}

      <div
        className={styles.scoreContainer}
        style={{
          "--score-angle": scoreAngle,
        }}
        title={`${safeScore.toFixed(1)}% match`}
      >
        <span className={styles.score}>
          {safeScore.toFixed(1)}%
        </span>

        <span className={styles.scoreLabel}>
          Match
        </span>
      </div>


      {/* =====================================
          MAIN MOVIE SECTION
          ===================================== */}

      <div className={styles.movieMain}>

        {/* ===================================
            POSTER
            =================================== */}

        <div className={styles.moviePoster}>

          {movie?.poster_url ? (
            <img
              src={movie.poster_url}
              alt={`${title} poster`}
              loading="lazy"
            />
          ) : (
            <div
              className={styles.posterFallback}
            >
              <span>🎬</span>

              <small>
                Poster unavailable
              </small>
            </div>
          )}

        </div>


        {/* ===================================
            MOVIE INFORMATION
            =================================== */}

        <div className={styles.movieInfo}>

          {/* Ranking */}

          <span className={styles.movieNumber}>
            #{index + 1}
          </span>


          {/* Title */}

          <h3>
            {title}
          </h3>


          {/* Match level */}

          <span className={styles.matchLevel}>
            {matchLevel}
          </span>


          {/* =================================
              MOVIE METADATA
              ================================= */}

          <div className={styles.movieMeta}>

            <span>
              🎭 {genre}
            </span>

            <span>
              😊 {mood}
            </span>

            <span>
              🌐 {language}
            </span>

            <span>
              ⏱️ {duration}
            </span>

            <span>
              ⭐ {rating}
            </span>

          </div>

        </div>


        {/* ===================================
            FULL WIDTH DESCRIPTION
            =================================== */}

        <p
          className={styles.movieDescription}
        >
          {description}
        </p>

      </div>


      {/* =====================================
          WHY THIS MOVIE
          ===================================== */}

      <div className={styles.reasonSection}>

        {/* Header */}

        <div className={styles.reasonHeader}>

          <div>

            <h4>
              Why this movie?
            </h4>

            <p>
              Based on your selected preferences
            </p>

          </div>

        </div>


        {/* =================================
            MATCHING FACTORS
            ================================= */}

        <div className={styles.matchGrid}>

          {matchFactors.map((factor) => (
            <div
              className={styles.matchItem}
              key={factor.name}
            >

              <span
                className={`${styles.matchIcon} ${factor.className}`}
              >
                {factor.icon}
              </span>

              <span
                className={styles.matchName}
              >
                {factor.name}
              </span>

              <strong
                title={factor.value}
              >
                {factor.value}
              </strong>

            </div>
          ))}

        </div>


        {/* =================================
            PREFERENCE MATCHES
            ================================= */}

        {matches.length > 0 && (
          <div
            className={styles.compactReason}
          >

            <span
              className={styles.reasonIcon}
            >
              ✓
            </span>

            <div>

              <span
                className={styles.reasonLabel}
              >
                Preference matches
              </span>

              <span
                className={styles.reasonText}
              >
                {matches
                  .map(
                    (item) => item.reason
                  )
                  .join(" • ")}
              </span>

            </div>

          </div>
        )}


        {/* =================================
            RECOMMENDATION INSIGHT
            ================================= */}

        {rules.length > 0 && (
          <div
            className={styles.compactReason}
          >

            <span
              className={styles.reasonIcon}
            >
              💡
            </span>

            <div>

              <span
                className={styles.reasonLabel}
              >
                Recommendation insight
              </span>

              <span
                className={styles.reasonText}
              >
                {rules
                  .map(
                    (item) => item.reason
                  )
                  .join(" ")}
              </span>

            </div>

          </div>
        )}


        {/* =================================
            PENALTIES
            ================================= */}

        {penalties.length > 0 && (
          <div
            className={styles.penalties}
          >

            <span
              className={styles.penaltyIcon}
            >
              ⚠️
            </span>

            <div>

              <span
                className={styles.reasonLabel}
              >
                Factors affecting the score
              </span>

              <span
                className={styles.reasonText}
              >
                {penalties
                  .map(
                    (item) => item.reason
                  )
                  .join(" ")}
              </span>

            </div>

          </div>
        )}

      </div>


      {/* =====================================
          VIEW DETAILS
          ===================================== */}

      <button
        type="button"
        className={styles.movieDetailsButton}
      >

        <span>
          View Details
        </span>

        <span
          className={styles.buttonArrow}
        >
          →
        </span>

      </button>

    </article>
  );
}

export default RecommendationCard;