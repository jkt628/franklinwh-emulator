from typing import Generic, TypeVar

from pydantic import BaseModel

Result = TypeVar("Result")


class Response(BaseModel, Generic[Result]):
    code: int = 200
    message: str = "Success"
    result: Result
    success: bool = True


class ResponseWithTotal(Response[Result]):
    total: int = 1
