import pytest
from utils import rand_string, d

# Test gets
def test_getitem(d):
    key = rand_string()
    value = rand_string()
    d[key] = value
    assert d[key] == value

def test_getitem_fail(d):
    key = rand_string()
    with pytest.raises(KeyError):
        d[key]

def test_get_none(d):
    key = rand_string()
    res = d.get(key)
    assert res is None

def test_get_default(d):
    key = rand_string()
    default = rand_string()
    res = d.get(key, default)
    assert res == default

def test_pop_removes(d):
    key = rand_string()
    value = rand_string()
    default = rand_string()
    d[key] = value
    _ = d.pop(key, default)
    assert key not in d

def test_pop_there_default(d):
    key = rand_string()
    value = rand_string()
    default = rand_string()
    d[key] = value
    res = d.pop(key, default)
    assert res != default
    assert res == value

def test_pop_there_no_default(d):
    key = rand_string()
    value = rand_string()
    d[key] = value
    res = d.pop(key)
    assert res == value

def test_pop_not_there_default(d):
    key = rand_string()
    default = rand_string()
    res = d.pop(key, default)
    assert res == default

def test_pop_not_there_no_default(d):
    key = rand_string()
    with pytest.raises(KeyError):
        d.pop(key)
