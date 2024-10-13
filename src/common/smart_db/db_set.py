from abc import ABC
import datetime
import sqlite3
from typing import Any, Generic, List, Optional, Tuple, TypeVar, get_type_hints
import uuid

from common.cryptography.data_encoder import Encoder
from common.dependency_injection.auto_wire import AutoWire
from common.logging.logger import LoggerInterface
from common.smart_db.query_builder import QueryBuilder

T = TypeVar('T')


class DbSet(ABC, Generic[T]):

    def __init__(self, context: 'DbContext', encoder: Encoder, logger: LoggerInterface, query_builder: QueryBuilder):
        self._context = context
        self._encoder = encoder
        self._model_cls = self._get_model_class()
        self.model_cls = self._get_model_class()
        self.table_name = self.model_cls.__name__ + "s"
        self.fields = get_type_hints(self.model_cls)
        self.query_builder = query_builder
        self._logger = logger
        self.setup_table()

    def reset_query_builder(self):
        self.query_builder.reset()

    def _get_model_class(self) -> type:
        return self.__orig_bases__[0].__args__[0]

    def setup_table(self) -> None:
        fields_str = ", ".join(
            f"{name} {self._type_to_sqlite_type(t)}" for name, t in self.fields.items()
        )
        create_table_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({fields_str})"
        self._execute(create_table_query)

    def create(self, entity: T) -> None:
        encrypted_entity = self._encrypt_entity(entity)
        columns = ", ".join(self.fields.keys())
        placeholders = ", ".join("?" for _ in self.fields)
        insert_query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        self._execute(insert_query, self._to_row(encrypted_entity))

    def update(self, entity: T, attribute_name: str) -> None:
        if attribute_name not in self.fields:
            raise ValueError(
                f"Attribute {attribute_name} is not a valid field for this entity.")

        value_to_update = getattr(entity, attribute_name)
        if isinstance(value_to_update, str):
            encrypted_value = self._encoder.encrypt_data(value_to_update)
        else:
            encrypted_value = value_to_update

        update_query = f"UPDATE {self.table_name} SET {attribute_name} = ? WHERE id = ?"

        id_value = getattr(entity, 'id')

        parameters = (encrypted_value, id_value)

        self._execute(update_query, parameters)

    def delete(self, entity_id: int) -> None:
        delete_query = f"DELETE FROM {self.table_name} WHERE id = ?"
        self._execute(delete_query, (entity_id,))

    def get_all(self) -> List[T]:
        select_query = f"SELECT * FROM {self.table_name}"
        rows = self._fetchall(select_query)
        return [self._decrypt_entity(self._from_row(row)) for row in rows]

    def where(self, attribute):
        self.query_builder = self.query_builder.where(attribute)
        return self

    def like(self, value: str):
        self.query_builder = self.query_builder.like(value)
        return self

    def search(self, fields: List[str], value: str):
        self.query_builder = self.query_builder.search(fields, value)
        return self

    def equals(self, value: Any):
        self.query_builder = self.query_builder.equals(value)
        return self

    def in_(self, values: List[Any]):
        self.query_builder = self.query_builder.in_(values)
        return self

    def all(self) -> List[T]:
        combined_condition = self.query_builder.build()
        all_records = self.get_all()
        result = [
            record for record in all_records if combined_condition(record)]
        self._context.close_db()
        return result

    def first_or_none(self) -> Optional[T]:
        combined_condition = self.query_builder.build()
        all_records = self.get_all()
        for record in all_records:
            if combined_condition(record):
                self._context.close_db()
                return record
        self._context.close_db()
        return None

    def _encrypt_entity(self, entity: T) -> T:
        encrypted_entity = {}
        for field in self.fields.keys():
            value = getattr(entity, field)
            if isinstance(value, str):
                encrypted_entity[field] = self._encoder.encrypt_data(value)
            else:
                encrypted_entity[field] = value
        return self.model_cls(**encrypted_entity)

    def _decrypt_entity(self, entity: T) -> T:
        decrypted_entity = {}
        for field in self.fields.keys():
            value = getattr(entity, field)
            if isinstance(value, str):
                decrypted_entity[field] = self._encoder.decrypt_data(value)
            else:
                decrypted_entity[field] = value
        return self.model_cls(**decrypted_entity)

    def _from_row(self, row: Tuple) -> T:
        kwargs = {field: value for field,
                  value in zip(self.fields.keys(), row)}
        return self.model_cls(**kwargs)

    def _to_row(self, entity: T) -> Tuple:
        return tuple(getattr(entity, field) for field in self.fields)

    def _type_to_sqlite_type(self, python_type: type) -> str:
        if python_type == int:
            return "INTEGER"
        elif python_type == str:
            return "TEXT"
        elif python_type == float:
            return "REAL"
        elif python_type == uuid.UUID:
            return "TEXT"
        elif python_type == datetime or python_type == datetime.date:
            return "TEXT"
        else:
            raise ValueError(f"Unsupported type: {python_type}")

    def _execute(self, query: str, parameters: Tuple[Any, ...] = ()) -> sqlite3.Cursor:
        cursor = self._context.get_cursor()
        cursor.execute(query, parameters)
        self._logger.info("Successfully executed query.",
                          query=query, parameters=str(parameters))
        return cursor

    def _fetchall(self, query: str, parameters: Tuple[Any, ...] = ()) -> List[Tuple]:
        cursor = self._execute(query, parameters)
        return cursor.fetchall()

    def _fetchone(self, query: str, parameters: Tuple[Any, ...] = ()) -> Optional[Tuple]:
        cursor = self._execute(query, parameters)
        return cursor.fetchone()
