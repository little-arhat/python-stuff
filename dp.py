
# Given string "wwhhhwwwh" and int n, where "w" is working day and "h" is a
# holiday, find maximum consecutive holiday period you can take by booking n
# day off.

# This is a variantion of "longest sub-sequence with a sum" problem:
def cost(c):
    return 1 if c == 'w'  else 0

def max_vac_rec(calend, tot):
    def inner(seq, days, left):
        if not seq or left <= 0:
            return days
        excl = inner(seq[1:], days, left)
        incl = inner(seq[1:], days + 1, left - cost(seq[0]))
        return max(excl, incl)
    return inner(calend, 0, tot)

def max_vac(calend, holidays):
    s = 0
    longest = 0
    h = {}
    for (i, ch) in enumerate(calend):
        s += cost(ch)
        if s == holidays:
            longest = i + 1
        if s not in h:
            h[s] = i
        p = h.get(s - holidays)
        if p is not None:
            if longest < (i - p):
                longest = i - p
    return longest


# Given an array of integers, return a new array such that each element at
# index i of the new array is the product of all the numbers in the original
# array except the one at i.
# For example, if our input was [1, 2, 3, 4, 5],
# the expected output would be [120, 60, 40, 30, 24].
# If our input was [3, 2, 1], the expected output would be [2, 3, 6].
from functools import reduce
from operator import mul
prod = lambda seq: reduce(mul, seq, 1)
def prod_array(a):
    x = list(a)
    p = prod(x)
    return [int(p / i) for i in x]

def prod_array_no_div(a):
    x = list(a)
    r = [1] * len(x)
    for (i, el) in enumerate(x):
        for (k, sel) in enumerate(x):
            if i != k:
                r[i] *= sel
    return r

# Given a list of numbers and a number k,
# return whether any two numbers from the list add up to k.
# For example, given [10, 15, 3, 7] and k of 17,
# return true since 10 + 7 is 17.
# Bonus: Can you do this in one pass?
def add_up_multi(a, n):
    x = list(a)
    r = []
    for (i, el) in enumerate(x):
        for (k, d) in enumerate(x):
            r.append(el + d)
    return any(b == n for b in r)

def add_up_dp(a, n):
    x = list(a)
    r = dict()
    for (i, el) in enumerate(x):
        if (n - el) in r:
            return True
        r[el] = i
    return False

# ser/deser
# node = Node('root', Node('left', Node('left.left')), Node('right'))
# assert deserialize(serialize(node)).left.left.val == 'left.left'
class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    def __repr__(self):
        return 'Node("{}", {}, {})'.format(self.val, self.left, self.right)

def serialize(t):
    if t is None:
        return '()'
    return '({} {} {})'.format(t.val, serialize(t.left), serialize(t.right))

def tokenize(rr):
    return rr.replace('(', ' ( ').replace(')', ' ) ').split()

def read_tokens(ts):
    if not ts:
        raise ValueError('empty')
    el = ts.pop(0)
    if el == '(':
        args = []
        while ts[0] != ')':
            args.append(read_tokens(ts))
        ts.pop(0)
        if not args:
            return None
        (val, left, right) = args
        return Node(val, left, right)
    elif el == ')':
        raise ValueError(')')
    else:
        return el


def deserialize(rr):
    return read_tokens(tokenize(rr))


# cons(a, b) constructs a pair, and
# car(pair) and cdr(pair) returns the first and last
# element of that pair. For example, car(cons(3, 4))
# returns 3, and cdr(cons(3, 4)) returns 4.
# Given this implementation of cons:
def cons(a, b):
    def pair(f):
        return f(a, b)
    return pair
# Implement car and cdr.
def car(p):
    return p(lambda x, y: x)
def cdr(p):
    return p(lambda x, y: y)

# Given the mapping a = 1, b = 2, ... z = 26,
# and an encoded message, count the number of ways it
# can be decoded.
# For example, the message '111' would give 3,
# since it could be decoded as 'aaa', 'ka', and 'ak'.
# You can assume that the messages are decodable.
# For example, '001' is not allowed.
mp = {str(i - 96):chr(i) for i in range(97, 97 + 26)}
cases = [
    ('',          1),
    ('1',         1),
    ('11',        2),
    ('91',        1),
    ('19',        2),
    ('111',       3),
    ('1111',      5),
    ('1311',      4),
    ('11231489', 10),
]

def decodable_ways(n, mp):
    if not n:
        return 0
    h = [0] * (len(n) + 1)
    h[0] = 1
    for i in range(1, len(n) + 1):
        h[i] = h[i - 1]
        if i >= 2 and (n[i-2:i] in mp):
            h[i] += h[i - 2]
    return h[-1]


# cases
# A unival tree (which stands for "universal value")
# is a tree where all nodes under it have the same value.
# Given the root to a binary tree, count the number of
# unival subtrees.

cases = [
    (None,                                                          0),
    (Node(1),                                                       1),
    (Node(0, Node(1), Node(1)),                                     2),
    (Node(0, Node(0), Node(1)),                                     2),
    (Node(1, Node(1), Node(1)),                                     3),
    (Node(0, Node(1), Node(0, Node(1, Node(1), Node(1)), Node(0))), 5),
]

from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    val: int
    left: Optional[Node] = None
    right: Optional[Node] = None


def unival_count(g):
    if g is None:
        return 0
    v = True
    if g.left is not None:
        v &= g.val == g.left.val
    if g.right is not None:
        v &= g.val == g.right.val
    return int(v) + unival_count(g.left) + unival_count(g.right)


# Given a list of integers, write a function that returns
# the largest sum of non-adjacent numbers.
# Numbers can be 0 or negative.
# For example, [2, 4, 6, 2, 5] should return 13,
# since we pick 2, 6, and 5. [5, 1, 1, 5] should return 10,
# since we pick 5 and 5.

cases = [
    ([],                0),
    ([42],             42),
    ([27, 42],         42),
    ([5, 1, 1, 5],     10),
    ([2, 4, 6, 2, 5],  13),
    ([2, 4, 6, 2, -5], 8)
]

def non_adj_sum(a):
    def inner(seq, sofar, picked):
        if not seq:
            return sofar
        if picked:
            incl = 0
        else:
            incl = inner(seq[1:], sofar + seq[0],
                         True)
        excl = inner(seq[1:], sofar, False)
        return max(excl, incl)
    return inner(list(a), 0, False)

def non_adj_sum_dp(a):
    seq = list(a)
    minus1, prev, largest = 0, 0, 0
    for i in seq:
        print('>', 'pp', minus1, 'pr', prev, 'l', largest, ':', i)
        minus1, prev = prev, largest
        largest = max(prev, minus1 + i)
        print('<', 'pp', minus1, 'pr', prev, 'l', largest, ':', i)
    return largest

# Implement an autocomplete system.
# That is, given a query string s and a set of all
# possible query strings, return all strings in the set
# that have s as a prefix.
# For example, given the query string de and the set
# of strings [dog, deer, deal], return [deer, deal].

from collections import defaultdict
class Trie:
    def __init__(self):
        self.val = None
        self.children = defaultdict(Trie)
    def insert(self, word):
        cursor = self
        for l in word:
            cursor = cursor.children[l]
        cursor.val = word
    def __iter__(self):
        if self.val is not None:
            yield self.val
        for c in self.children.values():
            yield from c
    def find(self, prefix):
        cursor = self
        for l in prefix:
            if l not in cursor.children:
                return None
            cursor = cursor.children[l]
        return cursor

def build_trie(words):
    t = Trie()
    for word in words:
        t.insert(word)
    return t

class AutoC:
    def __init__(self, d):
        self.t = build_trie(d)
    def query(self, a):
        return self.t.find(a)
    def qlist(self, a):
        cc = self.query(a)
        if cc is None:
            return []
        else:
            return list(cc)


# There exists a staircase with N steps,
# and you can climb up either 1 or 2 steps at a time.
# Given N, write a function that returns the number of
# unique ways you can climb the staircase.
# The order of the steps matters.
# For example, if N is 4, then there are 5 unique ways:
# 1, 1, 1, 1
# 2, 1, 1
# 1, 2, 1
# 1, 1, 2
# 2, 2
# What if, instead of being able to climb 1 or 2 steps
# at a time, you could climb any number from a set of
# positive integers X?
# For example, if X = {1, 3, 5},
# you could climb 1, 3, or 5 steps at a time.
# NOTE: this is variation of "ATM/change problem" (order dependent!)

def steps_rec(height, steps={1, 2}):
    def inner(n, path):
        print('>', n, path)
        if n == 0:
            yield path
        for s in steps:
            if n - s >= 0:
                yield from inner(n - s, path + [s])
    paths = inner(height, [])
    return list(paths)

def steps_dp(height, steps={1, 2}):
    n = len(steps)
    nways = []
    for i in range(1, height + 1):
        for x in steps:
            if i - x >= 0:
                nways[i] += nways[i - x]
    return nways

# Given an integer k and a string s,
# find the length of the longest substring that contains
# at most k distinct characters.
# For example, given s = "abcba" and k = 2,
# the longest substring with k distinct characters is "bcb".

def longest_distinct_sub(s, k):
    def inner(rest, subs, current):
        print('>', 'r', rest, 's', subs, 'c', current)
        if not rest:
            return current
        ch = rest[0]
        if len(set(subs + ch)) > k:
            incl = 0
        else:
            incl = inner(rest[1:], subs + ch, current + 1)
        excl = inner(rest[1:], "", 0)
        print('<', 'i', incl, 'e', excl)
        return max(excl, incl)
    return inner(s, '', 0)

# LCS for input Sequences “ABCDGH” and “AEDFHR” is “ADH”
# LCS for input Sequences “AGGTAB” and “GXTXAYB” is “GTAB”
def lcs(x, y):
    def inner(a, b, c):
        if not a or not b:
            return (0, c)
        elif a[-1] == b[-1]:
            (n, b) = inner(a[:-1], b[:-1], c + b[-1])
            return (n + 1, b)
        else:
            (n1, b1) = inner(a, b[:-1], c)
            (n2, b2) = inner(a[:-1], b, c)
            if n1 > n2:
                return n1, b1
            else:
                return n2, b2
    return inner(x, y, '')


def lcs_dp(X, Y, d='', s=lambda a, b: a +b):
    # find the length of the strings
    m = len(X)
    n = len(Y)
    # declaring the array for storing the dp values
    L = [[None]*(n+1) for i in range(m+1)]
    T = [[None]*(n+1) for i in range(m+1)]
    """Following steps build L[m+1][n+1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
                T[i][j] = d
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1] + 1
                T[i][j] = s(T[i-1][j-1], Y[j-1])
            else:
                a = L[i-1][j]
                b = L[i][j-1]
                if a > b:
                    L[i][j] = a
                    T[i][j] = T[i-1][j]
                else:
                    L[i][j] = b
                    T[i][j] = T[i][j-1]
    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n], T[m][n]

from collections import namedtuple

def parse_fs(s):
    parts = s.split('\n')
    level = -1
    p = []
    b = []
    for part in parts:
        i = part.count('\t')
        cp = part.replace('\t', '')
        if '.' in part:
            b.append('/'.join(p) + '/' + cp)
        else:
            if i > level:
                p.append(cp)
            elif p:
                p.pop()
            level = i
    return b


# Given an array of integers and a number k,
# where 1 <= k <= length of the array,
# compute the maximum values of each subarray of length k.
# For example, given array = [10, 5, 2, 7, 8, 7]
# and k = 3, we should get: [10, 7, 8, 8], since:
# 10 = max(10, 5, 2)
# 7 = max(5, 2, 7)
# 8 = max(2, 7, 8)
# 8 = max(7, 8, 7)
# Do this in O(n) time and O(k) space.
# You can modify the input array in-place and
# you do not need to store the results.
# You can simply print them out as you compute them.

def max_each_suba(a, k):
    z = k - 1
    n = len(a) // k + z
    maxis = []
    for i in range(z, len(a)):
        maxis.append(max(a[i-z:i+1]))
    return maxis

def lis_dp(a):
    d = {}
    for (i, el) in enumerate(a):
        d[i] = (i, 1)
        for j in range(i):
            if (a[j] < a[i]) and (d[j][1] + 1 > d[i][1]):
                d[i] = (j, d[j][1] + 1)
    bestl = -1
    besti = -1
    for (k, (_p, v)) in d.items():
        if v > bestl:
            bestl = v
            besti = k
    b = [a[besti]]
    z = besti
    while (z in d):
        (pr, _) = d[z]
        if z == pr:
            break
        b.insert(0, a[pr])
        z = pr
    return b
