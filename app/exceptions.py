from fastapi import status
from fastapi import HTTPException


class BaseAppError(HTTPException):
    def __init__(
        self,
        status_code: int | None = None,
        detail: str | None = None,
        headers=None,
        *args,
        **kwargs,
    ):
        if status_code is None:
            status_code = self.status_code

        if detail is None:
            detail = self.detail

        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
            *args,
            **kwargs,
        )


class UnauthorizedError(BaseAppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Unauthorized"

    # !TODO: remove
    # def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"):
    #     super().__init__(status_code=status_code, detail=detail)


class PermissionDeniedError(BaseAppError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Permission denied"

    # !TODO: remove
    # def __init__(self, status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"):
    #     super().__init__(status_code=status_code, detail=detail)


class WorkInProgressError(BaseAppError):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    detail = "Work in progress"

    # !TODO: remove
    # def __init__(self, status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Work in progress"):
    #     super().__init__(status_code=status_code, detail=detail)


# ======================================================


class ConfigException(Exception):
    pass
