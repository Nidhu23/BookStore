from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from Bookstore import settings, BookstoreError, responses
import jwt
from jwt.exceptions import InvalidSignatureError, DecodeError


def get_tokens(username, cache_instance):
    user = User.objects.get(username=username)
    tokens = RefreshToken.for_user(user)
    cache_instance.set_value("refresh_" + str(user.pk), str(tokens))
    return tokens


def delete_user(token, cache_instance):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        user_id = payload["user_id"]
        if cache_instance.del_value("refresh_" + str(user_id)) == 1:
            return 1
        return 0
    except InvalidSignatureError:
        raise BookstoreError.BookStoreError(
            responses.get_response("InvalidSignatureError"), 401
        )
    except DecodeError:
        raise BookstoreError.BookStoreError(responses.get_response("DecodeError"), 401)
