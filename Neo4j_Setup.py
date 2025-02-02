from neo4j import GraphDatabase

def get_neo4j_driver():
    """Establishes a Neo4j driver connection."""
    NEO4J_URI = "neo4j+s://fe67dae3.databases.neo4j.io"
    NEO4J_AUTH = ("neo4j", "f2clXhFExbRIiyLciwAzVcpt_1uGVAqHZ6Kw5u-lymc")
    return GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

def fetch_recommended_movies(neo4j_driver, genres, watched_movie_ids):
    """Fetches one movie per genre excluding watched movies."""
    recommended_movies = []
    with neo4j_driver.session() as session:
        for genre in genres:
            result = session.run(
                """
                MATCH (m:Movie)
                WHERE m.genre = $genre AND NOT m.id IN $watched_ids
                RETURN m.title AS title, m.genre AS genre
                LIMIT 1
                """,
                genre=genre,
                watched_ids=watched_movie_ids
            )
            record = result.single()
            if record:
                recommended_movies.append({"title": record["title"], "genre": record["genre"]})
    return recommended_movies
