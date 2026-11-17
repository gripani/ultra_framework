from itertools import batched
from typing import List, Union, Callable, Type, Literal

from sqlalchemy import ColumnElement, LambdaElement
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import SQLCoreOperations
from sqlalchemy.sql.roles import ExpressionElementRole, TypedColumnsClauseRole

from ultra_framework.entities.sql_entity import SQLEntity
from ultra_framework.mixins.session_mixin import SessionMixin

type Criterion[T] = Union[
    ColumnElement[T],
    SQLCoreOperations[T],
    ExpressionElementRole[T],
    TypedColumnsClauseRole[T],
    Callable[[], ColumnElement[T] | LambdaElement]
]


class CRUDRepository[M: SQLEntity, ID](SessionMixin):

    entity_class: Type[M]
    pk_column_dict: dict[Literal["pk"], ColumnElement[ID]]

    def save(self, entity: M) -> M:
        self.add(entity)
        self.flush()
        return entity

    def save_many(self, entities: list[M], n_batch: int = 1000) -> list[M]:
        new_entities: list[M] = []
        for batch in batched(entities, n_batch):
            self.bulk_save_objects(batch)
            self.flush()
            new_entities.extend(batch)
        return new_entities

    def find_all(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by = None
    ) -> list[M]:
        query = self.query(self.entity_class)
        if order_by is None:
            query = query.order_by(self.pk_column_dict["pk"])
        else:
            query = query.order_by(order_by)

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        return query.all()

    def find_by_pk(self, idx: ID) -> M | None:
        return self.query(self.entity_class).filter(self.pk_column_dict["pk"] == idx).first()

    def delete(self, entity: M) -> None:
        self.delete_one(entity)

    def filter_by_conditions(
            self,
            conditions: List[Criterion[bool]],
            limit: int | None = None,
            offset: int | None = None,
            order_by = None
    ) -> Query[M]:
        query = self.query(self.entity_class).filter(*conditions)
        if order_by is None:
            query = query.order_by(self.pk_column_dict["pk"])
        else:
            query = query.order_by(order_by)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query
