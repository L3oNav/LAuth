import redis

def get_redis_connection():
    return redis.Redis(host="redis") 
