from __future__ import annotations

from copy import copy
from typing import Any

from .evaluator import Dialect, Evaluable, ExecutingOptions


class Combinable:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)


class Comparable:
    def __eq__(self, other):
        return Equal(self, other)

    def __ne__(self, other):
        return NotEqual(self, other)

    def __lt__(self, other):
        return Lt(self, other)

    def __gt__(self, other):
        return Gt(self,other)

    def __le__(self, other):
        return Lte(self, other)

    def __ge__(self, other):
        return Gte(self, other)

    def in_(self, other: list | tuple | Box):
        return In(self, other)

    def has_(self, other):
        return Has(self,other)

    def has_any_(self, other):
        return HasAny(self, other)


class Combiner:
    def __init__(self, value1: Any, value2: Any) -> None:
        self._value1 = self._wrap_value_if_need(value1)
        self._value2 = self._wrap_value_if_need(value2)

    @staticmethod
    def _wrap_value_if_need(value: Any) -> Box:
        if not isinstance(value, (Box, Combiner, Evaluable)):
            return Box(value)
        else:
            return value


class Box(Evaluable, Comparable):
    def __init__(self, value: Any, is_attribute: bool = False):
        self._value = value
        self._is_attribute = is_attribute

    def evaluate(self, _: Dialect, options: ExecutingOptions = None):
        value = copy(self._value)

        if options:
            attr_wrapper = options.get('wrap_attrs_in')
            if self._is_attribute and attr_wrapper:
                value = attr_wrapper(value)

            value_wrapper = options.get('wrap_values_in')
            if not self._is_attribute and value_wrapper:
                value = value_wrapper(value)

        return value

    @property
    def is_attribute(self) -> bool:
        return self._is_attribute


class And(Combiner, Combinable, Evaluable):
    def evaluate(self, dialect: Dialect, options: ExecutingOptions = None):
        return dialect._and_(self._value1.evaluate(dialect, options), self._value2.evaluate(dialect, options))


class Or(Combiner, Combinable, Evaluable):
    def evaluate(self, dialect: Dialect, options: ExecutingOptions = None):
        return dialect._or_(self._value1.evaluate(dialect, options), self._value2.evaluate(dialect, options))


class Not(Box, Combinable, Evaluable):
    def evaluate(self, dialect: Dialect, options: ExecutingOptions = None):
        return dialect._not_(self._value.evaluate(dialect, options))


class Equal(Combiner, Combinable, Evaluable):
    def evaluate(self, dialect: Dialect, options: ExecutingOptions = None):
        return dialect._equal_(self._value1.evaluate(dialect, options), self._value2.evaluate(dialect, options))


class NotEqual(Combiner, Combinable, Evaluable):
    def evaluate(self, dialect: Dialect, options: ExecutingOptions = None):
        return dialect._not_equal_(self._value1.evaluate(dialect, options), self._value2.evaluate(dialect, options))


class Lt(Combiner, Combinable, Evaluable):
    def evaluate(self, dialect: Dialect, options: ExecutingOptions = None):
        return dialect._lt_(self._value1.evaluate(dialect, options), self._value2.evaluate(dialect, options))


class Gt(Combiner, Combinable, Evaluable):
    def evaluate(self, dialect: Dialect, options: ExecutingOptions = None):
        return dialect._gt_(self._value1.evaluate(dialect, options), self._value2.evaluate(dialect, options))


class Lte(Combiner, Combinable, Evaluable):
    def evaluate(self, dialect: Dialect, options: ExecutingOptions = None):
        return dialect._lte_(self._value1.evaluate(dialect, options), self._value2.evaluate(dialect, options))


class Gte(Combiner, Combinable, Evaluable):
    def evaluate(self, dialect: Dialect, options: ExecutingOptions = None):
        return dialect._gte_(self._value1.evaluate(dialect, options), self._value2.evaluate(dialect, options))


class In(Combiner, Combinable, Evaluable):
    def evaluate(self, dialect: Dialect, options: ExecutingOptions = None):
        return dialect._in_(self._value1.evaluate(dialect, options), self._value2.evaluate(dialect, options))


class Has(Combiner, Combinable, Evaluable):
    def evaluate(self, dialect: Dialect, options: ExecutingOptions = None):
        return dialect._has_(self._value1.evaluate(dialect, options), self._value2.evaluate(dialect, options))


class HasAny(Combiner, Combinable, Evaluable):
    def evaluate(self, dialect: Dialect, options: ExecutingOptions = None):
        return dialect._has_any_(self._value1.evaluate(dialect, options), self._value2.evaluate(dialect, options))
