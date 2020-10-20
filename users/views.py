from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import request
from rest_framework.response import Response
from .models import User
from .serializers import LoginSerializer
from .otp import send_otp
from Bookstore import redis_setup
from rest_framework import status
import logging

logger = logging.getLogger("django")
# Create your views here.
@api_view(["POST"])
def login(request):
    try:
        redis_instance = redis_setup.get_redis_instance()
        username = request.data.get("user_name")
        mobile_num = request.data.get("mobile_num")
        if username == None and mobile_num == None:
            return Response("Please Enter either user name or mobile number for login")
        else:
            login_id = User.objects.get(Q(username=username) | Q(mobile_num=mobile_num))
            serializer = LoginSerializer(login_id)
            if serializer.is_valid:
                if serializer.data == []:
                    return Response(
                        {
                            "message": "user with this number or name does not exist",
                            "status": status.HTTP_404_NOT_FOUND,
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )
                mobile_num = serializer.data.get("mobile_num")
                username = serializer.data.get("username")
                OTP = send_otp(mobile_num)
                redis_instance.set("otp_" + username, OTP)
                return Response(
                    {"message": "OTP sent successfully", "status": status.HTTP_200_OK},
                    status=status.HTTP_200_OK,
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
            {
                "message": "user with this number or name does not exist",
                "status": status.HTTP_404_NOT_FOUND,
            },
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logger.error(e)
        return Response(
            {
                "message": "Something went wrong",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
