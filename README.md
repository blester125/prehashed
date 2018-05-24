# Prehashed

[![Build Status](https://travis-ci.com/blester125/prehashed.svg?branch=master)](https://travis-ci.com/blester125/prehashed)

A python dictionary that hashes keys before they are inserted to the dict. This yields substantial memory savings when the keys of a dictionary are quite large (for example long stings).

### Memory Graph

### Collisions

Obviously we want to know __What is the probability that I will have a hash collision?__. We can figure this out by asking the reverse. What is the probability that all of keys are unique? Once we have this we can answer the original question by subtracting this from 1.

Given N possible hash values (`2 ** 160` for sha1) we know the first hash will be unique, Then for the second one we know there are `N - 1` hashes we could use and still be unique, this means our probability is `N - 1 / N`. This continues for `N - 2, 3` etc. So if we are hashing `k` keys we can find the probability of them all being unique with `PI i=1 -> k-1 (N - i) / N`. This can be approximated with `e^((-k * (k - 1)) / (2 * N))`. This can be further approximated with (k * (k - 1) / (2 * N)) for small k because `1 - e^x ~= x` and when N is 2 ** 160 most k is small.

Graph

To sum this up here is a table with some of the probabilities of your keys colliding.

| k | Odds |
| - | ---- |
|`1.71x10^15` | `1 in 10 ^ 18` |
|`1.71x10^19` | `1 in 10 billion` |
|`1.71x10^21` | `1 in a million` |
|`1.71x10^23` | `1 in 100` |
|`1.42x10^24` | `1 in 2` |

So unless you plan use put `171,000,000,000,000,000,000,000` keys into this dict I wouldn't worry about collisions.

There is a small chance that keys will collide. When this happens this dictionary cannot detect that and as a result these keys will overwrite each other. This is so rare that git doesn't have a mitigation strategy either.

While a collisions are super rare if you are worried about it I would suggest that all of your values are the same type so that you aren't expecting a string and get an int in the super unlikely case if a collision.

If you are still scared about collisions there is also a function `initial_add(k, v)` that will modify your key until it doesn't have a collision, adds it to the dictionary, and returns the new key to use. You need to keep this key to get the value later so this kind of breaks the point of this dict where you want to be able to throw away your keys.
