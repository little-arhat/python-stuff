# -*- coding:utf-8 -*-

from __future__ import print_function

import itertools
import collections
import random
import string
import Queue

import graph

# start = "hit"
# end = "cog"
# dict = ["hot","dot","dog","lot","log","cog", "hit"]
# As one shortest transformation is "hit" -> "hot" -> "dot" -> "dog" -> "cog"
def word_ladder(start, stop, dictionary):
    if start not in dictionary or stop not in dictionary:
        raise ValueError("Dictionary missing start or stop")
    g = collections.defaultdict(set)
    buckets = collections.defaultdict(set)
    for word in dictionary:
        for i in range(len(word)):
            bucket = word[:i] + '_' + word[i+1:]
            buckets[bucket].add(word)
    for bucket_words in buckets.itervalues():
        for word in bucket_words:
            neighbours = bucket_words.difference([word])
            g[word].update(neighbours)
    # to prevent surprises w/ defaultdict
    g = dict(g)
    (_, pred) = graph.bfs(g, start)
    if stop not in pred:
        raise ValueError("Stop is not reachable")
    p = pred[stop]
    path = [stop, p]
    while p != start:
        p = pred[p]
        path.append(p)
    return list(reversed(path))


def navigate_pad(st, pad_width=5):
    alpha = string.lowercase
    # print pad
    for (i, l) in enumerate(alpha):
        if (i % pad_width) == 0:
            print()
        print(l, end='')
        if (i % pad_width) != (pad_width - 1):
            print(' ', end='')
    print()
    current_x = 0
    current_y = 0
    commands = []
    for letter in st:
        # ord(letter) - ord('a')
        # alpha.index(letter)
        # assuming sorted alphabeth:
        location = ord(letter) - ord(alpha[0])
        loc_x = location % pad_width
        loc_y = location / pad_width
        print('We are at ({}, {}). Target letter at ({}, {})'.format(current_x,
                                                                     current_y,
                                                                     loc_x,
                                                                     loc_y))
        hor_command = "right" if current_x < loc_x else "left"
        vert_command = "down" if current_y < loc_y else "up"
        commands.extend([hor_command] * abs(current_x - loc_x))
        commands.extend([vert_command] * abs(current_y - loc_y))
        commands.append("press")
        current_x = loc_x
        current_y = loc_y
    return commands


def radix_sort(L):
    return MSD_radix_string_sort(list(enumerate(L)))

def MSD_radix_string_sort(L, i=0):
    # base case (list must already be sorted)
    if len(L) <= 1:
        return L
    # divide (first by length, then by lexicographical order of the first character)
    done_bucket = []
    buckets = [ [] for x in range(27) ] # one for each letter in a-z
    for (rank, s) in L:
        if i >= len(s):
            done_bucket.append((rank, s))
        else:
            buckets[ord(s[i]) - ord('a')].append((rank, s))
    # conquer (recursively sort buckets)
    buckets = [ MSD_radix_string_sort(b, i + 1) for b in buckets ]
    # marry (chain all buckets together)
    return done_bucket + [ b for blist in buckets for b in blist ]
