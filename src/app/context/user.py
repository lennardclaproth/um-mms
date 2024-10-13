from dataclasses import dataclass
from datetime import date
from uuid import UUID
from enum import Enum
from common.cryptography.data_encoder import Encoder
from common.dependency_injection.auto_wire import AutoWire
from common.logging.logger import LoggerInterface
from common.smart_db.context import DbContext
from common.smart_db.db_set import DbSet
from common.smart_db.query_builder import QueryBuilder


class Roles(Enum):
    SUPERADMIN = "super_admin"
    ADMIN = "admin"
    CONSULTANT = "consultant"


@dataclass
class User():
    id: UUID
    username: str
    password: str
    first_name: str
    last_name: str
    role: str
    registration_date: date


class UserDbSet(DbSet[User], metaclass=AutoWire):
    def __init__(self, db_context: DbContext, encoder: Encoder, logger: LoggerInterface, query_builder: QueryBuilder):
        super().__init__(db_context, encoder=encoder,
                         logger=logger, query_builder=query_builder)
