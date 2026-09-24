from data.movies import movies
from engine.recommender import get_recommendations
from engine.validator import choose_option

from config.options import (
    GENRES,
    MOODS,
    LANGUAGES,
    RATINGS
)


def get_user_preferences():

    print("\n================================")
    print("   MOVIE RECOMMENDATION SYSTEM")
    print("================================")

    genre = choose_option(
        "Select Genre",
        GENRES
    )

    mood = choose_option(
        "Select Mood",
        MOODS
    )

    language = choose_option(
        "Select Language",
        LANGUAGES
    )

    while True:

        try:
            max_duration = int(
                input(
                    "\nMaximum duration (minutes): "
                )
            )

            if max_duration > 0:
                break

            print("Duration must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")

    rating = choose_option(
        "Select Age Rating",
        RATINGS
    )

    return {
        "genre": genre,
        "mood": mood,
        "language": language,
        "max_duration": max_duration,
        "rating": rating
    }




def display_recommendations(recommendations):

    print("\n================================")
    print("       RECOMMENDATIONS")
    print("================================")

    if not recommendations:

        print("\nNo suitable movies found.")
        return

    for index, movie in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"\n{index}. 🎬 {movie['title']}"
        )

        print(
            f"   Match Score: "
            f"{movie['score']:.2f}%"
        )

        print(
            f"   Match Level: "
            f"{movie['match_level']}"
        )

        summary = movie["summary"]

        # ---------------------------------------------
        # Matching preferences
        # ---------------------------------------------

        if summary["matches"]:

            print("\n   ✓ Matching Preferences:")

            for item in summary["matches"]:

                print(
                    f"      ✓ {item['reason']} "
                    f"(+{item['score']})"
                )

        # ---------------------------------------------
        # AI rules
        # ---------------------------------------------

        if summary["rules"]:

            print("\n   🧠 Rules Fired:")

            for item in summary["rules"]:

                print(
                    f"      → {item['reason']} "
                    f"(+{item['score']})"
                )

        # ---------------------------------------------
        # Penalties
        # ---------------------------------------------

        if summary["penalties"]:

            print("\n   ⚠ Penalties:")

            for item in summary["penalties"]:

                print(
                    f"      ⚠ {item['reason']} "
                    f"({item['score']})"
                )

        print()



def main():

    user = get_user_preferences()

    recommendations = get_recommendations(
        movies,
        user
    )

    display_recommendations(
        recommendations
    )


if __name__ == "__main__":
    main()