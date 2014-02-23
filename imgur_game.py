#!/usr/bin/env python


from __future__ import print_function
from urllib3 import PoolManager
# Disabling GPL code until resolved.
# https://github.com/winny-/imgurgame/issues/1
# from pyimgur import Imgur
from requests.exceptions import HTTPError
from re import compile, search
from collections import namedtuple


CLIENT_ID = 'a1dc76d0afc2f34'


Image = namedtuple('Image', ('id', 'type'))


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


def build_search(s):
    if len(s) != 5:
        raise RuntimeError('Imgur images are 5 letter long paths. '
                           '{} is {} characters long.'.format(s, len(s)))
    permutations = all_casings(s)
    return permutations


def game_http(s):
    """
    Take string and check for imgur URLs. Must be 5 characters long.
    Returns URLs that exist.
    """
    possible_ids = build_search(s)
    file_ext = compile(r'[a-zA-Z0-9]{5}\.(png|jpg|jpeg|gif)')
    http = PoolManager(40)
    for id_ in possible_ids:
        r = http.request('GET', 'http://imgur.com/'+id_)
        if r.status == 200:
            found_ext = search(file_ext, r.data).group(1)
            yield Image(id_, found_ext)


def game_api(s):
    """
    Take string and check for imgur URLs. Must be 5 characters long.
    Returns dicts representing URLs that exist. Dict looks like this:
    {
        'url': 'http://imgur.com/daURL',
        'direct': 'http://imgur.com/daURL.png',
        'id': 'daURL'
    }
    """
    raise NotImplemented()
    if len(s) != 5:
        raise RuntimeError('Imgur images are 5 letter long paths. '
                           '{} is {} characters long.'.format(s, len(s)))
    permutations = all_casings_sorted(s)
    im = Imgur(CLIENT_ID)
    for i in permutations:
        try:
            image = im.get_image(i)
            if image.link == 'http://i.imgur.com/removed.png':
                continue
            yield {
                'url': 'http://imgur.com/'+i,
                'direct': image.link,
                'id': i,
                'thumb': image.link_big_square,
            }
        except HTTPError:
            pass


def format(it, columns=3, sort=True):
    """Format iterable into columns. columns=3 by default."""
    c = 1
    it = sorted(it, reverse=True) if sort else it
    for i in it:
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
        valid_urls = (valid[0] for valid in game_http(arg))
        format(valid_urls)
