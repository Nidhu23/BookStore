from rest_framework import status

response_message = {
    "product_doesnt_exist": {
        "message": "No books found",
        "status": status.HTTP_404_NOT_FOUND,
    },
    "InvalidSignatureError": {
        "message": "Wrong token,Please login again",
        "status": status.HTTP_401_UNAUTHORIZED,
    },
    "DecodeError": {
        "message": "Token,Please login again",
        "status": status.HTTP_401_UNAUTHORIZED,
    },
    "GetBookError": {
        "Error_message": "There was an error while fetching the books",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    },
    "EmptyBookList": {
        "Error_message": "No books found",
        "status_code": status.HTTP_404_NOT_FOUND,
    },
    "OtpSuccess": {"message": "OTP sent successfully", "status": status.HTTP_200_OK},
    "UserNotExist": {
        "message": "user with this number or name does not exist",
        "status": status.HTTP_404_NOT_FOUND,
    },
    "GenericError": {
        "error_message": "Something went wrong",
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
    },
    "LoginSuccess": {"message": "Successfully logged In", "status": status.HTTP_200_OK},
    "WrongOtp": {
        "message": "OTP you entered is wrong",
        "status": status.HTTP_400_BAD_REQUEST,
    },
    "TokenMissing": {"message": "Token missing", "status": status.HTTP_400_BAD_REQUEST},
    "OtpOrNameMissing": {
        "message": "Otp or username missing,Please enter both",
        "status": status.HTTP_400_BAD_REQUEST,
    },
    "LogoutSuccess": {
        "message": "Logged out successfully",
        "status": status.HTTP_200_OK,
    },
    "FieldError": {
        "message": "Field does does not exist,check field name",
        "status": status.HTTP_400_BAD_REQUEST,
    },
    "RedisConnectionError": {
        "message": "redis server connection refused",
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
    },
}


def get_response(key):
    return response_message.get(key)