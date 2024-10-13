from app.context.user import User
from common.mediator.cqrs import Query


class GetAllUsersQuery(Query):
    def __init__(self):
        pass
