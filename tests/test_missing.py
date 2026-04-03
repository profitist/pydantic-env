from src.missing import MissingType


def test_missing_is_not_none():
    assert MissingType() is not None

def test_missing_singleton():
    obj1 = MissingType()
    obj2 = MissingType()
    assert obj1 is obj2