combination_rules = [

    # ---------------------------------------------------------
    # ACTION
    # ---------------------------------------------------------

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
            "genre": "Action",
            "mood": "Exciting"
        },
        "bonus": 8,
        "reason": "Action + Exciting preference"
    },

    # ---------------------------------------------------------
    # SCI-FI
    # ---------------------------------------------------------

    {
        "type": "COMBINATION",
        "conditions": {
            "genre": "Sci-Fi",
            "mood": "Suspenseful"
        },
        "bonus": 10,
        "reason": "Sci-Fi + Suspenseful preference"
    },

    {
        "type": "COMBINATION",
        "conditions": {
            "genre": "Sci-Fi",
            "mood": "Exciting"
        },
        "bonus": 8,
        "reason": "Sci-Fi + Exciting preference"
    },

    # ---------------------------------------------------------
    # COMEDY
    # ---------------------------------------------------------

    {
        "type": "COMBINATION",
        "conditions": {
            "genre": "Comedy",
            "mood": "Funny"
        },
        "bonus": 10,
        "reason": "Comedy + Funny preference"
    },

    {
        "type": "COMBINATION",
        "conditions": {
            "genre": "Comedy",
            "mood": "Relaxed"
        },
        "bonus": 8,
        "reason": "Comedy + Relaxed preference"
    },

    # ---------------------------------------------------------
    # HORROR
    # ---------------------------------------------------------

    {
        "type": "COMBINATION",
        "conditions": {
            "genre": "Horror",
            "mood": "Suspenseful"
        },
        "bonus": 10,
        "reason": "Horror + Suspenseful preference"
    },

    # ---------------------------------------------------------
    # ROMANCE
    # ---------------------------------------------------------

    {
        "type": "COMBINATION",
        "conditions": {
            "genre": "Romance",
            "mood": "Emotional"
        },
        "bonus": 10,
        "reason": "Romance + Emotional preference"
    },

    {
        "type": "COMBINATION",
        "conditions": {
            "genre": "Romance",
            "mood": "Relaxed"
        },
        "bonus": 8,
        "reason": "Romance + Relaxed preference"
    },

    # ---------------------------------------------------------
    # DRAMA
    # ---------------------------------------------------------

    {
        "type": "COMBINATION",
        "conditions": {
            "genre": "Drama",
            "mood": "Emotional"
        },
        "bonus": 10,
        "reason": "Drama + Emotional preference"
    },

    {
        "type": "COMBINATION",
        "conditions": {
            "genre": "Drama",
            "mood": "Suspenseful"
        },
        "bonus": 6,
        "reason": "Drama + Suspenseful preference"
    }
]


penalty_rules = [

    # ---------------------------------------------------------
    # HORROR GENRE PENALTY
    # ---------------------------------------------------------

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