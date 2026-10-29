from flask import Flask, request, jsonify
from flask_cors import CORS

from database.movies import get_all_movies
from engine.recommender import get_recommendations

from config.options import (
    GENRES,
    MOODS,
    LANGUAGES,
    RATINGS
)

app = Flask(__name__)
CORS(app)


def validate_user_preferences(user):
    errors = []

    required_fields = [
        "genre",
        "mood",
        "language",
        "max_duration",
        "rating"
    ]

    for field in required_fields:
        if field not in user:
            errors.append(f"Missing field: {field}")

    if errors:
        return errors

    if user["genre"] not in GENRES:
        errors.append(f"Invalid genre: {user['genre']}")

    if user["mood"] not in MOODS:
        errors.append(f"Invalid mood: {user['mood']}")

    if user["language"] not in LANGUAGES:
        errors.append(f"Invalid language: {user['language']}")

    if user["rating"] not in RATINGS:
        errors.append(f"Invalid rating: {user['rating']}")

    try:
        user["max_duration"] = int(user["max_duration"])

        if user["max_duration"] <= 0:
            errors.append("max_duration must be greater than 0.")

    except (ValueError, TypeError):
        errors.append("max_duration must be a number.")

    return errors


@app.route("/api/movies", methods=["GET"])
def movies():
    """Return all movies for the Discover page."""
    try:
        all_movies = get_all_movies()
        return jsonify({"movies": all_movies}), 200

    except Exception:
        app.logger.exception("Failed to fetch movies")
        return jsonify({"error": "Failed to fetch movies."}), 500


@app.route("/api/movies/<int:movie_id>", methods=["GET"])
def movie_details(movie_id):
    """Return one movie for the details page."""
    try:
        all_movies = get_all_movies()

        movie = next(
            (
                item for item in all_movies
                if int(item.get("id", -1)) == movie_id
            ),
            None
        )

        if movie is None:
            return jsonify({"error": "Movie not found."}), 404

        return jsonify({"movie": movie}), 200

    except (TypeError, ValueError):
        return jsonify({"error": "Invalid movie data."}), 500

    except Exception:
        app.logger.exception("Failed to fetch movie details")
        return jsonify({"error": "Failed to fetch movie details."}), 500


@app.route("/api/recommend", methods=["POST"])
def recommend():
    user = request.get_json(silent=True)

    if not isinstance(user, dict):
        return jsonify({
            "error": "A valid JSON request body is required."
        }), 400

    errors = validate_user_preferences(user)

    if errors:
        return jsonify({
            "error": "Invalid user preferences.",
            "details": errors
        }), 400

    try:
        # Retrieve movies from Supabase through the existing helper.
        movies = get_all_movies()

        # Preserve the existing recommendation engine.
        recommendations = get_recommendations(movies, user)

        return jsonify({
            "recommendations": recommendations
        }), 200

    except Exception:
        app.logger.exception("Recommendation request failed")
        return jsonify({
            "error": "Failed to generate recommendations."
        }), 500


if __name__ == "__main__":
    app.run(debug=False)