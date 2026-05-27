
def get_string(l, i):
    try:
        return l[i]
    except IndexError:
        return None

def has_string(l, s):
    i = 0
    left = 0
    right = None
    while True:
        maybe_string = get_string(l, i)
        if (maybe_string is None) or (maybe_string > s):
            right = i
            ni = (i - left) + 1
            if i <= left or i == ni : # 2 <= 4
                return False
            else:
                i = ni
        elif maybe_string == s:
            return True
        elif maybe_string < s:
            left = i
            if i == 0:
                i += 1
            elif right is not None:
                ni = i + (right - left) / 2
                if i >= right or i == ni:
                    return False
                else:
                    i = ni
            else:
                i = i * 2
