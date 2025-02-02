from pymongo import MongoClient
# reusable functions for mongodb operations
def get_mongo_client():
    """Establishes a MongoDB client connection."""
    MONGO_URI = "mongodb+srv://followalong:Password123@cluster0.jcdn2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    return MongoClient(MONGO_URI)

def get_movies_collection(client):
    """Returns the movies collection from MongoDB."""
    db = client["movie_recommendation"]
    return db["movies"]

def get_users_collection(client):
    """Returns the users collection from MongoDB."""
    db = client["movie_recommendation"]
    return db["users"]

def fetch_all_users(users_collection):
    """Fetches all movies from the database."""
    return list(users_collection)
    
def fetch_all_movies(movies_collection):
    """Fetches all movies from the database."""
    return list(movies_collection.find({}, {"_id": 1, "title": 1, "genre": 1}))

def fetch_movie_genres(movies_collection, movie_ids):
    """Fetches genres for the given list of movie IDs."""
    genres = movies_collection.find({"_id": {"$in": movie_ids}}, {"_id": 0, "genre": 1})
    return list(set(movie["genre"] for movie in genres))

def fetch_movie_titles_by_ids(movies_collection, movie_ids):
    """Fetches movie titles for the given list of movie IDs."""
    movies = movies_collection.find({"_id": {"$in": movie_ids}}, {"_id": 0, "title": 1})
    return [movie["title"] for movie in movies]
