import random
import string
import pytest
from prehashed import PrehashedDict
from prehashed.prehashed import sha1_fn

# Utilities
def rand_string(min_=5, max_=26):
    res = [random.choice(string.ascii_letters) for _ in rand_len(min_, max_)]
    return ''.join(res)

def rand_len(min_=5, max_=11):
    return range(random.randint(min_, max_))

def find(needles, haystack, hash_me=True):
    found = True
    for k, v in needles:
        if hash_me:
            k = sha1_fn(k)
        found_me = False
        for h in haystack:
            if h[0] == k and h[1] == v:
                found_me = True
        found = found_me
    return found

@pytest.fixture
def d():
    return PrehashedDict()
