from abc import ABC
import os
import sqlite3
from typing import get_type_hints

from common.cryptography.data_encoder import Encoder
from common.dependency_injection.auto_wire import AutoWire
from common.smart_db.db_set import DbSet


class DbContext(ABC):
    def __init__(self, encoder: Encoder):
        self._db_path = "data/um-mms.db"
        self._encrypted_db_path = f"{self._db_path}.lcenc"
        self._connection = None
        self._encoder = encoder

    def get_cursor(self):
        if self._connection is None:
            self._encoder.decrypt_file(self._encrypted_db_path)
            self._connection = sqlite3.connect(self._db_path)
        return self._connection.cursor()

    def save_changes(self):
        if self._connection:
            self._connection.commit()
            self._connection.close()
            self._connection = None
            self._encoder.encrypt_file(self._db_path)

    def close_db(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            self._encoder.encrypt_file(self._db_path)

    def _create_empty_db(self):
        conn = sqlite3.connect(self._db_path)
        conn.close()
        self._encoder.encrypt_file(self._db_path)

    def initialize_db(self):
        if os.path.exists(self._encrypted_db_path):
            self._encoder.decrypt_file(self._encrypted_db_path)
        if os.path.exists(self._db_path):
            self._encoder.encrypt_file(self._db_path)
        else:
            self._create_empty_db()

    def initialize_tables(self):
        for attr_name, attr_type in get_type_hints(self.__class__).items():
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, DbSet):
                attr_value.setup_table()
