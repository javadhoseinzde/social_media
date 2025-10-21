from rest_framework.views import exception_handler
from rest_framework import status
from .message import result_message

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = result_message(
            message="ERROR",
            status_code=response.status_code,
            result=response.data
        )
    else:
        response = Response(
            result_message(
                message="ERROR",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=str(exc)
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response