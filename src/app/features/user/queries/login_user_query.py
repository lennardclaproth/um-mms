from app.context.user import User
from common.mediator.cqrs import Query


class LoginUserQuery(Query):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
