
def is_concat(d, s):
    for w in d:
        print("T={}; checking={}".format(s, w))
        if s.startswith(w):
            rest = s[len(w):]
            if not rest:
                return True
            n = is_concat(d, rest)
            if n:
                return True
    return False


def is_concat2(d, s):
    for w in d:
        print("T={}; checking={}".format(s, w))
        rest = None
        if s.startswith(w):
            rest = s[len(w):]
        elif s.endswith(w):
            rest = s[:-len(w)]
        if rest is not None:
            if not rest:
                return True
            n = is_concat2(d, rest)
            if n:
                return True
    return False


def is_concat_split(ds, s):
    l = len(s)
    for i in range(1, l+1):
        first, rest = s[:i], s[i:]
        print('memeing')
        if first in ds:
            if not rest:
                return True
            else:
                if is_concat_split(ds, rest):
                    return True
    return False

def is_concat2(d, s):
    return is_concat_split(set(d), s)


def is_concat_dp(ds, s):
    if not s:
        return False
    xl = len(s) + 1
    memo = [False for _ in range(xl)]
    for i in range(1, xl):
        print('i={}; si={}; memo={}'.format(i, s[:i], memo[i]))
        if (not memo[i]) and (s[:i] in ds):
            memo[i] = True
        if memo[i]:
            for j in range(i+1, xl):
                print('j={}; sj={}; memo={}'.format(j, s[i:i+j-1], memo[j]))
                if (not memo[j]) and (s[i:i+j-i] in ds):
                    memo[j] = True
                if (j == xl-1) and memo[j]:
                    return True
    return False

def is_concat(d, s):
    if not d:
        return False
    return is_concat_dp(set(d), s)
