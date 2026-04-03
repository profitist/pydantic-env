import pytest
import os

from pydantic import BaseModel, Field

from src.core import EnvField, EnvFieldError

@pytest.fixture()
def setup_env():
    os.environ['TEST_ENV_FIELD'] = 'test'
    yield
    del os.environ['TEST_ENV_FIELD']


def test_env_field__correct(setup_env):
    class TestModel(BaseModel):
        test_field: str = EnvField('TEST_ENV_FIELD')

    obj = TestModel()

    assert obj.test_field == 'test'


def test_env_field_default__correct():
    class TestModel(BaseModel):
        test_field: str = EnvField('TEST_ENV_FIELD', default='test')
    obj = TestModel()
    assert obj.test_field == 'test'

def test_env_field_required__raises():
    with pytest.raises(EnvFieldError):
        class TestModel(BaseModel):
            test_field: str = EnvField('TEST_ENV_FIELD')

        obj = TestModel()


def test_reads_from_env__int():
    os.environ['TEST_ENV_FIELD_INT'] = '3000'

    class TestModel(BaseModel):
        port: int = EnvField('TEST_ENV_FIELD_INT', default=8080, cast=int)

    obj = TestModel()
    assert obj.port == 3000

    del os.environ['TEST_ENV_FIELD_INT']


def test_reads_from_env__float():
    os.environ['TEST_ENV_FIELD_FLOAT'] = '3000.5'
    class TestModel(BaseModel):
        port: float = EnvField('TEST_ENV_FIELD_FLOAT', default=8080, cast=float)

    obj = TestModel()
    assert obj.port == 3000.5

    del os.environ['TEST_ENV_FIELD_FLOAT']


def test_reads_from_env__bool():
    os.environ['TEST_ENV_FIELD_BOOL'] = 'True'
    class TestModel(BaseModel):
        port: bool = EnvField('TEST_ENV_FIELD_BOOL', default=False, cast=bool)

    obj = TestModel()
    assert obj.port is True

    del os.environ['TEST_ENV_FIELD_BOOL']


def test_reads_from_env__incorrect_cast():
    os.environ['TEST_ENV_FIELD_INT'] = 'some'
    with pytest.raises(EnvFieldError):
        class TestModel(BaseModel):
            port: str = EnvField('TEST_ENV_FIELD_INT', cast=int)

        obj = TestModel()