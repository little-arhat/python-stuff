
from __future__ import print_function

import sys
import math

from collections import Counter
from functools import partial
from itertools import starmap

# A Fast Voxel Traversal Algorithm for Ray Tracing (1987)
# by John Amanatides, Andrew Woo
# http://www.cse.chalmers.se/edu/year/2011/course/TDA361_Computer_Graphics/grid.pdf

GRID_SIZE = 800

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
    dirx = math.copysign(1, dx)
    diry = math.copysign(1, dy)
    dirz = math.copysign(1, dz)
    while True:
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
        if ((dirx * (cx - cx2) > 0) or
            (diry * (cy - cy2) > 0) or
            (dirz * (cz - cz2) > 0)):
            break
        else:
            f(cx, cy, cz)

def counter(result):
    def cnt(x,y,z):
        result[(x,y,z)] += 1
    return cnt

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: ./{} <filename>'.format(sys.argv[0]))
    else:
        box = Counter()
        trav = partial(grid_traverse, f=counter(box))
        with open(sys.argv[1]) as f:
            for line in f:
                trav(*(GRID_SIZE*float(c) for c in line.split(',')))
        print('Number of crossed voxels: {}'.format(len(box)))
        n = 10 if len(sys.argv) < 3 else int(sys.argv[2])
        for point, count in box.most_common(n):
            print('{} -- {}'.format(point, count))
