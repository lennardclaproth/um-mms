from app.context.member import MemberDbSet
from app.context.user import UserDbSet
from common.cryptography.data_encoder import Encoder
from common.dependency_injection.auto_wire import AutoWire
from common.smart_db.context import DbContext


class UniqueMealDbContext(DbContext, metaclass=AutoWire):

    members: MemberDbSet
    users: UserDbSet

    def __init__(self, encoder: Encoder):
        super().__init__(encoder)

    def initialize_db(self):
        super().initialize_db()
        self.members = MemberDbSet()
        self.users = UserDbSet()
        super().initialize_tables()
