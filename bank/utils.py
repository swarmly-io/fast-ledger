
import itertools

def first_or_none(l): 
    return next(iter(l or []), None)

def flat_map(func, *iterable):
    return itertools.chain.from_iterable(map(func, *iterable))