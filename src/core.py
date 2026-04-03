import os
from typing import Any, Annotated, ClassVar

import pydantic
from pydantic import Field, BaseModel, field_validator
from src.missing import MISSING

class EnvFieldError(Exception):
    pass


class EnvField:
    def __init__(self, name: str, default: Any = MISSING, required: bool = True, cast: type = str):
        self.name = name
        self.default = default
        self.required = required
        self.cast = cast


class EnvConfig(BaseModel):
    env_prefix: ClassVar[str] = ''

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for field_name, field in list(cls.__annotations__.items()):
            value = cls.__dict__.get(field_name)
            if isinstance(value, EnvField):
                env_field = value
                env_field.name = f'{cls.env_prefix}{env_field.name}'

                def make_field_factory(ef: EnvField):
                    def _factory():
                        env_value = os.getenv(ef.name)
                        try:
                            if env_value is not None:
                                return ef.cast(env_value)
                        except ValueError, TypeError:
                            raise EnvFieldError(
                                f"Invalid value for env var: {ef.name} with type: {ef.cast}")
                        if ef.default is not MISSING:
                            return ef.default

                        if not ef.required:
                            return None
                        raise EnvFieldError(f"Missing required env var: {ef.name}")

                    return _factory

                setattr(cls, field_name, Field(default_factory=make_field_factory(env_field)))
