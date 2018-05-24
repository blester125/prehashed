import pytest
from utils import rand_string, d

# Test dels
def test_del_present(d):
    key = rand_string()
    value = rand_string()
    d[key] = value
    del d[key]
    with pytest.raises(KeyError):
        res = d[key]

def test_del_missing(d):
    key = rand_string()
    with pytest.raises(KeyError):
        del d[key]

# Test contains
def test_contains(d):
    key = rand_string()
    d[key] = rand_string()
    assert key in d

def test_not_contains(d):
    key = rand_string()
    assert key not in d

