from __future__ import annotations

from typing import List, Self, Annotated

from fastapi.params import Query
from pydantic import BaseModel


class PaginatedParams(BaseModel):

    page: Annotated[int,Query(1, ge=1)]
    per_page: Annotated[int, Query(100, ge=0)]

    @property
    def limit(self) -> int:
        return self.per_page

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


class PaginatedResponse[M: BaseModel](BaseModel):

    count: int
    fields: List[M]

    @classmethod
    def paginate(cls, fields: List[M]) -> PaginatedResponse:
        return cls(
            fields=fields,
            count=len(fields)
        )
