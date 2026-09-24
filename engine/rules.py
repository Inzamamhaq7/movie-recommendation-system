
from data.rules import (
    combination_rules,
    penalty_rules
)


def check_conditions(conditions, data):
    """
    Check whether all conditions match the given data.
    """

    for attribute, expected_value in conditions.items():

        if data.get(attribute) != expected_value:
            return False

    return True


def check_user_conditions(conditions, user):
    """
    Check user-specific conditions.

    Supports:
    - exact match
    - _not condition
    """

    for attribute, expected_value in conditions.items():

        if attribute.endswith("_not"):

            actual_attribute = attribute[:-4]

            if user.get(actual_attribute) == expected_value:
                return False

        else:

            if user.get(attribute) != expected_value:
                return False

    return True


def evaluate_combination_rule(rule, movie, user):
    """
    Evaluate a combination rule.
    """

    movie_matches = check_conditions(
        rule["conditions"],
        movie
    )

    user_matches = check_conditions(
        rule["conditions"],
        user
    )

    if movie_matches and user_matches:

        return {
            "score": rule["bonus"],
            "reason": rule["reason"]
        }

    return None


def evaluate_penalty_rule(rule, movie, user):
    """
    Evaluate a penalty rule.
    """

    movie_matches = check_conditions(
        rule["movie_conditions"],
        movie
    )

    user_matches = check_user_conditions(
        rule["user_conditions"],
        user
    )

    if movie_matches and user_matches:

        return {
            "score": -rule["penalty"],
            "reason": rule["reason"]
        }

    return None


def evaluate_rule(rule, movie, user):
    """
    Generic rule evaluator.

    Determines how to evaluate the rule
    based on its type.
    """

    rule_type = rule["type"]

    if rule_type == "COMBINATION":

        return evaluate_combination_rule(
            rule,
            movie,
            user
        )

    if rule_type == "PENALTY":

        return evaluate_penalty_rule(
            rule,
            movie,
            user
        )

    return None


def apply_rules(movie, user):
    """
    Apply all available rules to a movie.
    """

    rules = (
        combination_rules
        + penalty_rules
    )

    results = []

    for rule in rules:

        result = evaluate_rule(
            rule,
            movie,
            user
        )

        if result is not None:
            results.append(result)

    return results


def get_max_combination_bonus():
    """
    Find the largest possible combination bonus.
    """

    if not combination_rules:
        return 0

    return max(
        rule["bonus"]
        for rule in combination_rules
    )