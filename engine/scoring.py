from config.weights import WEIGHTS


def create_result(score, reason):
    return {
        "score": score,
        "reason": reason
    }


def calculate_genre_score(movie, user):

    if movie["genre"] == user["genre"]:
        return create_result(
            WEIGHTS["genre"],
            f"Genre matched: {movie['genre']}"
        )

    return create_result(
        0,
        f"Genre did not match: {movie['genre']}"
    )


def calculate_mood_score(movie, user):

    if movie["mood"] == user["mood"]:
        return create_result(
            WEIGHTS["mood"],
            f"Mood matched: {movie['mood']}"
        )

    return create_result(
        0,
        f"Mood did not match: {movie['mood']}"
    )


def calculate_language_score(movie, user):

    if movie["language"] == user["language"]:
        return create_result(
            WEIGHTS["language"],
            f"Language matched: {movie['language']}"
        )

    return create_result(
        0,
        f"Language did not match: {movie['language']}"
    )


def calculate_rating_score(movie, user):

    if movie["rating"] == user["rating"]:
        return create_result(
            WEIGHTS["rating"],
            f"Age rating matched: {movie['rating']}"
        )

    return create_result(
        0,
        f"Age rating did not match: {movie['rating']}"
    )


def calculate_duration_score(movie, user):

    movie_duration = movie["duration"]
    max_duration = user["max_duration"]

    # Perfect duration match
    if movie_duration <= max_duration:

        return create_result(
            WEIGHTS["duration"],
            f"Duration matched: {movie_duration} min"
        )

    # Movie is slightly longer
    difference = movie_duration - max_duration

    if difference <= 15:

        partial_score = WEIGHTS["duration"] * 0.5

        return create_result(
            partial_score,
            f"Duration slightly exceeds preference: "
            f"{movie_duration} min"
        )

    # Movie is much longer
    return create_result(
        0,
        f"Duration too long: {movie_duration} min"
    )