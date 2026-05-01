from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose import JWTError

from app.core.exceptions import AppException


def _envelope(
    success: bool,
    data: Any,
    message: str,
    errors: Any = None,
) -> dict:
    resp: dict[str, Any] = {
        "success": success,
        "data": data,
        "message": message,
    }
    if errors is not None:
        resp["errors"] = errors
    return resp


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    detail = (
        exc.detail
        if isinstance(
            exc.detail,
            dict,
        )
        else {"message": str(exc.detail)}
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=_envelope(
            success=False,
            data=None,
            message=detail.get("message", "An error occurred"),
            errors=detail.get("errors"),
        ),
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    field_errors: dict[str, str] = {}
    for error in exc.errors():
        loc = " -> ".join(str(name) for name in error["loc"] if name != "body")
        field_errors[loc] = error["msg"]

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=_envelope(
            success=False,
            data=None,
            message="Validation failed",
            errors=field_errors,
        ),
    )


async def jwt_exception_handler(
    request: Request,
    exc: JWTError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=_envelope(
            success=False,
            data=None,
            message="Invalid or expired token",
        ),
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_envelope(
            success=False,
            data=None,
            message="An internal server error occurred",
        ),
    )
