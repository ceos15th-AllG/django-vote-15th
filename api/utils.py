from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    m = 'ERROR'
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        if response.status_code == 400:
            m = "잘못된 요청입니다."
        elif response.status_code == 404:
            m = "데이터를 찾을 수 없습니다."
        elif response.status_code == 403:
            m = "해당 권한이 없습니다."
        response.data = {
            'status_code': response.status_code,
            'message': m,
            'detail': response.data
        }

    return response
