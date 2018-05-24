import random
import pytest
from utils import rand_string
from prehashed.prehashed import sha1_fn

@pytest.fixture
def class_ex():
    class A:
        def __init__(self):
            self.x = 45
        def __str__(self):
            return f"{self.__name__}.x = {self.x}"

# sha1 tests
def test_sha1_type():
    key = rand_string()
    assert isinstance(sha1_fn(key), int)

def test_sha1_value():
    key = 'test'
    gold = 966482230667555116936258103322711973649032657875
    assert sha1_fn(key) == gold

def test_sha1_int_type():
    key = random.randint(2, 101)
    assert isinstance(sha1_fn(key), int)

def test_sha1_int_value():
    key = 1
    gold = 304942582444936629325699363757435820077590259883
    assert sha1_fn(key) == gold

def test_sha1_obj_type(class_ex):
    assert isinstance(sha1_fn(class_ex), int)

def test_sha1_obj_value(class_ex):
    gold = 633327772932199023258151861061014836005222876887
    assert sha1_fn(class_ex) == gold
