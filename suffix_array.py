# -*- coding:utf-8 -*-

from __future__ import print_function

import itertools
import collections
import random
import string
import Queue


class SuffixTree(object):
    def __init__(self, st):
        self.string = st
        self.root = Node()
    def print_tree(self):
        self.root.print_node()
        print()
    def __repr__(self):
        return 'SuffixTree of %s:%s' % (self.string,
                                        self.root)


class Node(object):
    def __init__(self, parent=None, path_label=None):
        self.parent = parent
        self.path_label = path_label
        if parent and path_label:
            self.distance = self.parent.distance + len(path_label)
        else:
            self.distance = 0
        self.branches = []
    def add_node(self, path_label):
        n = Node(self, path_label)
        self.branches.append(n)
        return n
    def connect_node(self, node, path_label):
        node.path_label = path_label
        node.parent = self
        node.distance = node.parent.distance + len(path_label)
        self.branches.append(node)
        return node
    def __repr__(self):
        if self.path_label:
            if self.branches:
                return 'InternalNode(%s):%s' % (self.path_label, self.branches)
            else:
                return 'Leaf(%s)' % (self.path_label)
        else:
            return 'Root:%s' % (self.branches)
    def print_node(self, offset=0):
        if self.path_label:
            pl = '__%s' % self.path_label
        else:
            pl =  '.'
        print(pl, sep='', end='')
        no = offset + len(pl) + len('__')
        if self.branches:
            print('__')
            for branch in self.branches:
                print('%s|' % (' ' * no))
                print('%s|' % (' ' * no), sep='', end='')
                branch.print_node(offset=no + len('|'))
        else:
            print()


class SuffixArray(object):
    def __init__(self, st):
        self.st = st
        self.pos = make_suffix_array(st)
        rank = [0] * len(self.st)
        for i in range(len(self.st)):
            rank[self.pos[i]] = i
        self.rank = rank
        h = 0
        lcp = [None] * len(self.st)
        for i in range(len(self.st)):
            if rank[i] > 0:
                k = self.pos[rank[i] - 1]
                while ((i + h) < len(self.st) and
                       (k + h) < len(self.st) and
                       self.st[i + h] == self.st[k + h]):
                    h = h + 1
                lcp[rank[i]] = h
                if h > 0:
                    h = h - 1
        self.lcp = lcp
    def substr(self, beg, end=None):
        end = end or len(self.st)
        return self.st[beg] if beg==end else self.st[slice(beg, end)]
    def __repr__(self):
        return 'SuffixArray of %s: %s' % (self.st, self.pos)
    def show(self):
        return [self.st[i:] for i in self.pos]


def suffix_array_to_suffix_tree(sa):
    st = SuffixTree(sa.string)
    n = len(sa.string)
    make_suffix = lambda b, e: sa.st[slice(b, e)]
    add_node = lambda t, b, e: t.add_node(make_suffix(b, e))
    connect_node = lambda t, n, b, e: t.connect_node(n, make_suffix(b, e))
    current = add_node(st.root, sa.pos[0], n)
    for (ai, ai1, hi, hi1) in itertools.izip(sa.pos[:-1], sa.pos[1:],
                                             sa.lcp[:-1], sa.lcp[1:]):
        # guard against root case:  current.parent
        while current.distance > hi1:
            current = current.parent
        if current.distance == hi1:
            # case 1
            current = add_node(current, ai1 + hi1, n)
        else:
            # case 2
            # get rightmost node
            # and delete edge to it
            w = current.branches.pop()
            y = add_node(current, ai + current.distance, ai + hi1)
            connect_node(y, w, ai + hi1, ai + w.distance + 1)
            current = add_node(y, ai1 + hi1, n)
        # st.print_tree()
    return st


def leq(*args):
    if len(args) == 4:
        return leq_pair(*args)
    elif len(args) == 6:
        return leq_triple(*args)
    else:
        raise ValueError("Incorrect number of args, support 4 or 6")


def leq_pair(a1, a2, b1, b2):
    return (a1 < b1) or (a1 == b1) and (a2 <= b2)


def leq_triple(a1, a2, a3, b1, b2, b3):
    return (a1 < b1) or (a1 == b1) and leq_pair(a2, a3, b2, b3)


def radix_pass(arr, n, source, alpha):
    # counter array
    result = [0] * len(arr)
    counter = collections.Counter()
    for ind in arr[:n]:
        counter[source[ind]] += 1
    sum_ = 0
    for letter in alpha:
        freq, counter[letter] = counter[letter], sum_
        sum_ += freq
    for ind in arr[:n]:
        result[counter[source[ind]]] = ind
        counter[source[ind]] += 1
    return result


def sa_rec(source, n, alpha, SA):
    n0 = (n + 2)/3
    n1 = (n + 1)/3
    n2 = n/3
    n02 = n0 + n2
    # make suff12 divisible by 3
    suff12 = [i for i in xrange(n + n0 - n1) if i % 3 != 0]
    suff12.extend([0, 0, 0])
    SA12 = radix_pass(suff12, n02, source[2:], alpha)
    suff12 = radix_pass(SA12, n02, source[1:], alpha)
    SA12 = radix_pass(suff12, n02, source, alpha)
    # find lexicographic names of triples
    name = 0
    array_name = [0]
    (c0, c1, c2) = (-1, -1, -1)
    for pos in SA12[:n02]:
        if any([source[pos] != c0,
                source[pos + 1] != c1,
                source[pos + 2] != c2]):
            name += 1
            array_name.append(name)
            c0 = source[pos]
            c1 = source[pos + 1]
            c2 = source[pos + 2]
        # left half
        if pos % 3 == 1:
            suff12[pos/3] = name
        # right half
        else:
            suff12[pos/3 + n0] = name
    # recurse if names are not yet unique
    if name < n02:
        SA12 = sa_rec(suff12, n02, array_name, SA12)
        # store uniq names in suff12 using suffix array SA12
        for (i, pos) in enumerate(SA12[:n02]):
            suff12[pos] = i + 1
    else:
        # generate suffix array SA12 directly
        for (i, pos) in enumerate(suff12[:n02]):
            SA12[pos - 1] = i
    # stably sort the mod 0 suffixes from SA12 by their first character
    suff0 = [SA12[i] * 3 for i in xrange(n02) if SA12[i] < n0]
    SA0 = radix_pass(suff0, n0, source, alpha)
    # merge sorted SA0 suffixes and sorted SA12 suffixes
    get_i = lambda: (SA12[t] * 3 + 1 if SA12[t] < n0 else (SA12[t] - n0) * 3 + 2)
    p = 0
    k = 0
    t = n0 - n1
    while k < n:
        i = get_i()
        # pos of current offset SA12 suffix
        j = SA0[p] if p < n0 else 0 # pos of current offset SA0 suffix
        # different compares for mod 1 and mod 2 suffixes
        if (SA12[t] < n0):
            test = leq(source[i], suff12[SA12[t] + n0],
                       source[j], suff12[j/3])
        else:
            test = leq(source[i] ,source[i + 1], suff12[SA12[t] - n0 +1],
                       source[j], source[j + 1], suff12[j/3 + n0])
            # test = source[i] < source[j]
        if test:
            # suffix from SA12 is smaller
            SA[k] = i
            t += 1
            if t == n02:
                # done, only SA0 suffixes left
                k += 1
                while p < n0:
                    SA[k] = SA0[p]
                    p += 1
                    k += 1
        else:
            # suffix from SA0 is smaller
            SA[k] = j
            p += 1
            if p == n0:
                # done, only SA12 suffixes left
                k += 1
                while t < n02:
                    SA[k] = get_i()
                    t += 1
                    k += 1
        k += 1
    return SA[:-3]


def make_suffix_array(source):
    n = len(source)
    source += (unichr(1) * 3)
    alpha = sorted(set(source))
    SA = [0] * len(source)
    return sa_rec(source, n, alpha, SA)


def lrs(src):
    sa = SuffixArray(src)
    lrs = ""
    for (i, lcp) in enumerate(sa.lcp):
        if lcp is None:
            continue
        if lcp > len(lrs):
            lrs = sa.substr(sa.pos[i], sa.pos[i] + lcp)
    return lrs

def bin_search(arr, target, predicat):
    if not arr:
        return None
    ind = len(arr)/2
    item = arr[ind]
    if predicat(item, target):
        return (ind, item)
    else:
        if target > item:
            return bin_search(arr[ind:], target, predicat)
        else:
            return bin_search(arr[:ind], target, predicat)

def contains(src, pat):
    sa = SuffixArray(src)
    return bin_search(sa.show(), pat, lambda i, t: i.startswith(t)) is not None
