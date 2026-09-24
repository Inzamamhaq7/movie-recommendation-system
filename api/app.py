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
            errors.append(
                f"Missing field: {field}"
            )

    if errors:
        return errors

    if user["genre"] not in GENRES:
        errors.append(
            f"Invalid genre: {user['genre']}"
        )

    if user["mood"] not in MOODS:
        errors.append(
            f"Invalid mood: {user['mood']}"
        )

    if user["language"] not in LANGUAGES:
        errors.append(
            f"Invalid language: {user['language']}"
        )

    if user["rating"] not in RATINGS:
        errors.append(
            f"Invalid rating: {user['rating']}"
        )

    try:
        user["max_duration"] = int(
            user["max_duration"]
        )

        if user["max_duration"] <= 0:
            errors.append(
                "max_duration must be greater than 0."
            )

    except (ValueError, TypeError):
        errors.append(
            "max_duration must be a number."
        )

    return errors


@app.route("/api/recommend", methods=["POST"])
def recommend():

    user = request.get_json()

    if not user:
        return jsonify({
            "error": "Request body is required."
        }), 400

    errors = validate_user_preferences(
        user
    )

    if errors:
        return jsonify({
            "error": "Invalid user preferences.",
            "details": errors
        }), 400

    # Get movies from Supabase
    movies = get_all_movies()

    # Generate recommendations
    recommendations = get_recommendations(
        movies,
        user
    )

    return jsonify({
        "recommendations": recommendations
    })


if __name__ == "__main__":
    app.run(
        debug=True
    )