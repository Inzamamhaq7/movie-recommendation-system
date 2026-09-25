from config.weights import (
    WEIGHTS,
    MATCH_LEVELS
)

from engine.scoring import (
    calculate_genre_score,
    calculate_mood_score,
    calculate_language_score,
    calculate_duration_score,
    calculate_rating_score
)

from engine.rules import (
    apply_rules,
    get_max_combination_bonus
)


def calculate_score(movie, user):

    # -------------------------------------------------
    # 1. Calculate individual preference scores
    # -------------------------------------------------

    results = [
        calculate_genre_score(movie, user),
        calculate_mood_score(movie, user),
        calculate_language_score(movie, user),
        calculate_duration_score(movie, user),
        calculate_rating_score(movie, user)
    ]

    # -------------------------------------------------
    # 2. Apply recommendation rules
    # -------------------------------------------------

    rule_results = apply_rules(
        movie,
        user
    )

    results.extend(rule_results)

    # -------------------------------------------------
    # 3. Calculate raw score
    # -------------------------------------------------

    raw_score = sum(
        result["score"]
        for result in results
    )

    # -------------------------------------------------
    # 4. Calculate theoretical maximum
    # -------------------------------------------------

    base_max_score = sum(
        WEIGHTS.values()
    )

    max_combination_bonus = (
        get_max_combination_bonus()
    )

    max_score = (
        base_max_score
        + max_combination_bonus
    )

    # -------------------------------------------------
    # 5. Convert to percentage
    # -------------------------------------------------

    percentage = (
        raw_score / max_score
    ) * 100

    # Keep the public score safely between 0 and 100.
    percentage = max(
        0,
        min(percentage, 100)
    )

    return percentage, results


def get_match_level(score):

    if score >= MATCH_LEVELS["excellent"]:
        return "Excellent Match"

    if score >= MATCH_LEVELS["good"]:
        return "Good Match"

    if score >= MATCH_LEVELS["moderate"]:
        return "Moderate Match"

    if score >= MATCH_LEVELS["weak"]:
        return "Weak Match"

    return "Not Recommended"


def get_score_summary(results):

    matches = []
    penalties = []
    rules = []

    factor_prefixes = (
        "Genre ",
        "Mood ",
        "Language ",
        "Duration ",
        "Rating "
    )

    for result in results:

        score = result["score"]
        reason = result["reason"]

        # -------------------------------------------------
        # Normal preference factors
        # -------------------------------------------------

        if reason.startswith(factor_prefixes):

            if score > 0:

                matches.append({
                    "reason": reason,
                    "score": score
                })

            else:

                penalties.append({
                    "reason": reason,
                    "score": score
                })

        # -------------------------------------------------
        # Negative recommendation rules
        # -------------------------------------------------

        elif score < 0:

            penalties.append({
                "reason": reason,
                "score": score
            })

        # -------------------------------------------------
        # Positive recommendation rules
        # -------------------------------------------------

        elif score > 0:

            rules.append({
                "reason": reason,
                "score": score
            })

    return {
        "matches": matches,
        "rules": rules,
        "penalties": penalties
    }


def get_factor_scores(results):

    factor_scores = {
        "genre": 0,
        "mood": 0,
        "language": 0,
        "duration": 0,
        "rating": 0
    }

    for result in results:

        reason = result["reason"]
        score = result["score"]

        if reason.startswith("Genre "):

            factor_scores["genre"] = score

        elif reason.startswith("Mood "):

            factor_scores["mood"] = score

        elif reason.startswith("Language "):

            factor_scores["language"] = score

        elif reason.startswith("Duration "):

            factor_scores["duration"] = score

        elif reason.startswith("Rating "):

            factor_scores["rating"] = score

    return factor_scores


def get_recommendations(movies, user):

    recommendations = []

    for movie in movies:

        score, results = calculate_score(
            movie,
            user
        )

        # -------------------------------------------------
        # Minimum recommendation threshold
        # -------------------------------------------------

        if score >= MATCH_LEVELS["weak"]:

            match_level = get_match_level(
                score
            )

            summary = get_score_summary(
                results
            )

            factor_scores = get_factor_scores(
                results
            )

            recommendations.append({

                # -----------------------------------------
                # Movie information
                # -----------------------------------------

                "id": movie.get("id"),

                "title": movie.get(
                    "title",
                    "Untitled Movie"
                ),

                "genre": movie.get(
                    "genre",
                    "Unknown"
                ),

                "mood": movie.get(
                    "mood",
                    "Unknown"
                ),

                "language": movie.get(
                    "language",
                    "Unknown"
                ),

                "duration": movie.get(
                    "duration",
                    0
                ),

                "rating": movie.get(
                    "rating",
                    "Not Rated"
                ),

                "description": movie.get(
                    "description",
                    "Recommended based on your preferences."
                ),

                "poster_url": movie.get(
                    "poster_url"
                ),

                # -----------------------------------------
                # Recommendation information
                # -----------------------------------------

                "score": round(
                    score,
                    2
                ),

                "match_level": match_level,

                "factor_scores": factor_scores,

                "results": results,

                "summary": summary
            })

    # -------------------------------------------------
    # Highest score first
    # -------------------------------------------------

    recommendations.sort(
        key=lambda movie: movie["score"],
        reverse=True
    )

    return recommendations