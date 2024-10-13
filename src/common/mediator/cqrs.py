from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic

TCommand = TypeVar('TCommand', bound='Command')
TQuery = TypeVar('TQuery', bound='Query')
TResult = TypeVar('TResult')

class Command(ABC):
    pass

class Query(ABC):
    pass

class CommandHandler(ABC, Generic[TCommand]):
    @abstractmethod
    def handle(self, command: TCommand) -> None:
        pass

class QueryHandler(ABC, Generic[TQuery, TResult]):
    @abstractmethod
    def handle(self, query: TQuery) -> TResult:
        pass