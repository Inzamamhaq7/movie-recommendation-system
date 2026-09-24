
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
    # 2. Apply AI rules
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
    # 4. Calculate maximum possible score
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
    # 5. Convert score to percentage
    # -------------------------------------------------

    percentage = (
        raw_score / max_score
    ) * 100

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

    normal_keywords = [
        "Genre matched",
        "Genre did not match",
        "Mood matched",
        "Mood did not match",
        "Language matched",
        "Language did not match",
        "Duration matched",
        "Duration slightly exceeds preference",
        "Duration too long",
        "Age rating matched",
        "Age rating did not match"
    ]

    for result in results:

        score = result["score"]
        reason = result["reason"]

        # Positive normal preference matches
        if score > 0 and reason in normal_keywords:

            matches.append({
                "reason": reason,
                "score": score
            })

        # Negative results / penalties
        elif score < 0:

            penalties.append({
                "reason": reason,
                "score": score
            })

        # Positive AI rules
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


def get_recommendations(movies, user):

    recommendations = []

    for movie in movies:

        score, results = calculate_score(
            movie,
            user
        )

        if score >= 40:

            match_level = get_match_level(
                score
            )

            summary = get_score_summary(
                results
            )

            recommendations.append({
                "title": movie["title"],
                "score": score,
                "match_level": match_level,
                "results": results,
                "summary": summary
            })

    # Highest score first
    recommendations.sort(
        key=lambda movie: movie["score"],
        reverse=True
    )

    return recommendations