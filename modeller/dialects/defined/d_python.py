from typing import Any, Callable

from ..base import Dialect, Evaluable, ExecutingOptions


__all__ = [
    'PythonDialect',
]


def _attr_getter(attr: str) -> Callable:
    return lambda model: getattr(model, attr)


def _value_getter(value: Any) -> Callable:
    return lambda model: value


class PythonDialect(Dialect):
    def make(self, expression: Evaluable):
        options: ExecutingOptions = {
            'wrap_attrs_in': _attr_getter,
            'wrap_values_in': _value_getter,
        }

        return expression.evaluate(self, options)

    def _and_(self, value1: Any, value2: Any):
        return lambda model: value1(model) and value2(model)

    def _or_(self, value1: Any, value2: Any):
        return lambda model: value1(model) or value2(model)

    def _not_(self, value: Any):
        return lambda model: not value(model)

    def _equal_(self, value1: Any, value2: Any):
        return lambda model: value1(model) == value2(model)

    def _not_equal_(self, value1: Any, value2: Any):
        return self._not_(self._equal_(value1, value2))

    def _lt_(self, value1: Any, value2: Any):
        return lambda model: value1(model) < value2(model)

    def _gt_(self, value1: Any, value2: Any):
        return lambda model: value1(model) > value2(model)

    def _lte_(self, value1: Any, value2: Any):
        return lambda model: value1(model) <= value2(model)

    def _gte_(self, value1: Any, value2: Any):
        return lambda model: value1(model) >= value2(model)

    def _in_(self, value1: Any, value2: Any):
        return lambda model: value1(model) in value2(model)

    def _has_(self, value1: Any, value2: Any):
        raise self._in_(value2, value1)

    def _has_any_(self, value1: Any, value2: Any):
        raise NotImplemented
