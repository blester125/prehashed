"""Benchmarking the size saving of the PrehashedDict."""

import sys
from pathlib import Path
from numbers import Number
from collections import Set, Mapping, deque, Counter
import matplotlib.pyplot as plt
from prehashed import PrehashedDict

def getsize(obj_0):
    """From: https://stackoverflow.com/a/30316760"""
    zero_depth_bases = (str, bytes, Number, range, bytearray)
    iteritems = 'items'
    """Recursively iterate to sum size of object & members."""
    def inner(obj, _seen_ids = set()):
        obj_id = id(obj)
        if obj_id in _seen_ids:
            return 0
        _seen_ids.add(obj_id)
        size = sys.getsizeof(obj)
        if isinstance(obj, zero_depth_bases):
            pass # bypass remaining control flow and return
        elif isinstance(obj, (tuple, list, Set, deque)):
            size += sum(inner(i) for i in obj)
        elif isinstance(obj, Mapping) or hasattr(obj, iteritems):
            size += sum(inner(k) + inner(v) for k, v in getattr(obj, iteritems)())
        # Check for custom object instances - may subclass above too
        if hasattr(obj, '__dict__'):
            size += inner(vars(obj))
        if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
            size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
        return size
    return inner(obj_0)

def graph():
    data_loc = Path('dm_stories_tokenized')
    d = PrehashedDict()
    dic = {}
    mine = []
    theirs = []
    for file_name in data_loc.glob("*.story"):
        data = open(file_name, 'r').read()
        d[data] = 1
        dic[data] = 1
        mine.append(getsize(d.keys()))
        theirs.append(getsize(dic.keys()))
    x = range(len(mine))
    plt.plot(x, mine)
    plt.plot(x, theirs)
    plt.show()


def main():
    data_loc = Path('dm_stories_tokenized')

    pre_d = PrehashedDict()
    pre_d2 = PrehashedDict(hash_fn=hash)
    d = {}
    for file_name in data_loc.glob("*.story"):
        data = open(file_name, "r").read()
        counts = Counter(data.split())
        pre_d[data] = counts
        pre_d2[data] = counts
        d[data] = counts

    print(f"Len of normal: {len(d)}, sha1: {len(pre_d)}, hash: {len(pre_d2)}")

    print(f"Size of keys with strings: {getsize(d.keys())}")
    print(f"Size of my prehased keys: {getsize(pre_d.keys())}")
    print(f"Size of my prehased keys (builtin hash): {getsize(pre_d2.keys())}")


if __name__ == "__main__":
    graph()
    main()
