from typing import Any

from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        errors: dict[
            str,
            Any,
        ]
        | None = None,
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "errors": errors,
            },
        )
        self.message = message
        self.errors = errors


class NotFoundError(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(status.HTTP_404_NOT_FOUND, f"{resource} not found")


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message)


class ForbiddenError(AppException):
    def __init__(
        self,
        message: str = "You do not have permission to perform this action",
    ):
        super().__init__(status.HTTP_403_FORBIDDEN, message)


class ConflictError(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(status.HTTP_409_CONFLICT, message)


class ValidationError(AppException):
    def __init__(
        self,
        message: str = "Validation failed",
        errors: dict[
            str,
            Any,
        ]
        | None = None,
    ):
        super().__init__(status.HTTP_400_BAD_REQUEST, message, errors)
