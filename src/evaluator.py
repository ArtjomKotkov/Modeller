from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypedDict, NotRequired
from typing import Any

__all__ = [
    'Dialect',
    'Evaluable',
    'ExecutingOptions'
]


class ExecutingOptions(TypedDict):
    wrap_attrs_in: NotRequired[Any]
    wrap_values_in: NotRequired[Any]


class Evaluable:
    def evaluate(self, dialect: Dialect, options: ExecutingOptions = None): ...


class Dialect(ABC):
    def make(self, expression: Evaluable):
        return expression.evaluate(self)

    @abstractmethod
    def _and_(self, value1: Any, value2: Any): ...

    @abstractmethod
    def _or_(self, value1: Any, value2: Any): ...

    @abstractmethod
    def _not_(self, value: Any): ...

    @abstractmethod
    def _equal_(self, value1: Any, value2: Any): ...

    @abstractmethod
    def _not_equal_(self, value1: Any, value2: Any): ...

    @abstractmethod
    def _lt_(self, value1: Any, value2: Any): ...

    @abstractmethod
    def _gt_(self, value1: Any, value2: Any): ...

    @abstractmethod
    def _lte_(self, value1: Any, value2: Any): ...

    @abstractmethod
    def _gte_(self, value1: Any, value2: Any): ...

    @abstractmethod
    def _in_(self, value1: Any, value2: Any): ...

    @abstractmethod
    def _has_(self, value1: Any, value2: Any): ...

    @abstractmethod
    def _has_any_(self, value1: Any, value2: Any): ...
