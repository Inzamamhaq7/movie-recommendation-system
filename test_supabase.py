from database.connection import supabase


response = (
    supabase
    .table("movies")
    .select("*")
    .execute()
)


print(response.data)