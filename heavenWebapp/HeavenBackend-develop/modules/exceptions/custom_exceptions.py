from rest_framework import exceptions, status, viewsets
from rest_framework.exceptions import APIException


class CustomDictException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid input."
    default_code = "invalid"


ERROR_BOOK = {
    # Plan
    "Plan": "AA",
    "PlanGroup": "AB",
    "PlanSeries": "AD",
    # HW Spec
    "Soc": "BB",
    "Power": "BA",
}

ERROR_CODE_BOOK = {}
