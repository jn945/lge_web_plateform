import logging
import logging.config
from datetime import datetime

from django.core import exceptions as djexceptions
from django.http.response import Http404
from django.utils import timezone

# from modules.settings import logger
from heaven.settings import base
from heaven.settings.base import DEBUG
from modules.exceptions.custom_exceptions import CustomDictException
from modules.exceptions.exception_codes import STATUS_RSP_INTERNAL_ERROR
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .custom_exceptions import ERROR_BOOK

logging_settings = base.LOGGING
logging.config.dictConfig(logging_settings)
logger = logging.getLogger("my_logger")


def custom_exception_handler(exc, context):
    logger.error("[CUSTOM_EXCEPTION_HANDLER_ERROR]")
    logger.error(f"[{datetime.now()}]")
    logger.error("> exc")
    logger.error(f"{exc}")
    logger.error("> context")
    logger.error(f"{context}")

    response = exception_handler(exc, context)
    except_json = {}

    print("exc입니다 + ", type(exc), exc)
    print("view입니다 + ", context["view"].queryset.model.__name__)
    if response is not None:
        print(response)
        if isinstance(exc, exceptions.ParseError):
            status = 400
            error = {"code": "CE001", "message": str(exc)}
        elif isinstance(exc, exceptions.AuthenticationFailed):
            status = 401
            error = {"code": "CE101", "message": str(exc)}
        elif isinstance(exc, exceptions.NotAuthenticated):
            status = 401
            error = {"code": "CE101", "message": str(exc)}
        elif isinstance(exc, exceptions.PermissionDenied):
            status = 403
            error = {"code": "CE102", "message": str(exc)}
        elif isinstance(exc, exceptions.NotFound) or isinstance(exc, Http404):
            status = 404
            error = {"code": "CE200", "message": str(exc)}
        elif isinstance(exc, exceptions.MethodNotAllowed):
            status = 405
            error = {"code": "CE300", "message": str(exc)}
        elif isinstance(exc, exceptions.NotAcceptable):
            status = 406
            error = {"code": "CE310", "message": str(exc)}
        elif isinstance(exc, exceptions.Throttled):
            status = 429
            error = {"code": "CE800", "message": str(exc)}
        elif isinstance(exc, exceptions.ValidationError):
            status = 400
            error = {"code": "CE001", "detail": str(exc)}
        else:
            status = 500
            error = {"code": "CE900", "detail": str(exc)}

        response_json = {
            "datetime": timezone.now(),
            "error": error,
        }

        return Response(response_json, status=status)
    else:
        status = 500
        print("타입 입니다", type(exc), exc)
        print("into the else")
        print(type(exc))
        except_json["datetime"] = timezone.now()
        except_json["error"] = {"code": "CE900", "detail": str(exc)}

        return Response(except_json, status=status)
