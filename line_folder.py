#!/usr/bin/env python

import re
import string
import itertools

def to_alf(seq):
    letters = iter(string.letters)
    symb_map = {}
    reverse_map = {}
    new_seq = []
    for el in seq:
        if el not in symb_map:
            let = letters.next()
            symb_map[el] = let
            reverse_map[let] = el
        # cannot use yield %(
        new_seq.append(symb_map[el])
    return (new_seq, reverse_map)

if __name__ == '__main__':
    with open('/Users/user/addrs.txt') as f:
        (new_seq, reverse_map) = to_alf(f)
    string_seq = ''.join(new_seq)
    print 'Found loops:'
    for m in re.findall(r'(.+?)\1+', string_seq):
        for s in m:
            print reverse_map[s],
        print

    new_seq = re.sub(r'((.+?)\2+)', "\\2", string_seq)
    with open('/Users/user/ol.txt', 'w') as f:
        f.writelines(reverse_map[symb] for symb in new_seq)
