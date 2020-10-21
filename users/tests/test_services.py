import pytest
from users.otp import send_otp
from Bookstore.BookstoreError import BookStoreError


def test_givenPhoneNumber_WhenWrongFormat_raisesException():
    with pytest.raises(BookStoreError):
        assert send_otp(+91809557)