# Prehashed

[![Build Status](https://travis-ci.com/blester125/prehashed.svg?branch=master)](https://travis-ci.com/blester125/prehashed)

A python dictionary that hashes keys before they are inserted to the dict. This yields substantial memory savings when the keys of a dictionary are quite large (for example long stings).

The point of this is that we can store keys that are really large (long strings) cheaply. For example when storing the documents in the tokenized Dailymail dataset the keys take up `1.018 GB` while this implementation takes `10.53 MB`. A small space saving (`7.79 MB` vs `10.53 MB`) can be found using the built in `hash` function but the results of this are not shareable across runs because python changes the seed across runs.

### Collisions

Obviously we want to know __What is the probability that I will have a hash collision?__. We can figure this out by asking the reverse. What is the probability that all of keys are unique? Once we have this we can answer the original question by subtracting this from 1.

Given N possible hash values (![equ](https://latex.codecogs.com/gif.latex?2^{160}) for sha1) we know the first hash will be unique, Then for the second one we know there are ![equ](https://latex.codecogs.com/gif.latex?N-1) hashes we could use and still be unique, this means our probability is ![equ](https://latex.codecogs.com/gif.latex?\frac{N-1}{N}). This continues for ![equ](https://latex.codecogs.com/gif.latex?N-2), ![equ](https://latex.codecogs.com/gif.latex?N-3) etc. So if we are hashing ![equ](https://latex.codecogs.com/gif.latex?k) keys we can find the probability of them all being unique with ![equ](https://latex.codecogs.com/gif.latex?\Pi^{k-1}_{i&space;=&space;1}\frac{(N-i)}{N}). The probability of a collision can then be approximated with ![equ](https://latex.codecogs.com/gif.latex?1-e^{\frac{-k(k-1)}{2N}}). This can be further approximated with ![equ](https://latex.codecogs.com/gif.latex?\frac{k(k-1)}{2N}) for small ![equ](https://latex.codecogs.com/gif.latex?k) because ![equ](https://latex.codecogs.com/gif.latex?1&space;-&space;e^{-x}&space;\approx&space;x) and when ![equ](https://latex.codecogs.com/gif.latex?N) is ![equ](https://latex.codecogs.com/gif.latex?2^{160}) most ![equ](https://latex.codecogs.com/gif.latex?k) is small.

Graph

To sum this up here is a table with some of the probabilities of your keys colliding.

| k | Odds |
| - | ---- |
| ![equ](https://latex.codecogs.com/gif.latex?1.71\times10^{18}) | ![equ](https://latex.codecogs.com/gif.latex?1&space;\text{&space;in&space;}&space;10^{18}) |
| ![equ](https://latex.codecogs.com/gif.latex?1.71\times10^{19}) | ![equ](https://latex.codecogs.com/gif.latex?1&space;\text{&space;in&space;}&space;10&space;\text{&space;billion}) |
| ![equ](https://latex.codecogs.com/gif.latex?1.71\times10^{21}) | ![equ](https://latex.codecogs.com/gif.latex?1&space;\text{&space;in&space;a&space;million}) |
| ![equ](https://latex.codecogs.com/gif.latex?1.71\times10^{23}) | ![equ](https://latex.codecogs.com/gif.latex?1&space;\text{&space;in&space;}&space;100) |
| ![equ](https://latex.codecogs.com/gif.latex?1.42\times10^{24}) | ![equ](https://latex.codecogs.com/gif.latex?1&space;\text{&space;in&space;}&space;2) |

So unless you plan use put `171,000,000,000,000,000,000,000` keys into this dict or people will die if your code has bugs I wouldn't worry about collisions.

There is a small chance that keys will collide. When this happens this dictionary cannot detect that and as a result these keys will overwrite each other. This is so rare that git doesn't have a mitigation strategy either.

While a collisions are super rare if you are worried about it I would suggest that all of your values are the same type so that you aren't expecting a string and get an int in the super unlikely case if a collision.

If you are still scared about collisions there is also a function `initial_add(k, v)` that will modify your key until it doesn't have a collision, adds it to the dictionary, and returns the new key to use. You need to keep this key to get the value later so this kind of breaks the point of this dict where you want to be able to throw away your keys.
