# Modeller
Current lib provides simple and common interface for making abstract specifications, and then compile to any defined or custom dialect.

### Using dialects
Using dialects to compile abstract specification to backend related code.
```python
from modeller import SModel
from modeller.dialects.defined import SqlAlchemyDialect, MongoDbDialect, PythonDialect

# Test model
class TestModel(SModel):
    a: str = 'asfasfas'
    b: int

# Test specification
spec = (TestModel.b > 12) & (TestModel.a == '1')


# Instancing dialects
sqlalchemy_dialect = SqlAlchemyDialect()

# Sqlalchemy spec compiling
sqlalchemy_spec = sqlalchemy_dialect.make(spec)

# Compiling spec forsure
from sqlalchemy.dialects.postgresql import dialect
g = sqlalchemy_spec.compile(dialect=dialect(), compile_kwargs={"render_postcompile": True, 'literal_binds': True})  # b > 12 AND a = '1'


# Mongodb spec compiling
mongodb_dialect = MongoDbDialect()
mongodb_spec = mongodb_dialect.make(spec)  # {'$and': [{'b': {'$gt': 12}}, {'a': '1'}]}


# Python callable spec compiling
python_dialect = PythonDialect()
python_spec = python_dialect.make(spec)

# Testing python spec by filtering model instances
sp = [TestModel(a='1', b=13), TestModel(a='2', b=100), TestModel(a='3', b=1)]
result = list(filter(lambda model: python_spec(model), sp))  # [TestModel{'a': '1', 'b': 13}]
```

### Implement custom dialect
Writting custom dialect based on default **Dialect** class.
```python
from modeller import Dialect

class CustomDialect(Dialect):
    
    # Define handling for each of operation methods
    def _and_(self, value1: Any, value2: Any):
        return {'and': [value1, value2]}

    def _or_(self, value1: Any, value2: Any):
        return {'or': [value1, value2]}

    def _not_(self, value: Any):
        return {'not': value}

    def _equal_(self, value1: Any, value2: Any):
        return {'eq': [value1, value2]}

    def _not_equal_(self, value1: Any, value2: Any):
        return {'neq': [value1, value2]}

    def _lt_(self, value1: Any, value2: Any):
        return {'lt': [value1, value2]}

    def _gt_(self, value1: Any, value2: Any):
        return {'gt': [value1, value2]}

    def _lte_(self, value1: Any, value2: Any):
        return {'lte': [value1, value2]}

    def _gte_(self, value1: Any, value2: Any):
        return {'gte': [value1, value2]}

    def _in_(self, value1: Any, value2: Any):
        return {'in': [value1, value2]}

    def _has_(self, value1: Any, value2: Any):
        return {'has': [value1, value2]}

    def _has_any_(self, value1: Any, value2: Any):
        raise NotImplemented
```