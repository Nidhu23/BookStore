import redis
from Bookstore import settings, BookstoreError, responses
from rest_framework import status


class CacheSetUp:
    def __init__(self):
        self.redis_instance = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
        )

    def set_value(self, key, value):
        try:
            self.redis_instance.set(key, value)
        except redis.exceptions.ConnectionError:
            raise BookstoreError.BookStoreError(
                responses.get_response("RedisConnectionError"), 500
            )

    def get_value(self, key):
        try:
            return self.redis_instance.get(key).decode()
        except redis.exceptions.ConnectionError:
            raise BookstoreError.BookStoreError(
                responses.get_response("RedisConnectionError"), 500
            )

    def del_value(self, key):
        try:
            return self.redis_instance.delete(key)
        except redis.exceptions.ConnectionError:
            raise BookstoreError.BookStoreError(
                responses.get_response("RedisConnectionError"), 500
            )
