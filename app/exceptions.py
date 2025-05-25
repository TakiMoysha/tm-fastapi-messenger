from fastapi import status
from fastapi import HTTPException


class BaseAppError(HTTPException): ...


class PermissionDeniedError(BaseAppError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Permission denied"

    def __init__(self, status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"):
        super().__init__(status_code=status_code, detail=detail)


class WorkInProgressError(BaseAppError):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    detail = "Work in progress"

    def __init__(self, status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Work in progress"):
        super().__init__(status_code=status_code, detail=detail)


# ======================================================


class ConfigException(Exception):
    pass
