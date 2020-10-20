import math, random
from twilio.rest import Client
from Bookstore import settings


account_sid = settings.TWILIO_SID
auth_token = settings.TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)


def gen_otp():
    DIGITS = "0123456789"
    OTP = ""
    for digit in range(4):
        OTP += DIGITS[math.floor(random.random() * 10)]
    return OTP


def send_otp(phone_num):
    OTP = gen_otp()

    message = client.messages.create(
        body=f"your OTP is {OTP}",
        from_=settings.TWILIO_NUMBER,
        to=phone_num,
    )
    return OTP