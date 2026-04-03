import os

import pytest

from src.core import EnvConfig, EnvField, EnvFieldError


def test_envconfig_class():
    os.environ['TEST_ENV_FIELD_STR'] = 'test'
    os.environ['TEST_ENV_FIELD_INT'] = '3000'


    class TestModel(EnvConfig):
        env_prefix = 'TEST_'

        string: str = EnvField('ENV_FIELD_STR')
        integer: str = EnvField('ENV_FIELD_INT', cast=int)

    obj = TestModel()

    assert obj.string == 'test'
    assert obj.integer == 3000

    del os.environ['TEST_ENV_FIELD_STR']
    del os.environ['TEST_ENV_FIELD_INT']


def test_envconfig_class_missing_field():
    class TestModel(EnvConfig):
        env_prefix = 'TEST_'
        missing: str = EnvField('ENV_FIELD_MISSING', required=True)

    with pytest.raises(EnvFieldError):
        obj = TestModel()


def test_envconfig_default():
    class TestModel(EnvConfig):
        env_prefix = 'TEST_'
        port: int = EnvField('PORT', cast=int, default=8080)

    obj = TestModel()
    assert obj.port == 8080




