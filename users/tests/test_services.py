import pytest
from users.otp import send_otp
from Bookstore.redis_setup import CacheSetUp
from Bookstore.BookstoreError import BookStoreError


def test_givenPhoneNumber_WhenWrongFormat_raisesException():
    with pytest.raises(BookStoreError):
        assert send_otp(+91809557)


def test_RedisConnection_whenServerNotRunning_raisesException():
    cache_instance = CacheSetUp()
    with pytest.raises(BookStoreError):
        cache_instance.set_value("key", "value")
