import time

import redis
import json

# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = "redis"
redis_port = 6379
redis_password = ""


class RedisAnalytics:
    _EXPIRE_TIME = 60 * 60 * 27  # Prevents timezone problems
    __TIME_SLICE = 60 * 60
    __HANDLER_PREFIX = "analytics"

    __COUNTER_LIMITS = 100

    def __init__(self):
        self.connection = redis.StrictRedis(host=redis_host,
                                            port=redis_port,
                                            password=redis_password,
                                            decode_responses=True)

    def __get_key(self, key_time, data_class, increment=False):
        """"""
        timestamp = key_time / self.__TIME_SLICE

        return f"{self.__HANDLER_PREFIX}::{data_class}::{timestamp + 1 if increment else 0}"

    def __get_counter_key(self, data_class):
        return f"{self.__HANDLER_PREFIX}::{data_class}::counter"

    def touch(self, value, data_class, prevent_clear=False):
        actual_time = int(time.time())
        key = self.__get_counter_key(data_class)

        self.connection.zadd(key, {value: actual_time})

        if not prevent_clear:
            count = self.connection.zcard(key)
            if count > self.__COUNTER_LIMITS * 2:
                self.connection.zpopmin(key, count - self.__COUNTER_LIMITS * 1.1)

    def get_latest(self, data_class, n):
        key = self.__get_counter_key(data_class)
        return self.connection.zrange(key, 0, n, desc=True)

    def count(self, value, data_class, forced=False):
        actual_time = int(time.time())
        key = self.__get_key(actual_time, data_class)
        next_key = self.__get_key(actual_time, data_class, increment=True)

        score = self.connection.zadd(key, {value: 1 if not forced else 0}, incr=True)
        self.connection.zadd(next_key, {value: score})
        self.connection.expire(key, self._EXPIRE_TIME * 2)

        self.connection.set(f"{self.__HANDLER_PREFIX}::{data_class}::latest_touch", actual_time)

        if forced:
            self.connection.set(f"{self.__HANDLER_PREFIX}::{data_class}::latest_forced_touch", actual_time)

    def get_last_update(self, data_class):
        latest = self.connection.get(f"{self.__HANDLER_PREFIX}::{data_class}::latest_touch")
        latest_forced = self.connection.set(f"{self.__HANDLER_PREFIX}::{data_class}::latest_forced_touch")

        return latest, latest_forced

    def get_top_n(self, data_class, n):
        actual_time = int(time.time())
        key = self.__get_key(actual_time, data_class)

        return self.connection.zrange(key, 0, n, desc=True)
