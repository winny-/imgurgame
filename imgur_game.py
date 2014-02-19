#!/usr/bin/env python


from __future__ import print_function
from urllib3 import PoolManager


def all_casings(input_string):
    """
    Get all case permutations, takes into account non-alphabetic characters.
    Based off of http://stackoverflow.com/a/6792898/2720026
    """

    if not input_string:
        yield ''
    else:
        first = input_string[:1]
        upper, lower = first.upper(), first.lower()
        if lower == upper:
            for sub_casing in all_casings(input_string[1:]):
                yield first + sub_casing
        else:
            for sub_casing in all_casings(input_string[1:]):
                yield lower + sub_casing
                yield upper + sub_casing


def exists(urls):
    """Yields each url in urls that exists (returns HTTP status 200)."""
    http = PoolManager(40)
    for url in urls:
        r = http.request('HEAD', url)
        if r.status == 200:
            yield url


def imgur_game(s):
    """
    Take string and check for imgur URLs. Must be 5 characters long.
    """
    if len(s) != 5:
        raise RuntimeError('Imgur images are 5 letter long paths. ' +
                           '{} is {} characters long.'.format(s, len(s)))
    permutations = all_casings(s)
    urls = ('http://imgur.com/'+p for p in permutations)
    return exists(urls)


def format(it, columns=3):
    """Format iterable into columns. columns=3 by default."""
    c = 1
    for i in sorted(it, reverse=True):
        if c < columns:
            print(i, end='  ')
            c += 1
        else:
            c = 1
            print(i)
    if c != 1:
        print()


if __name__ == '__main__':
    import sys

    args = sys.argv[1:]
    for arg in args:
        format(imgur_game(arg))
