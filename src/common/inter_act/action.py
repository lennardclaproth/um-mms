from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class ActionInterface(ABC, Generic[T]):

    @abstractmethod
    def act(self, input: T, page: 'PageInterface', **kwargs) -> None:
        pass
