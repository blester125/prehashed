from utils import rand_string, d
from prehashed import PrehashedDict
from prehashed.prehashed import sha1_fn

# Test inserts
def test_insert(d):
    key = rand_string()
    value = rand_string()
    d[key] = value
    assert key in d
    assert super(PrehashedDict, d).__contains__(sha1_fn(key))
    assert d[key] == value
    assert super(PrehashedDict, d).__getitem__(sha1_fn(key))

def test_overwrite(d):
    key = rand_string()
    value = rand_string()
    new_value = rand_string()
    d[key] = value
    assert d[key] == value
    d[key] = new_value
    assert d[key] == new_value

def test_set_default_not_there(d):
    key = rand_string()
    value = rand_string()
    res = d.setdefault(key, value)
    assert res == value

def test_set_default_there(d):
    key = rand_string()
    value = rand_string()
    default = rand_string()
    d[key] = value
    res = d.setdefault(key, default)
    assert res == value

def test_set_default_later_lookup(d):
    key = rand_string()
    value = rand_string()
    res = d.setdefault(key, value)
    assert res == value
    res = d[key]
    assert res == value

def test_initial_add():
    key = rand_string()
    value = rand_string()
    new_value = rand_string()
    d = PrehashedDict(((key, value),))
    new_key = d.initial_add(key, new_value)
    assert d[new_key] == new_value
    assert d[key] == value
    assert key != new_key
    assert len(new_key) > len(key)
