from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """При любой ошибке возварщает код 400"""
    response = exception_handler(exc, context)
    if response and response.status_code:
        response.status_code = 400
    return response
