from common.mediator.cqrs import Query


class FindMemberQuery(Query):
    def __init__(self, search_string: str):
        self.search_string = search_string
