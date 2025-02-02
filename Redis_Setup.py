import redis
# redis connection function
def get_redis_client():
    """Establishes a Redis client connection."""
    redis_host = "redis-13496.c44.us-east-1-2.ec2.redns.redis-cloud.com"
    redis_port = 13496
    redis_password = "zCF8PWvWx10Llqe5udewQ71xHy6GANsA"
    return redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

def fetch_watch_history(redis_client, user_id):
    """Fetches the watch history for a user from Redis."""
    watch_history = redis_client.get(f"watched:{user_id}")
    if watch_history:
        return list(map(int, watch_history.split(',')))  # Convert to list of integers
    return []
