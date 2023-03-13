from typing import Any

import sqlalchemy as sa

from ..base import Dialect, Evaluable, ExecutingOptions


__all__ = [
    'SqlAlchemyDialect',
]


class SqlAlchemyDialect(Dialect):
    def make(self, expression: Evaluable):
        options: ExecutingOptions = {
            'wrap_attrs_in': sa.sql.literal_column,
        }

        return expression.evaluate(self, options)

    def _and_(self, value1: Any, value2: Any):
        return sa.sql.and_(value1, value2)

    def _or_(self, value1: Any, value2: Any):
        return sa.sql.or_(value1, value2)

    def _not_(self, value: Any):
        return sa.sql.not_(value)

    def _equal_(self, value1: Any, value2: Any):
        return value1 == value2

    def _not_equal_(self, value1: Any, value2: Any):
        return self._not_(self._equal_(value1, value2))

    def _lt_(self, value1: Any, value2: Any):
        return value1 < value2

    def _gt_(self, value1: Any, value2: Any):
        return value1 > value2

    def _lte_(self, value1: Any, value2: Any):
        return value1 <= value2

    def _gte_(self, value1: Any, value2: Any):
        return value1 >= value2

    def _in_(self, value1: Any, value2: Any):
        return value1.in_(value2)

    def _has_(self, value1: Any, value2: Any):
        raise value2.in_(value1)

    def _has_any_(self, value1: Any, value2: Any):
        raise NotImplemented
