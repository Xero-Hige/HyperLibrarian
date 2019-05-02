import redis
import json

# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = "redis"
redis_port = 6379
redis_password = ""

FILES_EXPIRE_BASE_TIME = 20


class RedisCache:

    def __init__(self):
        self.connection = redis.StrictRedis(host=redis_host,
                                            port=redis_port,
                                            password=redis_password,
                                            decode_responses=True)

    def get(self, key):
        msg = self.connection.get(key)
        if not msg:
            return None

        self.connection.expire(key, FILES_EXPIRE_BASE_TIME * 2)
        return json.loads(msg)

    def set(self, key, value):
        value = json.dumps(value)
        self.connection.set(key, value, ex=FILES_EXPIRE_BASE_TIME)
