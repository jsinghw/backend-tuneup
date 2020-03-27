#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment"""

__author__ = "jsingh"

import cProfile
import pstats
import io
from functools import wraps
import timeit


def profile(func):
    """A function that can be used as a decorator to measure performance"""
    """HELP FROM https://www.youtube.com/watch?v=8qEnExGLZfY"""
    # You need to understand how decorators are constructed and used.
    # Be sure to review the lesson material on decorators, they are used
    # extensively in Django and Flask.
    @wraps(func)
    def inner_wrapper(*args, **kwargs):
        # Do something before calling func_to_decorate
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        # Do something after calling func_to_decorate
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s)
        ps.strip_dirs().sort_stats('cumulative').print_stats()
        print(s.getvalue())
        return result
    return inner_wrapper


def read_movies(src):
    """Returns a list of movie titles"""
    print('Reading file: {}'.format(src))
    with open(src, 'r') as f:
        return f.read().splitlines()


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list"""
    movies = read_movies(src)
    movies = [movie.lower() for movie in movies]
    movies.sort()
    duplicates = [
        movie1 for movie1, movie2 in zip(movies[:-1],
                                         movies[1:]) if movie1 == movie2]
    return duplicates


def timeit_helper(main):
    """Part A:  Obtain some profiling measurements using timeit"""
    num = 7
    rept = 5
    t = timeit.Timer(stmt=main, setup='from __main__ import main')
    result = min(t.repeat(repeat=rept, number=num))
    print(
        'Best time across {} repeats of {} runs per repeat: {:.12}'.format(
            rept, num, result)
        )


def main():
    """Computes a list of duplicate movie entries"""
    result = (find_duplicate_movies('movies.txt'))
    print('Found {} duplicate movies:'.format(len(result)))
    print('\n'.join(result))


if __name__ == '__main__':
    timeit_helper('main()')
