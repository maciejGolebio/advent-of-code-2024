from itertools import product
from typing import List

def timer(func):
    def wrapper(*args, **kwargs):
        from time import time
        start = time()
        result = func(*args, **kwargs)
        print(f"Function {func.__name__}{args} took {time() - start} seconds")
        return result
    
    return wrapper

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Function {func.__name__}{args} is called")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__}{args} is returning {result}")
        return result
    
    return wrapper


#@logger
def combine_lists(lists: List[List[str]]) -> List[str]:
    return [''.join(comb) for comb in product(*lists)]