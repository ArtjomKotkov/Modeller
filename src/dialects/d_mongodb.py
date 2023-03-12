from typing import Any

from src.evaluator import Dialect


__all__ = [
    'MongoDbDialect',
]


class MongoDbDialect(Dialect):
    def _and_(self, value1: Any, value2: Any):
        return {'$and': [value1, value2]}

    def _or_(self, value1: Any, value2: Any):
        return {'$or': [value1, value2]}

    def _not_(self, value: Any):
        return {'$not': value}

    def _equal_(self, value1: Any, value2: Any):
        return {value1: value2}

    def _not_equal_(self, value1: Any, value2: Any):
        return self._not_(self._equal_(value1, value2))

    def _lt_(self, value1: Any, value2: Any):
        return {value1: {'$lt': value2}}

    def _gt_(self, value1: Any, value2: Any):
        return {value1: {'$gt': value2}}

    def _lte_(self, value1: Any, value2: Any):
        return {value1: {'$lte': value2}}

    def _gte_(self, value1: Any, value2: Any):
        return {value1: {'$gte': value2}}

    def _in_(self, value1: Any, value2: Any):
        return {value1: {'$in': value2}}

    def _has_(self, value1: Any, value2: Any):
        return self._equal_(value1, value2)

    def _has_any_(self, value1: Any, value2: Any):
        return self._in_(value1, value2)
