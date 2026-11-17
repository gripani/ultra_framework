from collections.abc import Iterable

from sqlalchemy.orm import Session, Query


class SessionMixin:

    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def add(self, e: object) -> None:
        self._session.add(e)

    def flush(self) -> None:
        self._session.flush()

    def bulk_save_objects(self, batch: Iterable) -> None:
        self._session.bulk_save_objects(batch)

    def query[T](self, entity_class: type[T]) -> Query[T]:
        return self._session.query(entity_class)

    def delete_one(self, e: object) -> None:
        self._session.delete(e)
