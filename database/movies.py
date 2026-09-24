from database.connection import supabase


def get_all_movies():
    response = (
        supabase
        .table("movies")
        .select("*")
        .execute()
    )

    return response.data