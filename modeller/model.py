from typing import Any

from pydantic import create_model

from .combining import Box


class SMetaModel(type):
    def __getattribute__(self, item: str):
        if item.startswith('__') and item.endswith('__'):
            return super().__getattribute__(item)

        if item in self.__annotations__.keys():
            return Box(value=item, is_attribute=True)
        else:
            return super().__getattribute__(item)


class SModel(metaclass=SMetaModel):
    def __init__(self, **kwargs):
        self._store = {}

        self._prepare(kwargs)

    def _prepare(self, data: dict) -> None:
        default_data = self._extract_default_values()

        data_to_validate = {
            **default_data,
            **data,
        }

        self._store = self._validate(data_to_validate)

    @classmethod
    def _extract_default_values(cls) -> dict[str, Any]:
        return {
            key: value
            for key, value
            in cls.__dict__.items()
            if key in cls.__annotations__.keys() and value is not None
        }

    def _validate(self, data: dict) -> dict:
        validation_model = self._create_validation_model()
        return validation_model(**data).dict()

    @classmethod
    def _create_validation_model(cls):
        annotations_scheme = {key: (value, ...) for key, value in cls.__annotations__.items()}
        return create_model('validation_model', **annotations_scheme)

    def __getattribute__(self, item: str):
        if item == '_store':
            return super().__getattribute__(item)

        try:
            return self._store[item]
        except KeyError:
            return super().__getattribute__(item)
