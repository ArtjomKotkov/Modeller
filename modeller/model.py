from typing import Any, Dict, Type

from pydantic import create_model, BaseModel
from pydantic.main import BaseModel

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
    __pydantic_model__: Type[BaseModel]

    def __init__(self, **kwargs):
        self._set_kwargs(**kwargs)
        self._pre_validate()

    def _set_kwargs(self, **kwargs) -> None:
        default_values = self._extract_default_values()

        self.__dict__.update(default_values)
        self.__dict__.update(kwargs)

    def as_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def _pre_validate(self) -> None:
         self._validate(self.__dict__)

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
        return cls.__pydantic_model__(**data).dict()

    @classmethod
    def _create_validation_model(cls):
        annotations_scheme = {key: (value, ...) for key, value in cls.__annotations__.items()}
        cls.__pydantic_model__ = create_model(
            'validation_model',
            **annotations_scheme,
        )

    @classmethod
    def __get_validators__(cls):
        yield cls._dummy_validator

    @classmethod
    def _dummy_validator(cls, *args, **kwargs):
        return args[0]
