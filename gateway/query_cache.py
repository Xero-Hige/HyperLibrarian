import redis
import json

# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = "redis"
redis_port = 6379
redis_password = ""


class RedisCache:

    _EXPIRE_BASE_TIME = 60 * 45
    __HANDLER_PREFIX = "cache::"

    def __init__(self):
        self.connection = redis.StrictRedis(host=redis_host,
                                            port=redis_port,
                                            password=redis_password,
                                            decode_responses=True)

    def get(self, key):
        key = self.__HANDLER_PREFIX + key
        msg = self.connection.get(key)
        if not msg:
            return None

        self.connection.expire(key, self._EXPIRE_BASE_TIME * 2)
        return json.loads(msg)

    def set(self, key, value):
        key = self.__HANDLER_PREFIX + key
        value = json.dumps(value)
        self.connection.set(key, value, ex= self._EXPIRE_BASE_TIME)
