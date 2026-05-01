from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None
    message: str | None = None
    errors: dict[str, Any] | None = None

    @classmethod
    def ok(cls, data: Any, message: str | None = None) -> "ApiResponse":
        return cls(success=True, data=data, message=message)

    @classmethod
    def fail(
        cls, message: str, errors: dict[str, Any] | None = None
    ) -> "ApiResponse":
        return cls(success=False, data=None, message=message, errors=errors)
