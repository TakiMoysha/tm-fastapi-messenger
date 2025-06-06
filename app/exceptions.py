from fastapi import status
from fastapi import HTTPException


class BaseAppError(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal server error"

    def __init__(
        self,
        status_code: int | None = None,
        detail: str | None = None,
        headers=None,
    ):
        if status_code is None:
            status_code = self.status_code

        if detail is None:
            detail = self.detail

        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )


class UnauthorizedError(BaseAppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Unauthorized"


class PermissionDeniedError(BaseAppError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Permission denied"


class WorkInProgressError(BaseAppError):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    detail = "Work in progress"


# ======================================================


class ConfigException(Exception):
    pass
