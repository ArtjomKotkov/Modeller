from src.dialects import SqlAlchemyDialect, MongoDbDialect, PythonDialect
from src.main import SModel


if __name__ == '__main__':
    sqlalchemy_dialect = SqlAlchemyDialect()
    mongodb_dialect = MongoDbDialect()
    python_dialect = PythonDialect()

    # Моделька
    class TestModel(SModel):
        a: str = 'asfasfas'
        b: int

    # Спека
    spec = (TestModel.b > 12) & (TestModel.a == '1')

    # Компилим под sqlalchemy
    from sqlalchemy.dialects.postgresql import dialect
    import sqlalchemy as sa

    d = dialect()

    b = sqlalchemy_dialect.make(spec)

    # Скомпиленный еще и алхимией рузультат
    g = b.compile(dialect=d, compile_kwargs={"render_postcompile": True, 'literal_binds': True})
    print(g)
    # Компилим под mongodb
    # Готовый запрос для драйвера mongodb
    c = mongodb_dialect.make(spec)

    # Получаем питонячю спеку
    p = python_dialect.make(spec)

    # Тестовый пул моделей
    sp = [TestModel(a='1', b=13), TestModel(a='2', b=100), TestModel(a='3', b=1)]

    # Фильтруем по спеке
    result = list(filter(lambda model: p(model), sp))

    a = 12