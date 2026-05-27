
opening = '[{('
closing = ']})'
pairs = dict(zip(closing, opening))

def check(s):
    seen = []
    for c in s:
        if c in opening:
            seen.append(c)
        if c in closing:
            pair = pairs[c]
            if not seen:
                return False
            last = seen.pop()
            if pair != last:
                return False
    return (not bool(stack))
