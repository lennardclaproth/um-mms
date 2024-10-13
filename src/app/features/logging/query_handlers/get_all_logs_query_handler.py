from typing import List
from app.features.logging.queries.get_all_logs_query import GetAllLogsQuery
from common.dependency_injection.auto_wire import AutoWire
from common.logging.logger import CustomLogger, LoggerInterface
from common.mediator.cqrs import QueryHandler


class GetAllLogsQueryHandler(QueryHandler[GetAllLogsQuery, List[str]], metaclass=AutoWire):

    def __init__(self, logger: LoggerInterface):
        super().__init__()
        self._logger = logger

    def handle(self, query) -> List[str]:
        logs = self._logger.read_logs()
        return logs
