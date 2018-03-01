import redis
from api.utils.redis_pool import POOL


conn = redis.Redis(connection_pool=POOL)

# conn.hset("oldboy", "chuan", "123")
# data = conn.hget("oldboy", "chuan")
# conn.hset("oldboy", "chuck", 58)
conn.hincrby("oldboy", "chuck", -30)
data = conn.hget("oldboy", "chuck")

print(data)
