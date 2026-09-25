from config.weights import WEIGHTS


def create_result(score, reason):
    """
    Create a standard scoring result.
    """

    return {
        "score": score,
        "reason": reason
    }


def calculate_genre_score(movie, user):
    """
    Genre is an exact preference.

    Matching genre:
        Full score

    Different genre:
        No genre points
    """

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
    """
    Mood is an exact preference.

    Matching mood:
        Full score

    Different mood:
        No mood points
    """

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
    """
    Language is an exact preference.

    Matching language:
        Full score

    Different language:
        No language points
    """

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
    """
    Rating is treated as a maximum acceptable rating.

    The user selects the highest rating they are comfortable
    with.

    Rating order:

        G < PG < PG-13 < R

    If the movie is within the user's maximum rating,
    it receives the full rating score.

    If the movie exceeds the user's maximum rating,
    it receives zero rating points.
    """

    rating_order = {
        "G": 0,
        "PG": 1,
        "PG-13": 2,
        "R": 3
    }

    movie_rating = movie["rating"]
    user_rating = user["rating"]

    movie_level = rating_order.get(movie_rating)
    user_level = rating_order.get(user_rating)

    # Defensive handling for unexpected values.
    if movie_level is None:
        return create_result(
            0,
            f"Unknown movie rating: {movie_rating}"
        )

    if user_level is None:
        return create_result(
            0,
            f"Unknown user rating preference: {user_rating}"
        )

    if movie_level <= user_level:

        return create_result(
            WEIGHTS["rating"],
            f"Rating accepted: {movie_rating} is within your maximum of {user_rating}"
        )

    return create_result(
        0,
        f"Rating exceeds your maximum: {movie_rating} > {user_rating}"
    )


def calculate_duration_score(movie, user):
    """
    Calculate duration using gradual scoring.

    Duration within preference:
        100%

    1-10 minutes over:
        75%

    11-20 minutes over:
        50%

    21-30 minutes over:
        25%

    More than 30 minutes over:
        0%
    """

    movie_duration = movie["duration"]
    max_duration = user["max_duration"]

    duration_weight = WEIGHTS["duration"]

    if movie_duration <= max_duration:

        return create_result(
            duration_weight,
            f"Duration matched: {movie_duration} min"
        )

    difference = movie_duration - max_duration

    if difference <= 10:

        score = duration_weight * 0.75

        return create_result(
            score,
            f"Duration slightly exceeds preference: "
            f"{movie_duration} min (+{difference} min)"
        )

    if difference <= 20:

        score = duration_weight * 0.50

        return create_result(
            score,
            f"Duration moderately exceeds preference: "
            f"{movie_duration} min (+{difference} min)"
        )

    if difference <= 30:

        score = duration_weight * 0.25

        return create_result(
            score,
            f"Duration significantly exceeds preference: "
            f"{movie_duration} min (+{difference} min)"
        )

    return create_result(
        0,
        f"Duration too long: "
        f"{movie_duration} min (+{difference} min)"
    )