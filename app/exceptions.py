from fastapi import status
from fastapi import HTTPException


class PermissionDeniedException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Permission denied"


class WorkInProgressException(HTTPException):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    detail = "Work in progress"


# ======================================================


class ConfigException(Exception):
    pass
