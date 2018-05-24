import os
import random
import pickle
from unittest.mock import patch
import pytest
from prehashed import PrehashedDict
from prehashed.prehashed import sha1_fn
from utils import rand_string, rand_len, find, d

@pytest.fixture
def file_cleanup():
    file_name = 'test.p'
    yield file_name
    try:
        os.remove(file_name)
    except:
        pass

# Test pickling
def test_pickle(file_cleanup):
    file_name = file_cleanup
    keys = [rand_string() for _ in rand_len()]
    vals = [rand_string() for _ in keys]
    d = PrehashedDict({k: v for k, v in zip(keys, vals)})
    pickle.dump(d, open(file_name, 'wb'))
    d1 = pickle.load(open(file_name, 'rb'))
    for k in keys:
        assert k in d
        assert k in d1
    for k, v in zip(keys, vals):
        assert d1[k] == v
    assert d == d1

# Test fromkeys
def test_from_keys():
    keys = [rand_string() for _ in rand_len()]
    d = PrehashedDict.fromkeys(keys)
    for k in keys:
        assert d[k] == None

def test_from_keys_value(d):
    keys = [rand_string() for _ in rand_len()]
    value = rand_string()
    d = PrehashedDict.fromkeys(keys, value)
    for k in keys:
        assert d[k] == value

# Test process args
def test_process_args_none(d):
    res = list(d._process_args())
    assert not res

def test_process_args_kwargs(d):
    kwargs = {rand_string(): rand_string() for _ in rand_len()}
    print(kwargs)
    res = list(d._process_args(**kwargs))
    assert find(kwargs.items(), res)

def test_process_args_dict(d):
    dic = {rand_string(): rand_string() for _ in rand_len()}
    res = list(d._process_args(dic))
    assert find(dic.items(), res)

def test_process_args_dict_kwargs(d):
    dic = {rand_string(): rand_string() for _ in rand_len()}
    kwargs = {rand_string(): rand_string() for _ in rand_len()}
    res = list(d._process_args(dic, **kwargs))
    assert find(dic.items(), res)
    assert find(kwargs.items(), res)

def test_process_args_prehased(d):
    d1 = PrehashedDict({rand_string(): rand_string() for _ in rand_len()})
    res = list(d._process_args(d1))
    assert find(d1.items(), res, hash_me=False)

def test_process_args_prehased_kwargs(d):
    d1 = PrehashedDict({rand_string(): rand_string() for _ in rand_len()})
    kwargs = {rand_string(): rand_string() for _ in rand_len()}
    res = list(d._process_args(d1, **kwargs))
    assert find(d1.items(), res, hash_me=False)
    assert find(kwargs.items(), res)

def test_process_args_iterable(d):
    it = [(rand_string(), rand_string()) for _ in rand_len()]
    res = list(d._process_args(it))
    assert find(it, res)

def test_process_args_iterable_kwargs(d):
    kwargs = {rand_string(): rand_string() for _ in rand_len()}
    it = [(rand_string(), rand_string()) for _ in rand_len()]
    res = list(d._process_args(it, **kwargs))
    assert find(it, res)
    assert find(kwargs.items(), res)

def test_init_calls_process_args():
    d = PrehashedDict({rand_string(): rand_string()})
    with patch('prehashed.prehashed.PrehashedDict._process_args') as mock:
        arg = random.choice([
            {rand_string(): rand_string()},
            ((rand_string(), rand_string())),
            (),
            d
        ])
        kwargs = {rand_string(): rand_string() for _ in rand_len(0, 2)}
        d = PrehashedDict(arg, **kwargs)
        mock.assert_called_once_with(arg, **kwargs)

def test_update_calls_process_args():
    d1 = PrehashedDict({rand_string(): rand_string()})
    d = PrehashedDict()
    with patch('prehashed.prehashed.PrehashedDict._process_args') as mock:
        arg = random.choice([
            {rand_string(): rand_string()},
            ((rand_string(), rand_string())),
            (),
            d1
        ])
        kwargs = {rand_string(): rand_string() for _ in rand_len(0, 2)}
        d.update(arg, **kwargs)
        mock.assert_called_once_with(arg, **kwargs)
