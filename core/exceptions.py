from rest_framework import status
from rest_framework.exceptions import ErrorDetail, NotFound
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def permission_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response and response.status_code == status.HTTP_403_FORBIDDEN:
        error_detail = ErrorDetail(NotFound.default_detail)
        error_detail.code = NotFound.default_code
        response.status_code = NotFound.status_code
        response.data["detail"] = "Access denied. Kindly contact admin."

    return response


class InvalidUserTypeError(APIException):
    status_code = 400
    default_detail = "Invalid user type."
    default_code = "invalid_user_type"
