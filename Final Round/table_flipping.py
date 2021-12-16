# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Final Round - Problem F. Table Flipping
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/F
#
# Time:  O(N * (logN)^2), TLE in both PyPy2 and Python2
# Space: O(NlogN)
#

from bisect import bisect_left
from itertools import izip
from functools import partial

# Template:
# https://github.com/kamyu104/FacebookHackerCup-2021/blob/main/Round%202/valet_parking_chapter_2.py
class SegmentTreeMaxRange(object):  # 0-based index
    def __init__(self, N,
                 build_fn=lambda x, y: [y]*(2*x),
                 query_fn=lambda x, y: y if x is None else max(x, y),
                 update_fn=lambda x, y: y if x is None else x+y,
                 default_val=0):
        self.base = N
        self.H = (N-1).bit_length()
        self.query_fn = query_fn
        self.update_fn = update_fn
        self.tree = build_fn(N, default_val)
        self.lazy = [None]*N
        for i in reversed(xrange(1, N)):
            self.tree[i] = query_fn(self.tree[2*i], self.tree[2*i+1])

    def __apply(self, x, val):
        self.tree[x] = self.update_fn(self.tree[x], val)
        if x < self.base:
            self.lazy[x] = self.update_fn(self.lazy[x], val)

    def update(self, L, R, h):  # Time: O(logN), Space: O(N)
        def pull(x):
            while x > 1:
                x //= 2
                self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2+1])
                if self.lazy[x] is not None:
                    self.tree[x] = self.update_fn(self.tree[x], self.lazy[x])

        if L > R:
            return
        L += self.base
        R += self.base
        L0, R0 = L, R
        while L <= R:
            if L & 1:  # is right child
                self.__apply(L, h)
                L += 1
            if R & 1 == 0:  # is left child
                self.__apply(R, h)
                R -= 1
            L //= 2
            R //= 2
        pull(L0)
        pull(R0)

    def query(self, L, R):  # Time: O(logN), Space: O(N)
        def push(x):
            n = 2**self.H
            while n != 1:
                y = x // n
                if self.lazy[y] is not None:
                    self.__apply(y*2, self.lazy[y])
                    self.__apply(y*2 + 1, self.lazy[y])
                    self.lazy[y] = None
                n //= 2

        result = None
        if L > R:
            return result

        L += self.base
        R += self.base
        push(L)
        push(R)
        while L <= R:
            if L & 1:  # is right child
                result = self.query_fn(result, self.tree[L])
                L += 1
            if R & 1 == 0:  # is left child
                result = self.query_fn(result, self.tree[R])
                R -= 1
            L //= 2
            R //= 2
        return result

# Template:
# https://github.com/kamyu104/FacebookHackerCup-2021/blob/main/Round%202/valet_parking_chapter_2.py
class SegmentTreeMax(object):  # 0-based index
    def __init__(self, N,
                 build_fn=lambda x, y: [y]*(2*x),
                 query_fn=lambda x, y: y if x is None else max(x, y),
                 update_fn=lambda x, y: y,
                 default_val=0):
        self.base = N
        self.query_fn = query_fn
        self.update_fn = update_fn
        self.tree = build_fn(N, default_val)
        for i in reversed(xrange(1, N)):
            self.tree[i] = query_fn(self.tree[2*i], self.tree[2*i+1])

    def update(self, i, h):  # Time: O(logN), Space: O(N)
        def apply(x, h):
            self.tree[x] = self.update_fn(self.tree[x], h)

        def pull(x):
            while x > 1:
                x //= 2
                self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2+1])

        apply(i+self.base, h)
        pull(i+self.base)

    def query(self, L, R):  # Time: O(logN), Space: O(N)
        result = None
        if L > R:
            return result

        L += self.base
        R += self.base
        while L <= R:
            if L & 1:  # is right child
                result = self.query_fn(result, self.tree[L])
                L += 1
            if R & 1 == 0:  # is left child
                result = self.query_fn(result, self.tree[R])
                R -= 1
            L //= 2
            R //= 2
        return result

# Template:
# https://github.com/kamyu104/FacebookHackerCup-2021/blob/main/Final%20Round/hire_flyers.py
class SegmentTree2D(object):  # 0-based index
    def __init__(self, N, build_leaf_fn, build_parent_fn, query_fn, update_fn, get_fn):
        self.tree = [None]*(2*N)
        self.base = N
        self.query_fn = query_fn
        self.update_fn = update_fn
        self.get_fn = get_fn
        for i in xrange(self.base, self.base+N):
            self.tree[i] = build_leaf_fn(i-self.base)
        for i in reversed(xrange(1, self.base)):
            self.tree[i] = build_parent_fn(self.tree[2*i], self.tree[2*i+1])

    def update(self, i, v, h):  # Time: O((logN)^2), Space: O(NlogN)
        x = self.base+i
        while x >= 1:
            self.update_fn(self.tree[x], v, h)
            x //= 2

    def query(self, L, R, v):  # Time: O((logN)^2), Space: O(NlogN)
        if L > R:
            return None
        L += self.base
        R += self.base 
        result  = None
        while L <= R:
            if L & 1:  # is right child
                result = self.query_fn(result, self.get_fn(self.tree[L], v))
                L += 1
            if R & 1 == 0:  # is left child
                result = self.query_fn(result, self.get_fn(self.tree[R], v))
                R -= 1
            L //= 2
            R //= 2
        return result

def update_A_rect(a, a_x0_y0, i, insert, st_x, st_y):
    st_x.update(a[X0], a_x0_y0[1], (a[Y1], i) if insert else None)
    st_x.update(a[X1], a_x0_y0[1], (a[Y1], i) if insert else None)
    st_y.update(a[Y0], a_x0_y0[0], (a[X1], i) if insert else None)
    st_y.update(a[Y1], a_x0_y0[0], (a[X1], i) if insert else None)

def get_A_rect_for_B_rect(b, st_x, st_y):
    p = st_x.query(b[X0], b[X1], b[Y1])
    if p and p[0] >= b[Y0]:
        return p[1]
    p = st_y.query(b[Y0], b[Y1], b[X1])
    if p and p[0] >= b[X0]:
        return p[1]
    return -1

def iter_dfs(A, B, A_x0_y0, i, lookup, st_x, st_y):
    if lookup[i]:
        return True
    stk = [[1, i]]
    while stk:
        step, u = stk.pop()
        if step == 1:
            lookup[u] = True
            stk.append((3, u))
            stk.append((2, u))
        elif step == 2:
            v = get_A_rect_for_B_rect(B[u], st_x, st_y)
            if v == -1:
                continue
            if lookup[v]:
                return False
            stk.append((2, u))
            stk.append((1, v))
        elif step == 3:
            update_A_rect(A[u], A_x0_y0[u], u, False, st_x, st_y)
    return True

def table_flipping():
    def build_leaf(keys, i):  # Total Time: O(NlogN), Total Space: O(N)
        keys = set(keys[i])
        return (sorted(keys), SegmentTreeMax(len(keys)))

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
        return (keys, SegmentTreeMax(len(keys)))

    def get(x, v):  # sum(cnt[x] for x in keys if x <= v), Time: O(logN)
        keys, st = x
        return st.query(0, bisect_left(keys, v+1)-1)

    def query(x, y):
        return y if x is None else max(x, y)

    def update(x, v, d):  # Time: O(logN)
        keys, st = x
        i = bisect_left(keys, v)
        st.update(i, d)

    N = input()
    A, B = [[None]*N for _ in xrange(2)]
    x_set, y_set = set(), set()
    for i in xrange(N):
        X, Y, W, H, D = raw_input().strip().split()
        X, Y, W, H = int(X), int(Y), int(W), int(H)
        A[i] = (X, Y, X+W, Y+H)
        if D == 'U':
            B[i] = (X, Y+H, X+W, (Y+H)+H)
        elif D == 'D':
            B[i] = (X, Y-H, X+W, (Y+H)-H)
        elif D == 'R':
            B[i] = (X+W, Y, (X+W)+W, Y+H)
        elif D == 'L':
            B[i] = (X-W, Y, (X+W)-W, Y+H)
        x_set.add((A[i][X0], i)), y_set.add((A[i][Y0], i)), x_set.add((A[i][X1], i)), y_set.add((A[i][Y1], i))
        x_set.add((B[i][X0], i)), y_set.add((B[i][Y0], i)), x_set.add((B[i][X1], i)), y_set.add((B[i][Y1], i))
    sorted_x = sorted(x_set)
    lower_x =[0]*len(sorted_x)
    for i in xrange(len(sorted_x)):
        lower_x[i] = i if i == 0 or sorted_x[i-1][0] != sorted_x[i][0] else lower_x[i-1]
    sorted_y = sorted(y_set)
    lower_y = [0]*len(sorted_y)
    for i in xrange(len(sorted_y)):
        lower_y[i] = i if i == 0 or sorted_y[i-1][0] != sorted_y[i][0] else lower_y[i-1]
    A_x0_y0 = [None]*N
    x_to_idx = {x:i for i, x in enumerate(sorted_x)}  # coordinate compression
    y_to_idx = {x:i for i, x in enumerate(sorted_y)}  # coordinate compression
    for i, ((a_x0, a_y0, a_x1, a_y1), (b_x0, b_y0, b_x1, b_y1)) in enumerate(izip(A, B)):
        A[i] = (x_to_idx[(a_x0, i)], y_to_idx[(a_y0, i)], x_to_idx[(a_x1, i)], y_to_idx[(a_y1, i)])
        B[i] = (x_to_idx[(b_x0, i)], y_to_idx[(b_y0, i)], x_to_idx[(b_x1, i)], y_to_idx[(b_y1, i)])
        # remember exact (unique) lower coordinates
        A_x0_y0[i] = (A[i][X0], A[i][Y0])
        # round coordinates up to value boundaries (with exclusive upper coordinates)
        A[i] = (lower_x[A[i][X0]], lower_y[A[i][Y0]], lower_x[A[i][X1]]-1, lower_y[A[i][Y1]]-1)
        B[i] = (lower_x[B[i][X0]], lower_y[B[i][Y0]], lower_x[B[i][X1]]-1, lower_y[B[i][Y1]]-1)
    # check for any overlap between final tables via line sweep
    events = []
    for x0, y0, x1, y1 in B:
        events.append((y0, 1, x0, x1))
        events.append((y1+1, -1, x0, x1))
    events.sort()
    st = SegmentTreeMaxRange(len(sorted_x))
    for _, v, l, r in events:
        st.update(l, r, v)
        if st.query(0, len(sorted_x)-1) > 1:
            return "NO"
    keys_x, keys_y = [[] for _ in xrange(len(sorted_x))], [[] for _ in xrange(len(sorted_y))]
    for i, ((x0, y0, x1, y1), (a_x0, a_y0)) in enumerate(izip(A, A_x0_y0)):
        keys_x[x0].append(a_y0)
        keys_x[x1].append(a_y0)
        keys_y[y0].append(a_x0)
        keys_y[y1].append(a_x0)
    st_x = SegmentTree2D(len(sorted_x), build_leaf_fn=partial(build_leaf, keys_x), build_parent_fn=build_parent, query_fn=query, update_fn=update, get_fn=get)
    st_y = SegmentTree2D(len(sorted_y), build_leaf_fn=partial(build_leaf, keys_y), build_parent_fn=build_parent, query_fn=query, update_fn=update, get_fn=get)
    for i in xrange(N):
        update_A_rect(A[i], A_x0_y0[i], i, True, st_x, st_y)
    lookup = [False]*N
    for i in xrange(N):
        if not iter_dfs(A, B, A_x0_y0, i, lookup, st_x, st_y):
            return "NO"  # cycle found
    return "YES"

X0, Y0, X1, Y1 = range(4)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, table_flipping())
