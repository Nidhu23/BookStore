from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import request, status
from rest_framework.response import Response
from .models import User
from .serializers import LoginSerializer
from .otp import send_otp
from Bookstore import redis_setup, responses, BookstoreError
import logging
from .services import get_tokens, delete_user

cache_instance = redis_setup.CacheSetUp()
logger = logging.getLogger("django")
# Create your views here.
@api_view(["POST"])
def login(request):
    """
    API for user login

    Parameter:
    argument(1): request method with request data containing either
    user name or mobile number

    Returns:
    sends user verification otp
    """
    try:
        username = request.data.get("username")
        mobile_num = request.data.get("mobile_num")
        if username == None and mobile_num == None:
            return Response("Please Enter either user name or mobile number for login")
        else:
            login_id = User.objects.get(Q(username=username) | Q(mobile_num=mobile_num))
            serializer = LoginSerializer(login_id)
            if serializer.is_valid:
                if serializer.data == []:
                    return Response(
                        responses.get_response("UserNotExist"),
                        status=responses.get_response("UserNotExist").get("status"),
                    )
                mobile_num = serializer.data.get("mobile_num")
                username = serializer.data.get("username")
                OTP = send_otp(mobile_num)
                cache_instance.set_value("otp_" + username, OTP)
                return Response(
                    responses.get_response("OtpSuccess"),
                    status=responses.get_response("OtpSuccess").get("status"),
                )
            else:
                return Response(
                    {
                        "message": serializer.errors,
                        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
    except User.DoesNotExist:
        return Response(
            responses.get_response("UserNotExist"),
            status=responses.get_response("UserNotExist").get("status"),
        )
    except BookstoreError.BookStoreError as error:
        return Response(error.message, error.status)
    except Exception as e:
        logger.error(e)
        return Response(
            responses.get_response("GenericError"),
            status=responses.get_response("GenericError").get("status"),
        )


@api_view(["POST"])
def verify_otp(request):
    """
    API to verify otp

    Parameter:
    argument(1): request method with request data containing user name
    and otp

    Returns:
    verifies otp and sends tokens in response header
    """
    try:
        username = request.data.get("username")
        otp = request.data.get("otp")
        if username == None or otp == None:
            return Response(
                responses.get_response("OtpOrNameMissing"),
                status=responses.get_response("OtpOrNameMissing").get("status"),
            )
        generated_otp = cache_instance.get_value("otp_" + username)
        if otp == generated_otp:
            if cache_instance.del_value("otp_" + username) == 1:
                tokens = get_tokens(username, cache_instance)
                return Response(
                    responses.get_response("LoginSuccess"),
                    headers={
                        "access_token": str(tokens.access_token),
                        "refresh": str(tokens),
                    },
                    status=responses.get_response("LoginSuccess").get("status"),
                )
        else:
            return Response(
                responses.get_response("WrongOtp"),
                status=responses.get_response("WrongOtp").get("status"),
            )
    except BookstoreError.BookStoreError as error:
        return Response(error.message, error.status)
    except Exception as e:
        logger.error(e)
        return Response(
            responses.get_response("GenericError"),
            status=responses.get_response("GenericError").get("status"),
        )


@api_view(["GET"])
def logout(request):
    """
    API to log user out

    Parameter:
    argument(1): request method with request header containing refresh token

    Returns:
    logged out message
    """
    try:
        token = request.headers.get("token")
        if token == None:
            return Response(
                responses.get_response("TokenMissing"),
                status=responses.get_response("TokenMissing").get("status"),
            )
        delete_user(token, cache_instance)
        return Response(
            responses.get_response("LogoutSuccess"),
            status=responses.get_response("LogoutSuccess").get("status"),
        )
    except BookstoreError.BookStoreError as error:
        return Response(error.message, error.status)
    except Exception as e:
        logger.error(e)
        return Response(
            responses.get_response("GenericError"),
            status=responses.get_response("GenericError").get("status"),
        )
