import streamlit as st
from MongoDB_Setup import get_mongo_client, get_movies_collection, fetch_all_movies, fetch_movie_genres, fetch_movie_titles_by_ids, fetch_all_users, get_users_collection
from Neo4j_Setup import get_neo4j_driver, fetch_recommended_movies
from Redis_Setup import get_redis_client, fetch_watch_history

# Setup connections
mongo_client = get_mongo_client()
movies_collection = get_movies_collection(mongo_client)
users_collection = get_users_collection(mongo_client)
neo4j_driver = get_neo4j_driver()
redis_client = get_redis_client()

# Streamlit App
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎥", layout="wide")

st.markdown("<h1 style='text-align: center; color: #FF6347;'>Movie Recommendation System 🎥</h1>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["View All Movies", "User Watch History", "Recommendations for User"])

# Section 1: View All Movies
if page == "View All Movies":
    st.markdown("## 📽️ **All Movies**")
    movies = fetch_all_movies(movies_collection)
    for movie in movies:
        st.markdown(f"🎞️ **Title**: {movie['title']}  \n📂 **Genre**: {movie['genre']}")

# Section 2: User Watch History
elif page == "User Watch History":
    st.markdown("## 🕵️ **User Watch History**")
    users = list(users_collection.find({}, {"_id": 1, "name": 1}))
    user_options = {user["_id"]: user["name"] for user in users}
    selected_user_id = st.selectbox("Select User:", options=user_options.keys(), format_func=lambda x: f"{x} - {user_options[x]}")
    
   # users = fetch_all_users(users_collection)  # Use MongoDB to fetch user details if needed
   # selected_user_id = st.selectbox("Select User:", options=["user1", "user2"], format_func=lambda x: f"User {x}")

    if st.button("Get Watch History"):
        watch_history = fetch_watch_history(redis_client, selected_user_id)
        if watch_history:
            watched_titles = fetch_movie_titles_by_ids(movies_collection, watch_history)
            st.success(f"🎉 User has watched: {', '.join(watched_titles)}")
        else:
            st.warning("⚠️ No watch history found for this user.")

# Section 3: Recommendations for User
elif page == "Recommendations for User":
    st.markdown("## 🎯 **Recommendations for User**")
    users = list(users_collection.find({}, {"_id": 1, "name": 1}))
    user_options = {user["_id"]: user["name"] for user in users}
    selected_user_id = st.selectbox("Select User for Recommendations:", options=user_options.keys(), format_func=lambda x: f"{x} - {user_options[x]}")
    
    #selected_user_id = st.selectbox("Select User for Recommendations:", ["user1", "user2"])
    if st.button("Get Recommendations"):
        watch_history = fetch_watch_history(redis_client, selected_user_id)
        genres = fetch_movie_genres(movies_collection, watch_history)
        if genres:
            recommendations = fetch_recommended_movies(neo4j_driver, genres, watch_history)
            if recommendations:
                st.success("🎥 Recommended Movies:")
                for rec in recommendations:
                    st.write(f"- **{rec['title']}** (Genre: {rec['genre']})")
            else:
                st.warning("⚠️ No recommendations found.")
        else:
            st.warning("⚠️ No genres found in the user's watch history.")
