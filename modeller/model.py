from typing import Any, Dict

from pydantic import create_model

from .combining import Box


class SMetaModel(type):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)

        instance._create_validation_model()

        return instance

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

    def as_dict(self) -> Dict[str, Any]:
        return self._store

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
            if key in cls.__annotations__.keys()
        }

    @classmethod
    def _validate(cls, data: dict) -> dict:
        if cls.__pydantic_model__ is None:
            cls._create_validation_model()
        return cls.__pydantic_model__(**data).dict()

    @classmethod
    def _create_validation_model(cls):
        annotations_scheme = {key: (value, ...) for key, value in cls.__annotations__.items()}
        cls.__pydantic_model__ = create_model('validation_model', **annotations_scheme)

    def __getattribute__(self, item: str) -> None:
        if (
                item.startswith('__') and item.endswith('__')
                or item.startswith('_')
                or item in self.__class__.__dict__.keys()
                or item in self.__dict__.keys()
        ):
            return super().__getattribute__(item)

        try:
            return self._store[item]
        except KeyError:
            return super().__getattribute__(item)

    def __setattr__(self, key, value) -> None:
        if key.startswith('_'):
            return super().__setattr__(key, value)

        if not self._store.get(key):
            raise AttributeError

        self._store[key] = value

    @classmethod
    def __get_validators__(cls):
        yield cls._dummy_validator

    @classmethod
    def _dummy_validator(cls, *args, **kwargs):
        return args[0]