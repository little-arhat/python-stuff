
def pairs(a, k):
    d = dict((x, i) for (i, x) in enumerate(a))
    c = 0
    for (i, n) in enumerate(a):
        need = k - i
        index = d.get(need, None)
        if index and index != i:
            c += 1
            del d[need]
            if n in d:
                del d[n]
    return c


def with_sort(a, k):
    # essentially the same quadro compl.
    s = sorted(a, reverse=True)
    maybe = set()
    c = 0
    for i in s:
        if i > k:
            continue
        else:
            complement = next(filter(lambda m: m+i == k, maybe), None)
            if complement:
                c += 1
                maybe.remove(complement)
                continue
            if i >= k//2:
                maybe.add(i)
    return c

for i in range(10000):
    k = random.randint(0, 5*(10**9))
    n = random.randint(1, 5*(10**5))
    l = [random.randint(0, 10**9) for _ in range(n)]
    p, s = pairs(l, k), with_sort(l, k)
    if p != s:
        print(l)
        print(k)
        break
