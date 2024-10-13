from dataclasses import dataclass
from datetime import date
from uuid import UUID
from common.cryptography.data_encoder import Encoder
from common.dependency_injection.auto_wire import AutoWire
from common.logging.logger import LoggerInterface
from common.smart_db.context import DbContext
from common.smart_db.db_set import DbSet
from common.smart_db.query_builder import QueryBuilder


@dataclass
class Member:
    id: UUID
    membership_id: str
    first_name: str
    last_name: str
    gender: str
    weight: str
    street: str
    house_number: str
    zip_code: str
    city: str
    email_address: str
    phonenumber: str
    registration_date: date


class MemberDbSet(DbSet[Member], metaclass=AutoWire):
    def __init__(self, db_context: DbContext, encoder: Encoder, logger: LoggerInterface, query_builder: QueryBuilder):
        super().__init__(db_context, encoder=encoder, logger=logger, query_builder=query_builder)
