from rest_framework import serializers
from .models import User
from django.core.validators import RegexValidator


class LoginSerializer(serializers.ModelSerializer):
    mobile_num = serializers.CharField(
        validators=[
            RegexValidator(regex="^\+[0-9]{2}(\s)?[0-9]{10}$"),
        ],
        required=False,
    )

    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["username", "mobile_num"]
