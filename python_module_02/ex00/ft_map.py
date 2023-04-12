#!/usr/bin/env python3
""" My own version of map()

"""
from collections.abc import Iterable

def ft_map(function_to_apply, iterable):
    """Map the function to all elements of the iterable.
    Args:
        function_to_apply: a function taking an iterable.
        iterable: an iterable object (list, tuple, iterator).
    Returns:
        An iterable.
        None if the iterable can not be used by the function.
    """
    try:
        if isinstance(iterable, Iterable):
            for i in iterable:
                yield function_to_apply(i)
        else:
            return None
    except Exception as exc: 
        print(exc)

# print(ft_map(lambda dum: dum + 1, x))
