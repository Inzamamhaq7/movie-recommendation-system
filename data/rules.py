combination_rules = [
    {
        "type": "COMBINATION",
        "conditions": {
            "genre": "Action",
            "mood": "Suspenseful"
        },
        "bonus": 10,
        "reason": "Action + Suspenseful preference"
    },
    {
        "type": "COMBINATION",
        "conditions": {
            "genre": "Sci-Fi",
            "mood": "Suspenseful"
        },
        "bonus": 8,
        "reason": "Sci-Fi + Suspenseful preference"
    },
    {
        "type": "COMBINATION",
        "conditions": {
            "genre": "Comedy",
            "mood": "Funny"
        },
        "bonus": 10,
        "reason": "Comedy + Funny preference"
    }
]


penalty_rules = [
    {
        "type": "PENALTY",
        "movie_conditions": {
            "genre": "Horror"
        },
        "user_conditions": {
            "genre_not": "Horror"
        },
        "penalty": 5,
        "reason": "Horror is outside the user's preferred genre"
    }
]