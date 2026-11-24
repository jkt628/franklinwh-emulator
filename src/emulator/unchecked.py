from typing import Any, Union

from pydantic import BaseModel


class _PostChecked(BaseModel):
    def model_post_init(self, context: Any) -> None:
        for n, f in self.__class__.model_fields.items():
            if getattr(self, n) is None and not (
                f.annotation is None
                or (f.annotation is Union and None not in f.annotation.__args__)
            ):
                raise NotImplementedError


# these class members are intentionally unchecked because __init__ runs with incomplete information.
# model_post_init throws an error to force child classes to initialize properly.

# pyright: reportAssignmentType=false


class _Noise(_PostChecked):
    basis: float = None
    two_percent: float = None
    zero_two_percent: float = None


class _Stats(_PostChecked):
    status: int = None
