import random
from utils import rand_string, rand_len, d
from prehashed import PrehashedDict

# Test copies
def test_copy_same_keys(d):
    keys = [rand_string() for _ in rand_len()]
    values = [rand_string() for _ in keys]
    d = PrehashedDict(zip(keys, values))
    g = d.copy()
    for k in keys:
        assert k in g

def test_copy_same_values(d):
    keys = [rand_string() for _ in rand_len()]
    values = [rand_string() for _ in keys]
    d = PrehashedDict(zip(keys, values))
    g = d.copy()
    for k, v in zip(keys, values):
        assert g[k] == v

def test_copy_change_one_copy(d):
    keys = [rand_string() for _ in rand_len()]
    values = [rand_string() for _ in keys]
    d = PrehashedDict(zip(keys, values))
    g = d.copy()
    new_val = rand_string()
    changed_key = random.choice(keys)
    g[changed_key] = new_val
    assert g[changed_key] == new_val
    assert d[changed_key] != new_val

def test_copy_add_one_copy(d):
    keys = [rand_string() for _ in rand_len()]
    values = [rand_string() for _ in keys]
    d = PrehashedDict(zip(keys, values))
    g = d.copy()
    new_key = rand_string()
    new_val = rand_string()
    g[new_key] = new_val
    assert g[new_key] == new_val
    assert new_key in g
    assert new_key not in d

def test_copy_delete_one_copy(d):
    keys = [rand_string() for _ in rand_len()]
    values = [rand_string() for _ in keys]
    d = PrehashedDict(zip(keys, values))
    g = d.copy()
    del_key = random.choice(keys)
    del g[del_key]
    assert del_key in d
    assert del_key not in g

def test_copy_change_one_old(d):
    keys = [rand_string() for _ in rand_len()]
    values = [rand_string() for _ in keys]
    d = PrehashedDict(zip(keys, values))
    g = d.copy()
    new_val = rand_string()
    changed_key = random.choice(keys)
    d[changed_key] = new_val
    assert d[changed_key] == new_val
    assert g[changed_key] != new_val

def test_copy_add_one_old(d):
    keys = [rand_string() for _ in rand_len()]
    values = [rand_string() for _ in keys]
    d = PrehashedDict(zip(keys, values))
    g = d.copy()
    new_key = rand_string()
    new_val = rand_string()
    d[new_key] = new_val
    assert d[new_key] == new_val
    assert new_key in d
    assert new_key not in g

def test_copy_delete_one_old(d):
    keys = [rand_string() for _ in rand_len()]
    values = [rand_string() for _ in keys]
    d = PrehashedDict(zip(keys, values))
    g = d.copy()
    del_key = random.choice(keys)
    del d[del_key]
    assert del_key in g
    assert del_key not in d

def test_copy_is_shallow(d):
    keys = [rand_string() for _ in rand_len()]
    values = [rand_string() for _ in keys]
    d = PrehashedDict(zip(keys, values))
    d['12'] = [1, 2, 3]
    g = d.copy()
    g['12'].append(4)
    assert d['12'] == [1, 2, 3, 4]
