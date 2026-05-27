
import functools
from string import ascii_letters
from collections import Counter
from itertools import combinations

def interface(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    inner.is_interface = True
    return inner

class Obj(object):
    @interface
    def onClick(self, x):
        return true

print Obj().onClick.is_interface


def bwt(s):
    """Apply Burrows-Wheeler transform to input string."""
    assert "\0" not in s, "Input string cannot contain null character ('\\0')"
    s += "\0"  # Add end of file marker
    table = sorted(s[i:] + s[:i] for i in range(len(s)))  # Table of rotations of string
    last_column = [row[-1:] for row in table]  # Last characters of each row
    return "".join(last_column)  # Convert list of characters into string""

def ibwt(r):
    """Apply inverse Burrows-Wheeler transform."""
    table = [""] * len(r)  # Make empty table
    for i in range(len(r)):
        table = sorted(r[i] + table[i] for i in range(len(r)))  # Add a column of r
    s = [row for row in table if row.endswith("\0")][0]  # Find the correct row (ending in "\0")
    return s.rstrip("\0")  # Get rid of trailing null character""


import inspect, ast

def f(lol):
    return lol + 2

t = ast.parse(inspect.getsource(f))
print ast.dump(t)



from decimal import Decimal, getcontext
from operator import itemgetter

getcontext().prec = 3

# This could be table in SQL database with id, name, price columns
goods = {
    'biscuits': Decimal('1.29'),
    'juice': Decimal('0.53'),
    'microwave_meal': Decimal('3.50')
}

# Offers represent relationships between quantity and cost
offers = {
    'biscuits': [],
    'juice': [
        (3, goods['juice'] * 2), # 3 for the prices of 2
        (10, Decimal(5)) # 10 for the 5GBP
    ],
    'microwave_meal': [
        (2, Decimal(5))
    ]
}

def calculate_total(basket):
    discounted = 0
    total = 0
    stats = {}
    for (good, quantity) in basket.iteritems():
        # 1. calculate total sum w/o offers
        good_total = quantity * goods[good]
        # 2. calculate total sum w/ offers
        # sorted by count DESC list of offers
        good_offers = reversed(sorted(offers[good], key=itemgetter(0)))
        good_discounted = 0
        # apply as many offers as possible
        for (offer_quantity, offer_price) in good_offers:
            if not quantity:
                break
            (offer_applied, remainder) = divmod(quantity, offer_quantity)
            quantity = remainder
            # if offer wasn't apply this is no-op:
            good_discounted += offer_price * offer_applied
        # use regular price for remainded goods
        good_discounted += quantity * goods[good]
        discounted += good_discounted
        total += good_total
        stats[good] = (good_total, good_discounted)
    return (total, discounted, stats)

user_basket_1 = {
    'biscuits': 6,
    'juice': 4,
    'microwave_meal': 2
}

user_basket_2 = {
    'biscuits': 1,
    'juice': 11,
    'microwave_meal': 3
}

user_basket_3 = {
    'biscuits': 2,
    'juice': 1,
    'microwave_meal': 1
}


def bresenham_linie_3D(x1, y1, z1, x2, y2, z2):
#    x1, y1, z1, x2, y2, z2 = map(int, [x1, y1, z1, x2, y2, z2])
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    pixel = map(math.floor, [x1, y1, z1])
    x_inc = -1 if (dx < 0) else 1
    l = abs(dx)
    y_inc = -1 if (dy < 0) else  1
    m = abs(dy)
    z_inc = -1 if (dz < 0) else 1
    n = abs(dz)
    dx2 = l * 2
    dy2 = m * 2
    dz2 = n * 2
    if ((l >= m) and (l >= n)):
        err_1 = dy2 - l
        err_2 = dz2 - l
        for i in range(int(math.ceil(l))):
            print pixel
            if (err_1 > 0):
                pixel[1] = math.floor(pixel[1] + y_inc)
                err_1 -= dx2
            if (err_2 > 0):
                pixel[2] = math.floor(pixel[2] + z_inc)
                err_2 -= dx2
            err_1 += dy2
            err_2 += dz2
            pixel[0] = math.floor(pixel[0] + x_inc)
    elif ((m >= l) and (m >= n)):
        err_1 = dx2 - m
        err_2 = dz2 - m
        for i in range(int(math.ceil(m))):
            print pixel
            if err_1 > 0:
                pixel[0] = math.floor(pixel[0] + x_inc)
                err_1 -= dy2
            if (err_2 > 0):
                pixel[2] = math.floor(pixel[2] + z_inc)
                err_2 -= dy2
            err_1 += dx2
            err_2 += dz2
            pixel[1] = math.floor(pixel[1] + y_inc)
    else:
        err_1 = dy2 - n
        err_2 = dx2 - n
        for i in range(int(math.ceil(n))):
            print pixel
            if (err_1 > 0):
                pixel[1] = math.floor(pixel[1] + y_inc)
                err_1 -= dz2
            if (err_2 > 0):
                pixel[0] = math.floor(pixel[0] + x_inc)
                err_2 -= dz2
            err_1 += dy2
            err_2 += dx2
            pixel[2] = math.floor(pixel[2] + z_inc)
    print pixel




def grid_traverse(x1, y1, z1, x2, y2, z2, f=print):
    frac = lambda x:math.modf(x)[0]
    def to_cell(x, y, z):
        return (math.floor(x), math.floor(y), math.floor(z))
    def init_step(ct, t1, t2):
        v = t2 - t1
        if v == 0:
            return 0, float('Inf'), float('Inf')
        dx = abs(1.0 / v)
        t = dx * (1.0 - frac(t1 / 1.0))
        return math.copysign(1, v), math.copysign(dx, v), t
    cx1, cy1, cz1 = to_cell(x1, y1, z1)
    cx2, cy2, cz2 = to_cell(x2, y2, z2)
    stepX, dx, tx = init_step(cx1, x1, x2)
    stepY, dy, ty = init_step(cy1, y1, y2)
    stepZ, dz, tz = init_step(cz1, z1, z2)
    cx, cy, cz = cx1, cy1, cz1
    f(cx, cy, cz)
    while abs(cx - cx2) > 1 or abs(cy - cy2) > 1 or abs(cz - cz2) > 1:
        if tx == ty == tz:
            tx, cx = tx + dx, cx + stepX
            ty, cy = ty + dy, cy + stepY
            tz, cz = tz + dz, cz + stepZ
        elif tx < ty:
            if tx == tz:
                tx, cx = tx + dx, cx + stepX
                tz, cz = tz + dz, cz + stepZ
            elif tx < tz:
                tx, cx = tx + dx, cx + stepX
            else:
                tz, cz = tz + dz, cz + stepZ
        else:
            if ty == tz:
                ty, cy = ty + dy, cy + stepY
                tz, cz = tz + dz, cz + stepZ
            elif ty < tz:
                ty, cy = ty + dy, cy + stepY
            else:
                tz, cz = tz + dz, cz + stepZ
        f(cx, cy, cz)
    if cx != cx2 or cy != cy2 or cz != cz2:
        f(cx2, cy2, cz2)



def find_eq_min(a, b):
    a = iter(a)
    b = iter(b)
    cand = None
    curr = None
    m = None
    oth = None
    na = None
    nb = None
    while True:
        if curr is None:
            na = next(a, None)
            nb = next(b, None)
            if na is None or nb is None:
                return cand
            if na == nb:
                cand = na
            else:
                curr = a if na > nb else b
                m = min(na, nb)
                oth = b if na > nb else a
        else:
            nc = next(curr, None)
            if nc is None:
                return cand
            if nc == m:
                cand = m
                curr = None
            else:
                t = curr
                curr = curr if nc > m else oth
                oth = oth if nc > m else t
                m = min(nc, m)



def planar(d, silent=False):
    # python
    x = list(d)
    c = len(x)
    first_g = -1
    for_b = c - 1
    spaces = ' ' * (4 + c)
    def pl(i, b, g):
        s = list(spaces)
        s[3 + i] = '^'
        s[3 + b] = '*'
        if g > -1:
            if g == i:
                s[3 + g] = 'A'
            else:
                s[3 + g] = '_'
        print ''.join(s)
    for i in range(c):
        if not silent:
            print '>>', ''.join(x)
            pl(i, for_b, first_g)
        if x[i] == 'B':
            while x[for_b] == 'B' and for_b > i :
                for_b -= 1
            # guard
            if for_b == i:
                return ''.join(x)
            t = x[for_b]
            x[for_b] = x[i]
            x[i] = t
        if x[i] == 'G':
            # first occ
            if first_g < 0:
                first_g = i
        if x[i] == 'R':
            if first_g > -1:
                t = x[first_g]
                x[first_g] = x[i]
                x[i] = t
                first_g += 1
        if not silent:
            print '||', ''.join(x)
            pl(i, for_b, first_g)
    return ''.join(x)

def control(s):
    return ''.join(reversed(sorted(s)))

def test(N):
    for i in range(N):
        t = ''.join(random.choice('RGB') for _ in range(random.randint(6, 100)))
        if planar(t, True) != control(t):
            print 'FUCK:', t
            return
    print 'ALL OK AFTER', N, 'ITERATIONS'


# def see_as_many_trees_as_possible(trees, angle_func):
#     angles = map(angle_func, trees)
#     sorted_angles = sorted(angles)
#     # [0, 10, 12, 33, 66, 130, 230, 300, 350]
#     viewpoints = {}
#     limit = 45
#     for angle in sorted_angles:
#         viewpoints[angle] = 1
#         for other_tree in sorted_angles():
#             if ((other_tree - angle) % 360) < limit:
#                 viewpoints[angle] += 1
#             else:
#                 break
#     s = sorted(viewpoints.items(), cmp=lambda (_k1, t1), (_k2, t2): cmp(t1, t2)
#     return next(s) # get first

def best(trees):
    trees = list(sorted(trees))
    trees.extend(360 + t for t in trees if t < 45) # make "circle"
    best_sight = []
    sight = []
    n = 0
    for tree in trees:
        n += 1
        sight.append(tree)
        while tree - sight[0] > 45:
            n += 1
            sight = sight[1:] # shift
        if len(sight) > len(best_sight):
            best_sight = list(sight) # avoid funny stuff
    return n, [t % 360 for t in best_sight]


def find_consec(s):
    target = None
    prev = None
    current = 0
    count = 0
    for char in s:
        if prev == char:
            current += 1
        else:
            if current > count:
                target = prev
                count = current
            prev = char
            current = 1
    return (target, count)




a = [1,2,4,5,7,29,30]
prices = {7:7, 1:2}

def find_prices(a):
    variants = [{valid_till: None, price:0}]
    last_var = 0
    for day in a:
        var = variants[last_var]
        if last_var['valid_till'] is None or last_var['valid_till'] < day:
            for (valid, price) in prices.items():



def find_last_valid(days, curday, valid):
    day_i = days.index(curday)
    last_valid = curday
    for day in days[day_i:]:
        if day - curday < valid:
            last_valid = day
        else:
            break
    return last_valid

def find_next_step(days, curday):
    day_i = days.index(curday)
    if len(days) -1 == day_i:
        return None
    else:
        return days[day_i + 1]

prices = {7:7, 30:25}
def build_graph(days):
    g = {}
    for day in days:
        g[day] = {}
        for (valid,price) in prices.items():
            last_val = find_last_valid(days, day, valid)
            g[day][last_val] = price
        next_step = find_next_step(days, day)
        if next_step is not None:
            g[day][next_step] = 2
    return g

ga = {
    '1': {'30': 25, '2': 2, '7':7},
    '2': {'30': 25, '4': 2, '7':7},
    '4': {'30': 25, '5': 2, '7':7},
    '5': {'30': 25, '7': 2},
    '7': {'30': 25, '29':2},
    '29':{'30':2},
    '30':{}
    }


a = [5,4,-3,2,0, 1,-1,0,2,-3,4,-5]

def alternating(it):
    was_match = False
    for (p, p1, p2) in zip(it[:-2], it[1:-1], it[2:]):
        if (p >= 0) and (p1 <= 0) and (p2 >= 0):
            was_match = True
            yield p
        elif (p <= 0) and (p1 >= 0) and (p2 <= 0):
            was_match = True
            yield p
        else:
                yield p

                yield p1
            break

def results(a):
    for (i, _) in enumerate(a):
        yield list(alternating(a[i:]))

def dist(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

from __future__ import print_function

def getLockerDistanceGrid( cityLength,  cityWidth,  lockerXCoordinates,  lockerYCoordinates):
    result = [[0] * cityWidth for _ in range(1, cityLength + 1)]
    coords = zip(lockerXCoordinates, lockerYCoordinates)
    for y in range(1, cityWidth + 1):
        for x in range(1, cityLength + 1):
            p = (x, y)
            d = map(lambda l: dist(p, l), coords)
            closest = min(d)
            result[x-1][y-1] = closest
    return result

for pack in x:
    for course in pack:
        c[course] += 1


def fizzBuzz(n):
    res = []
    for i in xrange(1, n+1):
        m3, m5 = i % 3, i % 5
        if (not m3) and (not m5):
            res.append("FizzBuzz")
        elif (not m3) and m5:
            res.append("Fizz")
        elif not m5:
            res.append("Buzz")
        else:
            res.append(str(i))
    return res

def change_direction(dx, dy):
    # not allowed!
    if abs(dx+dy) != 1:
        raise ValueError
    if dy == 0:
        return dy, dx
    if dx == 0:
        return -dy, dx

def print_spiral(matrix):
    M = len(matrix)
    if M:
        N = len(matrix[0])
        if not N:
            return
    else:
        return
    dx, dy = 1, 0   # direction
    x, y = 0, 0     # coordinate
    start = 0       # initial value for the matrix
    left_bound, right_bound = 0, N-1
    upper_bound, bottom_bound = 1, M-1
    # zero filled 2d array
    for not_use in range(N*M):
        print matrix[y][x],
        if (dx > 0 and x >= right_bound):
            dx, dy = change_direction(dx, dy)
            right_bound -= 1
        if (dx < 0 and x <= left_bound):
            dx, dy = change_direction(dx, dy)
            left_bound += 1
        if (dy > 0 and y >= bottom_bound):
            dx, dy = change_direction(dx, dy)
            bottom_bound -= 1
        if (dy < 0 and y <= upper_bound):
            dx, dy = change_direction(dx, dy)
            upper_bound += 1
        x += dx
        y += dy

a = [1,0,3,9,2]
def max_nona_sum(a):
    m = 0
    for (i, el) in enumerate(a):
        sums = [el] + [el + k for k in a[i+2:]]
        if sums:
            ms = max(sums)
            if ms > m:
                m = ms
    return m

def max_nona_rec(a):
    def iterx(a):
        rest = a[2:]
        if rest:
            return [a[0] + k for k in rest] + iterx(a[1:])
        else:
            return []
    return max(iterx(a))


def max_nona_seq(a):
    incl = 0
    excl = 0
    for el in a:
        tmp = incl
        incl = max(excl + el, incl)
        excl = tmp
    return max(incl, excl)

def max_non_dp(a):
    def iterx(i):
        if i < 0:
            return 0
        elif i == 0:
            return a[0]
        else:
            return max(iterx(i - 1), iterx(i - 2) + a[i])
    return iterx(len(a) - 1)

def paly(s):
    i = 0
    k = len(s) - 1
    while i < k:
        if s[i] != s[k]:
            return False
        i += 1
        k -= 1
    return s[k] == s[i]


# bool minWindow(const char* S, const char *T,
#                int &minWindowBegin, int &minWindowEnd) {
#   int sLen = strlen(S);
#   int tLen = strlen(T);
#   int needToFind[256] = {0};

#   for (int i = 0; i < tLen; i++)
#     needToFind[T[i]]++;

#   int hasFound[256] = {0};
#   int minWindowLen = INT_MAX;
#   int count = 0;
#   for (int begin = 0, end = 0; end < sLen; end++) {
#     // skip characters not in T
#     if (needToFind[S[end]] == 0) continue;
#     hasFound[S[end]]++;
#     if (hasFound[S[end]] <= needToFind[S[end]])
#       count++;

#     // if window constraint is satisfied
#     if (count == tLen) {
#       // advance begin index as far right as possible,
#       // stop when advancing breaks window constraint.
#       while (needToFind[S[begin]] == 0 ||
#             hasFound[S[begin]] > needToFind[S[begin]]) {
#         if (hasFound[S[begin]] > needToFind[S[begin]])
#           hasFound[S[begin]]--;
#         begin++;
#       }

#       // update minWindow if a minimum length is met
#       int windowLen = end - begin + 1;
#       if (windowLen < minWindowLen) {
#         minWindowBegin = begin;
#         minWindowEnd = end;
#         minWindowLen = windowLen;
#       } // end if
#     } // end if
#   } // end for

#   return (count == tLen) ? true : false;
# }

def smallest_sub(s, t):
    from collections import defaultdict
    from sys import maxint
    sl = len(s)
    tl = len(t)
    need_to_find = defaultdict(int)
    for char in t:
        need_to_find[char] += 1
    has_found = defaultdict(int)
    min_len = maxint
    count = 0
    begin = 0
    min_window_begin = 0
    min_window_end = 0
    for (end, char) in enumerate(s):
        if char not in need_to_find:
            continue
        has_found[char] += 1
        if has_found[char] <= need_to_find[char]:
            count += 1
        if count == tl:
            while ((need_to_find[s[begin]] == 0) or
                   (has_found[s[begin]] > need_to_find[s[begin]])):
                if (has_found[s[begin]] > need_to_find[s[begin]]):
                    has_found[s[begin]] -= 1;
                begin += 1
            window_len = end - begin + 1
            if window_len < min_len:
                min_len = window_len
                min_window_begin = begin
                min_window_end = end
    if count == tl:
        return (min_len, s[min_window_begin:min_window_end+1])
    else:
        return None

def show_grid(rows, cols, pos):
    (i, k) = pos
    s = [['0'] * cols for _ in range(rows)]
    s[i][k] = '*'
    return '\n'.join(''.join(r) for r in s)

def min_sum_path(grid):
    if not grid or not grid[0]:
        return 0
    from collections import defaultdict
    m = len(grid)
    n = len(grid[0])
    dp = [[0 for i in range(n)] for k in range(m)]
    dp[0][0] = grid[0][0]
    for i in range(1, n):
        dp[0][i] = dp[0][i-1] + grid[0][i]
    for i in range(1, m):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    for i in range(1, m):
        for j in range(1, n):
            # print show_grid(m, n, (i, j))
            # print
            if dp[i-1][j] > dp[i][j-1]:
                dp[i][j] = dp[i][j-1] + grid[i][j]
            else:
                dp[i][j] = dp[i-1][j] + grid[i][j]
    return (dp[m-1][n-1], dp)

def product(seq):
    p = 1
    for i in seq:
        p = p * i
    return p

def fact(f, to):
    return product(range(f+1, to+1))

def choose(n, k):
    return fact(1, n)/(fact(1, n-k) * fact(1, k))

def unique_path(m, n):
    # m + n - 2 -- number of cells we need to pass
    # 2 -- number of possible moves (down, right), so 0 1
    # 2**n -- number of all possible paths
    # m - 1 -- number of right moves
    # n - 1 -- number of left moves
    # number of interesting paths == number of paths among 2**n with 0s = (n-1)
    #  and 1s = (m-1)
    # or C n by k (choose n k)
    return choose(m + n - 2, m - 1)

class FlatBiTree:
    def __init__(self):
        self.level = 0
        self.count = 0
        self.data = [None]
    def insert(self, value):
        k = 0
        d = self.data
        try:
            while True:
                pointed = d[k]
                if pointed is None:
                    d[k] = value
                    self.count += 1
                    break
                elif value < pointed:
                    k = 2*k + 1
                else:
                    k = 2*k + 2
        except IndexError:
            self.level += 1
            d.extend([None] * (2**self.level))
            d[k] = value
            self.count += 1
    def mem(self, value):
        k = 0
        d = self.data
        try:
            while True:
                pointed = d[k]
                if pointed is None:
                    return False
                elif value == pointed:
                    return True
                elif value < pointed:
                    k = 2*k + 1
                else:
                    k = 2*k + 2
        except IndexError:
            return False


def change(target, coins):
    lc = len(coins)
    table = [None]*(target+1)
    table[0] = [None]
    for i in range(1, target+1):
        for (j, c) in enumerate(coins):
            if c <= i:
                sub_res = table[i-c]
                if (sub_res and
                    ((table[i] is None) or
                     ((len(sub_res) + 1) < len(table[i])))):
                    if sub_res == [None]:
                        table[i] = [c]
                    else:
                        table[i] = sub_res + [c]
    return table[-1]


def mybin(n):
    d = [0] * 30
    l = 0
    while (n > 0):
        d[l] = n % 2
        n //= 2
        l += 1
    return d, l

def solution(n):
    d = [0] * 30
    l = 0
    while (n > 0):
        d[l] = n % 2
        n //= 2
        l += 1
    for p in range(1, 1 + l):
        if p > l / 2:
            continue
        ok = True
        for i in xrange(l - p):
            if d[i] != d[i + p]:
                ok = False
                break
        if ok:
            return p
    return -1


def solution(a):
    x = sorted(enumerate(a), key=lambda (i, v): v)
    last_seen = None
    last_i = None
    for ((i1, v1), (i2, v2)) in zip(x[:-1], x[1:]):
        print('Lolka', i1, v1, i2, v2)
        if last_seen is None:
            last_seen = v1
            last_i = i1
        if v1 == v2:
            print (last_i, i2)
        else:
            last_seen = v2
            last_i = i2

def solution2(a):
    d = {}
    for (i,v) in enumerate(a):
        if v not in d:
            d[v] = [i]
        else:
            d[v].append(i)
    res = []
    for ix in d.itervalues():
        if len(ix) < 2:
            continue
        for (k, bi) in enumerate(ix):
            for bb in ix[k+1:]:
                res.append((bi, bb))
    return len(res)

def solution(a):
    d = {}
    for v in a:
        if v not in d:
            d[v] = (0, 0)
        else:
            (s, c) = d[v]
            new_c = c + 1
            new_s = s + new_c
            d[v] = (new_s, new_c)
    c = 0
    for (s, _) in d.itervalues():
        c += s
    return c

from collections import defaultdict
def nik_sol(a):
    def sum_range_before_n(n):
        n -= 1
        return n * (n + 1) // 2
    d = defaultdict(int)
    for i in a:
        d[i] += 1
    return sum(map(sum_range_before_n, d.values()))


class MinStack2:
   def __init__(self):
      self.data = []
      self.prev_min = {}
      self.current_min = float("inf")
   def push(self, el):
      self.data.insert(0, el)
      if el < self.current_min:
          prev = self.current_min
          self.current_min = el
          self.prev_min[el] = prev
   def pop(self):
       (head, *tail) = self.data
       self.data = tail
       if head == self.current_min and head in self.prev_min:
           self.current_min = self.prev_min[head]
           del self.prev_min[head]
       return head
   def peekmin(self):
       return self.current_min

import random
import statistics

def sample_stat(sampled):
    diffs = [(y-x) for (x, y) in zip(sampled[:-1], sampled[1:])]
    avg = sum(diffs) / (1.0 * len(diffs))
    return {'max': max(diffs),
            'median': statistics.median(diffs),
            'avg': avg}

def test_percentage(fn, percentage, seqs):
    for seq in seqs:
        c = len(seq)
        expected = (percentage/100.) * c
        sampled = list(fn(seq, percentage))
        got = len(sampled)
        stat = sample_stat(sampled)
        sqd = abs(got-expected)
        print(f'{percentage}% => got {got}, expected: {expected}, diff: {sqd}; stat: {stat}')

def test_one(fn, seqs):
    for n in (5, 10, 20, 25, 40, 50, 60, 75, 90):
        test_percentage(fn, n, seqs)

def gen_seqs(n, k, p):
    for i in range(n):
        yield list(range(random.randint(k, p)))

def test_sampling(sample_funcs):
    seqs = list(gen_seqs(10, 110, 160))
    for (name, func) in sample_funcs.items():
        print()
        print(f'Testing {name}...')
        test_one(func, seqs)

def sample_stream(it, percentage):
    if percentage <= 10:
        take_nth = 100 // percentage
        skip = lambda i: bool(i % take_nth)
    else:
        take_first_n = percentage // 10
        skip = lambda i: (i % 10) >= take_first_n
    for (i, el) in enumerate(it):
        if skip(i):
            continue
        else:
            yield el

def sample_random(it, percentage):
    n = percentage / 100.
    for el in it:
        if random.random() < n:
            yield el

def reservoir(k, seq):
    res = [seq[i] for i in range(k)]
    for (i, y) in enumerate(seq[k:]):
        j = random.randint(1, i + k)
        if j < k:
            res[j] = y
    return list(sorted(res))

def reservoir_indices(k):
    res = [i for i in range(k)]
    for i in range(k, 100):
        j = random.randint(1, i + k)
        if j < k:
            res[j] = i
    return set(res)

def reservoir_stream(it, percentage):
    indices = reservoir_indices(percentage)
    for (i, el) in enumerate(it):
        ii = i % 100
        if ii in indices:
            yield el



def lamps(n):
    lamps = {x:False for x in range(1, n+1)}
    players = list(range(1, n+1))
    for p in players:
        for l in lamps:
            if l%p == 0:
                lamps[l] = not lamps[l]
    return sorted([l for (l, s) in lamps.items() if s])

def f2(n, denom):
    ans = 10**10
    if n<=0:
        return 0
    for i in denom:
        if n-i>=0:
            ans = min(ans, 1+f2(n-i, denom))
            print(n, i, ans)
    return ans


def f(n, denom):
    ans = None
    if n<=0:
        return []
    for i in denom:
        if n-i>=0:
            d = f(n-i, denom)
            if d is None:
                continue
            r = [i] + d
            if ans is not None and len(ans) < len(r):
                ans = ans
            else:
                ans = r
    return ans


def calend(s):
    from functools import reduce
    def inner(acc, el):
        if el == acc['l']:
            acc['c'] += 1
        else:
            acc['c'] = 1
        acc['l'] = el
        acc['m'] = max(acc['m'], acc['c'])
        return acc
    return reduce(inner, s, {'m': 0, 'c':1, 'l':''})['m']


def max_vac_rec(calend, tot):
    def cost(c):
        return 1 if c == 'w'  else 0
    def inner(seq, days, left):
        if not seq or left <= 0:
            return days
        excl = inner(seq[1:], days, left)
        incl = inner(seq[1:], days + 1, left - cost(seq[0]))
        return max(excl, incl)
    return inner(calend, 0, tot)

def max_vac(calend, tot):
    def cost(c):
        return 1 if c == 'w'  else 0
    s = 0
    ln = 0
    h = {}
    for (i, ch) in enumerate(calend):
        s += cost(ch)
        if s == tot:
            ln = i + 1
        if s not in h:
            h[s] = i
            p = h.get(s - tot)
        if p is not None:
            if ln < (i - p):
                ln = i - p
    return ln


import random
def bochkas(l, n):
    rest = l
    b = []
    for e in range(n):
        fill = random.random() * rest
        b.append(fill)
        rest = rest - fill
    return b

def game(a, b, c):
    d = dict(locals())
    r = random.random()
    c = {k:(abs(v - r)) for (k, v) in d.items()}
    m = min(c.values())
    w = [k for (k, v) in c.items() if v==m]
    return w[0]

def run(a, b, c, n):
    for _ in range(n):
        yield(game(a, b, c))

def cnt(seq):
    c = Counter()
    for b in seq:
        c[b] += 1
    return c

def abc(*choices):
    return {l:c for (l, c) in zip(ascii_letters, choices)}

def inv(d):
    return {v:k for (k, v) in d.items()}

def m(pb):
    return max(pb.values())

def probs(choices):
    d = dict(choices)
    idd = inv(d)
    r = {k:0 for k in d}
    s = list(sorted(set([0, 1] + list(idd))))
    for (p, n) in zip(s[:-1], s[1:]):
        if p not in idd and n in idd:
            player = idd[n]
            r[player] += n - p
        elif p in idd and n not in idd:
            player = idd[p]
            r[player] += n - p
        else:
            p1 = idd[n]
            p2 = idd[p]
            r[p1] += (n - p) / 2.
            r[p2] += (n - p) / 2.
    return r

def bins01(n_bins):
    per_bin = 1. / n_bins
    s = 0
    for i in range(n_bins):
        s = i * per_bin
        yield s
    yield 1.0

def simulate_game(n_players, n_bins=100):
    per_bin = 1. / n_bins
    gb = list(bins01(n_bins))
    start = 0
    best_val = 1
    best_comb = None
    for players_choices in combinations(gb, n_players):
        bb = abc(*players_choices)
        win_probs = probs(bb)
        metric = m(win_probs)
        if best_comb is None or metric < best_val:
            best_val = metric
            best_comb = bb
    return (best_comb, best_val)
