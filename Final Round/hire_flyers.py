# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Final Round - Problem C. Hire Flyers
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/C
#
# Time:  O(N * (logN)^2), pass in PyPy2 but Python2
# Space: O(NlogN)
#

from collections import defaultdict
from bisect import bisect_left
from copy import deepcopy

# Template:
# https://github.com/kamyu104/GoogleKickStart-2021/blob/main/Round%20F/festival.py
class BIT(object):  # 0-indexed.
    def __init__(self, n):
        self.__bit = [0]*(n+1)  # Extra one for dummy node.

    def add(self, i, val):
        i += 1  # Extra one for dummy node.
        while i < len(self.__bit):
            self.__bit[i] += val
            i += (i & -i)

    def query(self, i):
        i += 1  # Extra one for dummy node.
        ret = 0
        while i > 0:
            ret += self.__bit[i]
            i -= (i & -i)
        return ret

# Template:
# https://github.com/kamyu104/FacebookHackerCup-2021/blob/main/Round%203/auth_ore_ization.py
class SegmentTree2D(object):  # 0-based index
    def __init__(self, N, build_leaf_fn, build_parent_fn, query_fn, update_fn, get_fn):  # modified
        self.tree = [None]*(2*N)
        self.base = N
        self.query_fn = query_fn
        self.update_fn = update_fn
        self.get_fn = get_fn  # modified
        for i in xrange(self.base, self.base+N):
            self.tree[i] = build_leaf_fn(i-self.base)  # modified
        for i in reversed(xrange(1, self.base)):
            self.tree[i] = build_parent_fn(self.tree[2*i], self.tree[2*i+1])  # modified

    def update(self, i, v, h):  # modified, Time: O((logN)^2), Space: O(NlogN)
        x = self.base+i
        while x >= 1:
            self.update_fn(self.tree[x], v, h)
            x //= 2

    def query(self, L, R, v):  # modified, Time: O((logN)^2), Space: O(NlogN)
        if L > R:
            return 0  # modified
        L += self.base
        R += self.base
        result  = None
        while L <= R:
            if L & 1:  # is right child
                result = self.query_fn(result, self.get_fn(self.tree[L], v))  # modified
                L += 1
            if R & 1 == 0:  # is left child
                result = self.query_fn(result, self.get_fn(self.tree[R], v))  # modified
                R -= 1
            L //= 2
            R //= 2
        return result

class Segment(object):
    def __init__(self, i, r, c, p, d, t=0):
        self.i = i  # agent's index
        self.r = r  # segment's initial row
        self.c = c  # segment's initial column
        self.p = p  # segment length
        self.d = d  # direction
        self.t = t  # turns taken by the agent before reaching the segment's initial row/column

    def get_time_val(self, N):
        return N * (self.t-self.r-self.c) + self.i

    def __cmp__(self, other):
        return cmp((self.r, self.c), (other.r, other.c))

def trim_segment(s, a, b, horizon):
    s = deepcopy(s)
    if s.d == R or s.d == D:           # forward segment
        sv1 = s.c if horizon else s.r  # first value
        sv2 = sv1+s.p-1                # last value
        t1 = max(a-sv1, 0)             # truncation at start
        t2 = max(sv2-b, 0)             # truncation at end
        if horizon:
            s.c += t1
        else:
            s.r += t1
        s.t += t1
        s.p -= t1+t2
    else:                              # backward segment
        sv2 = s.c if horizon else s.r  # last value
        sv1 = sv2-(s.p-1)              # first value
        t1 = max(a-sv1, 0)             # truncation at start
        t2 = max(sv2-b, 0)             # truncation at end
        if horizon:
            s.c -= t2
        else:
            s.r -= t2
        s.t += t2
        s.p -= t1 + t2
    return s

def merge_opposite_segements(s1, s2, horizon):
    nc = s2.c-s1.c+1 if horizon else s2.r-s1.r+1
    t1 = s1.t                                       # time for s1 to reach start
    t2 = s2.t+nc-1- int(s2.i < s1.i)                # time for s2 to reach start
    m = (s1.c if horizon else s1.r)+(t2-t1+2)//2-1  # last value painted over by s2
    return [trim_segment(s2, -INF, m, horizon), trim_segment(s1, m+1, INF, horizon)]

def process_linear_segments(segments, horizon, trimmed_segments):
    # collect and sort forward / backward segments
    d1, d2 = (R, L) if horizon else (D, U)
    P1 = [(s.r + s.c, -s.i, s) for s in segments if s.d == d1]
    P2 = [(-(s.r + s.c), -s.i, s) for s in segments if s.d != d1]
    P1.sort(), P2.sort()
    # reduce forward / backward segments independently
    S1, S2 = [], []
    last = -INF
    for _, _, s in P1:
        s = trim_segment(s, last+1, INF, horizon)  # trim to after last
        if s.p > 0:  # include if not obsolete
            S1.append(s)
        last = max(last, (s.c if horizon else s.r) + (s.p-1))
    last = INF
    for _, _, s in P2:
        s = trim_segment(s, -INF, last-1, horizon)  # trim to before last
        if s.p > 0:  # include if not obsolete
            S2.append(s)
        last = min(last, (s.c if horizon else s.r) - (s.p-1))
    # merge forward / backward segments
    events = []
    for i, s in enumerate(S1):
        sv = s.c if horizon else s.r
        events.append((sv, R, i))
        events.append((sv+s.p, U, i))
    for i, s in enumerate(S2):
        sv = s.c if horizon else s.r
        events.append((sv-(s.p-1), L, i))
        events.append((sv+1, D, i))
    events.sort()
    inds = [-1]*2
    for i, (v, e, s) in enumerate(events):
        # update set of ongoing segments
        inds[e//2] = s if e in (R, L) else -1
        # process ongoing segments?
        if i+1 < len(events) and v < events[i+1][0]:
            segments = []
            if inds[0] >= 0 and inds[1] >= 0:
                segments = merge_opposite_segements(S1[inds[0]], S2[inds[1]], horizon)
            elif inds[0] >= 0:
                segments = [S1[inds[0]]]
            elif inds[1] >= 0:
                segments = [S2[inds[1]]]
            for s in segments:
                s = trim_segment(s, v, events[i+1][0]-1, horizon)
                if s.p > 0:
                    trimmed_segments.append(s)

def hire_flyers():
    def build_leaf(i):  # Total Time: O(NlogN), Total Space: O(N)
        return (sorted(keys[i]), BIT(len(keys[i])))

    def build_parent(x, y):  # Total Time: O(NlogN), Total Space: O(NlogN)
        keys1, keys2 = (x[0] if x else []), (y[0] if y else [])
        i = j = 0
        keys = []
        while i < len(keys1) or j < len(keys2):
            if j == len(keys2) or (i < len(keys1) and keys1[i] < keys2[j]):
                keys.append(keys1[i])
                i += 1
            else:
                keys.append(keys2[j])
                j += 1
        return (keys, BIT(len(keys)))

    def get(x, v):  # sum(val[x] for x in keys if x >= v), Time: O(logN)
        keys, bit = x
        return bit.query(len(keys)-1) - bit.query(bisect_left(keys, v)-1)

    def query(x, y):
        return y if x is None else x+y

    def update(x, v, d):  # Time: O(logN)
        keys, bit = x
        bit.add(bisect_left(keys, v), d)

    N = input()
    row_segments, col_segments = defaultdict(list), defaultdict(list)
    for i in xrange(1, N+1):
        r, c, p, d =  raw_input().strip().split()
        r, c, p, d = int(r), int(c), int(p), DIRS[d]
        s = Segment(i, r, c, p, d)
        if s.d == R or s.d == L:
            row_segments[s.r].append(s)
        else:
            col_segments[s.c].append(s)
    # reduce each relevant row / column to disjoint segments
    trimmed_segments = []
    for segments in row_segments.itervalues():
        process_linear_segments(segments, True, trimmed_segments)
    for segments in col_segments.itervalues():
        process_linear_segments(segments, False, trimmed_segments)
    # compute base answer
    result = 0
    for s in trimmed_segments:
        result = (result + s.i*s.p) % MOD
    # consider 4 different rotations of the grid
    for r in xrange(4):
        # rotate everything 90 degrees clockwise
        for s in trimmed_segments:
            r, c, d = s.r, s.c, s.d
            s.r = c
            s.c = -r
            s.d = (d+1) % 4
        # consider 2 different vertical flips of the grid
        for _ in xrange(2):
            # Flip everything vertically
            for s in trimmed_segments:
                s.r = -s.r
                if s.d == U:
                    s.d = D
                elif s.d == D:
                    s.d = U
            # assemble list of line sweep events and distinct D segment columns
            events, col_segments = [], []
            for s in trimmed_segments:
                if s.d == R:
                    events.append((s.r, R, s))
                elif s.d == D:
                    events.append((s.r, U, s))
                    events.append((s.r+s.p-1, D, s))
                    col_segments.append(s.c)
            events.sort()
            col_segments = sorted(set(col_segments))
            # initialize 2D segment tree
            keys = [set() for _ in xrange(len(col_segments))]
            for s in trimmed_segments:
                if s.d == D:
                    keys[bisect_left(col_segments, s.c)].add(s.get_time_val(N))
            st = SegmentTree2D(len(col_segments), build_leaf_fn=build_leaf, build_parent_fn=build_parent, query_fn=query, update_fn=update, get_fn=get)
            # line sweep to subtract R segments covered by D ones
            for _, e, s in events:
                a = bisect_left(col_segments, s.c)
                v = s.get_time_val(N)
                if e == R:
                    b = bisect_left(col_segments, s.c+s.p)-1
                    result = (result - s.i*st.query(a, b, v)) % MOD
                else:
                    st.update(a, v, 1 if e == U else -1)
    return result

MOD = 10**9+7
INF = float("inf")
U, R, D, L = range(4)
DIRS = {'N':U, 'E':R, 'S':D, 'W':L}
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, hire_flyers())
