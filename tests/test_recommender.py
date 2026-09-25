import unittest

from engine.recommender import (
    calculate_score,
    get_match_level,
    get_score_summary,
    get_factor_scores,
    get_recommendations
)

from engine.scoring import (
    calculate_duration_score,
    calculate_rating_score
)


class TestRecommendationScoring(unittest.TestCase):

    # =========================================================
    # PERFECT MATCH
    # =========================================================

    def test_perfect_match(self):

        movie = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "duration": 100,
            "rating": "R"
        }

        user = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "max_duration": 120,
            "rating": "R"
        }

        score, results = calculate_score(
            movie,
            user
        )

        self.assertEqual(
            score,
            100
        )


    # =========================================================
    # POOR MATCH
    # =========================================================

    def test_poor_match(self):

        movie = {
            "genre": "Comedy",
            "mood": "Funny",
            "language": "English",
            "duration": 100,
            "rating": "PG"
        }

        user = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "max_duration": 120,
            "rating": "R"
        }

        score, results = calculate_score(
            movie,
            user
        )

        self.assertLess(
            score,
            60
        )


    # =========================================================
    # COMBINATION RULES
    # =========================================================

    def test_action_suspenseful_rule(self):

        movie = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "duration": 100,
            "rating": "R"
        }

        user = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "max_duration": 120,
            "rating": "R"
        }

        score, results = calculate_score(
            movie,
            user
        )

        reasons = [
            result["reason"]
            for result in results
        ]

        self.assertIn(
            "Action + Suspenseful preference",
            reasons
        )


    def test_sci_fi_suspenseful_rule(self):

        movie = {
            "genre": "Sci-Fi",
            "mood": "Suspenseful",
            "language": "English",
            "duration": 120,
            "rating": "PG-13"
        }

        user = {
            "genre": "Sci-Fi",
            "mood": "Suspenseful",
            "language": "English",
            "max_duration": 120,
            "rating": "PG-13"
        }

        score, results = calculate_score(
            movie,
            user
        )

        reasons = [
            result["reason"]
            for result in results
        ]

        self.assertIn(
            "Sci-Fi + Suspenseful preference",
            reasons
        )


    def test_comedy_funny_rule(self):

        movie = {
            "genre": "Comedy",
            "mood": "Funny",
            "language": "English",
            "duration": 100,
            "rating": "PG"
        }

        user = {
            "genre": "Comedy",
            "mood": "Funny",
            "language": "English",
            "max_duration": 120,
            "rating": "PG"
        }

        score, results = calculate_score(
            movie,
            user
        )

        reasons = [
            result["reason"]
            for result in results
        ]

        self.assertIn(
            "Comedy + Funny preference",
            reasons
        )


    def test_romance_emotional_rule(self):

        movie = {
            "genre": "Romance",
            "mood": "Emotional",
            "language": "English",
            "duration": 110,
            "rating": "PG-13"
        }

        user = {
            "genre": "Romance",
            "mood": "Emotional",
            "language": "English",
            "max_duration": 120,
            "rating": "PG-13"
        }

        score, results = calculate_score(
            movie,
            user
        )

        reasons = [
            result["reason"]
            for result in results
        ]

        self.assertIn(
            "Romance + Emotional preference",
            reasons
        )


    def test_drama_emotional_rule(self):

        movie = {
            "genre": "Drama",
            "mood": "Emotional",
            "language": "English",
            "duration": 120,
            "rating": "PG-13"
        }

        user = {
            "genre": "Drama",
            "mood": "Emotional",
            "language": "English",
            "max_duration": 120,
            "rating": "PG-13"
        }

        score, results = calculate_score(
            movie,
            user
        )

        reasons = [
            result["reason"]
            for result in results
        ]

        self.assertIn(
            "Drama + Emotional preference",
            reasons
        )


    def test_wrong_combination_rule(self):

        movie = {
            "genre": "Comedy",
            "mood": "Funny",
            "language": "English",
            "duration": 100,
            "rating": "PG"
        }

        user = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "max_duration": 120,
            "rating": "R"
        }

        score, results = calculate_score(
            movie,
            user
        )

        reasons = [
            result["reason"]
            for result in results
        ]

        self.assertNotIn(
            "Action + Suspenseful preference",
            reasons
        )


    # =========================================================
    # DURATION
    # =========================================================

    def test_duration_within_limit(self):

        result = calculate_duration_score(
            {
                "duration": 120
            },
            {
                "max_duration": 120
            }
        )

        self.assertEqual(
            result["score"],
            15
        )


    def test_duration_10_minutes_over(self):

        result = calculate_duration_score(
            {
                "duration": 130
            },
            {
                "max_duration": 120
            }
        )

        self.assertEqual(
            result["score"],
            11.25
        )


    def test_duration_20_minutes_over(self):

        result = calculate_duration_score(
            {
                "duration": 140
            },
            {
                "max_duration": 120
            }
        )

        self.assertEqual(
            result["score"],
            7.5
        )


    def test_duration_30_minutes_over(self):

        result = calculate_duration_score(
            {
                "duration": 150
            },
            {
                "max_duration": 120
            }
        )

        self.assertEqual(
            result["score"],
            3.75
        )


    def test_duration_more_than_30_minutes_over(self):

        result = calculate_duration_score(
            {
                "duration": 151
            },
            {
                "max_duration": 120
            }
        )

        self.assertEqual(
            result["score"],
            0
        )


    # =========================================================
    # RATING
    # =========================================================

    def test_rating_exact_match(self):

        result = calculate_rating_score(
            {
                "rating": "PG-13"
            },
            {
                "rating": "PG-13"
            }
        )

        self.assertEqual(
            result["score"],
            15
        )


    def test_rating_lower_than_maximum_is_accepted(self):

        result = calculate_rating_score(
            {
                "rating": "PG"
            },
            {
                "rating": "PG-13"
            }
        )

        self.assertEqual(
            result["score"],
            15
        )


    def test_rating_g_with_pg13_preference(self):

        result = calculate_rating_score(
            {
                "rating": "G"
            },
            {
                "rating": "PG-13"
            }
        )

        self.assertEqual(
            result["score"],
            15
        )


    def test_rating_above_maximum_is_rejected(self):

        result = calculate_rating_score(
            {
                "rating": "R"
            },
            {
                "rating": "PG-13"
            }
        )

        self.assertEqual(
            result["score"],
            0
        )


    def test_rating_pg13_with_g_preference_is_rejected(self):

        result = calculate_rating_score(
            {
                "rating": "PG-13"
            },
            {
                "rating": "G"
            }
        )

        self.assertEqual(
            result["score"],
            0
        )


    # =========================================================
    # PENALTIES
    # =========================================================

    def test_horror_penalty(self):

        movie = {
            "genre": "Horror",
            "mood": "Suspenseful",
            "language": "English",
            "duration": 100,
            "rating": "R"
        }

        user = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "max_duration": 120,
            "rating": "R"
        }

        score, results = calculate_score(
            movie,
            user
        )

        penalties = [
            result
            for result in results
            if result["score"] < 0
        ]

        self.assertTrue(
            any(
                "Horror is outside the user's preferred genre"
                in result["reason"]
                for result in penalties
            )
        )


    # =========================================================
    # FACTOR SCORES
    # =========================================================

    def test_factor_scores_are_correct(self):

        movie = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "duration": 130,
            "rating": "PG-13"
        }

        user = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "max_duration": 120,
            "rating": "PG-13"
        }

        score, results = calculate_score(
            movie,
            user
        )

        factors = get_factor_scores(
            results
        )

        self.assertEqual(
            factors["genre"],
            30
        )

        self.assertEqual(
            factors["mood"],
            25
        )

        self.assertEqual(
            factors["language"],
            15
        )

        self.assertEqual(
            factors["duration"],
            11.25
        )

        self.assertEqual(
            factors["rating"],
            15
        )


    # =========================================================
    # SUMMARY
    # =========================================================

    def test_summary_separates_matches_and_penalties(self):

        movie = {
            "genre": "Horror",
            "mood": "Suspenseful",
            "language": "English",
            "duration": 100,
            "rating": "R"
        }

        user = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "max_duration": 120,
            "rating": "R"
        }

        score, results = calculate_score(
            movie,
            user
        )

        summary = get_score_summary(
            results
        )

        self.assertGreater(
            len(summary["matches"]),
            0
        )

        self.assertEqual(
            len(summary["rules"]),
            0
        )

        self.assertGreater(
            len(summary["penalties"]),
            0
        )

    def test_summary_contains_positive_rules(self):

        movie = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "duration": 100,
            "rating": "R"
        }

        user = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "max_duration": 120,
            "rating": "R"
        }

        score, results = calculate_score(
            movie,
            user
        )

        summary = get_score_summary(
            results
        )

        self.assertGreater(
            len(summary["rules"]),
            0
        )

        self.assertTrue(
            any(
                "Action + Suspenseful preference"
                in item["reason"]
                for item in summary["rules"]
            )
        )


    # =========================================================
    # MATCH LEVELS
    # =========================================================

    def test_match_levels(self):

        self.assertEqual(
            get_match_level(95),
            "Excellent Match"
        )

        self.assertEqual(
            get_match_level(80),
            "Good Match"
        )

        self.assertEqual(
            get_match_level(65),
            "Moderate Match"
        )

        self.assertEqual(
            get_match_level(45),
            "Weak Match"
        )

        self.assertEqual(
            get_match_level(30),
            "Not Recommended"
        )


    # =========================================================
    # SCORE RANGE
    # =========================================================

    def test_score_never_exceeds_100(self):

        movie = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "duration": 100,
            "rating": "R"
        }

        user = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "max_duration": 120,
            "rating": "R"
        }

        score, results = calculate_score(
            movie,
            user
        )

        self.assertLessEqual(
            score,
            100
        )


    def test_recommendations_are_sorted(self):

        movies = [
            {
                "id": 1,
                "title": "Weak Movie",
                "genre": "Comedy",
                "mood": "Funny",
                "language": "Hindi",
                "duration": 180,
                "rating": "R"
            },
            {
                "id": 2,
                "title": "Strong Movie",
                "genre": "Action",
                "mood": "Suspenseful",
                "language": "English",
                "duration": 100,
                "rating": "R"
            }
        ]

        user = {
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "max_duration": 120,
            "rating": "R"
        }

        recommendations = get_recommendations(
            movies,
            user
        )

        for i in range(
            len(recommendations) - 1
        ):
            self.assertGreaterEqual(
                recommendations[i]["score"],
                recommendations[i + 1]["score"]
            )


if __name__ == "__main__":
    unittest.main()