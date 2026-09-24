import unittest

from engine.recommender import calculate_score


class TestRecommendationEngine(unittest.TestCase):

    def test_perfect_match(self):

        movie = {
            "title": "Test Movie",
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

        self.assertGreaterEqual(
            score,
            90
        )

    def test_poor_match(self):

        movie = {
            "title": "Comedy Movie",
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

    def test_action_suspenseful_rule(self):

        movie = {
            "title": "Action Movie",
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

    def test_wrong_combination_rule(self):

        movie = {
            "title": "Comedy Movie",
            "genre": "Comedy",
            "mood": "Funny",
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

        self.assertNotIn(
            "Action + Suspenseful preference",
            reasons
        )

    def test_duration_partial_match(self):

        movie = {
            "title": "Long Movie",
            "genre": "Action",
            "mood": "Suspenseful",
            "language": "English",
            "duration": 130,
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

        duration_result = next(
            result
            for result in results
            if "Duration" in result["reason"]
        )

        self.assertEqual(
            duration_result["score"],
            7.5
        )


if __name__ == "__main__":
    unittest.main()