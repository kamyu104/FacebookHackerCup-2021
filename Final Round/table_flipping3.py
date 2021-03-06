# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Final Round - Problem F. Table Flipping
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/F
#
# Time:  O(NlogN), pass in PyPy2 but Python2
# Space: O(NlogN)
#

from itertools import izip

class Node(object):
    def __init__(self, l=-1, r=-1):
        self.l = l
        self.r = r

def has_no_cycle(adj):
    in_degree = [0]*len(adj)
    for u in xrange(len(adj)):
        for v in adj[u]:
            in_degree[v] += 1
    q = [u for u, x in enumerate(in_degree) if not x]
    while q:
        new_q = []
        for u in q:
            for v in adj[u]:
                in_degree[v] -= 1
                if not in_degree[v]:
                    new_q.append(v)
        q = new_q
    return all(x == 0 for x in in_degree)

def table_flipping():
    def add_edge(u, v):
        if u == -1 or v == -1:
            return
        adj[u].append(v)

    def update(k, v, L, R, l, r, x):
        if r <= L or l >= R:
            return v
        u = len(tree)
        tree.append(Node())
        adj.append([])
        node = tree[-1]
        if L <= l <= r <= R:
            if x == -1:
                return -1
            if v != -1:
                has_no_overlap[0] = False
            if k == 0:
                add_edge(u, x)
            else:
                add_edge(x, u)
            return u
        if v != -1 and tree[v].l == tree[v].r == -1 and x != -1:
            has_no_overlap[0] = False
        mid = l+(r-l)//2
        node.l = update(k, tree[v].l if v != -1 else -1, L, R, l, mid, x)
        node.r = update(k, tree[v].r if v != -1 else -1, L, R, mid, r, x)
        if node.l == node.r == -1:
            return -1
        if k == 0:
            add_edge(u, node.l)
            add_edge(u, node.r)
        else:
            add_edge(node.l, u)
            add_edge(node.r, u)
        return u

    def add_edges(k, v, L, R, l, r, x):
        if v == -1 or r <= L or l >= R :
            return
        if L <= l <= r <= R:
            if k == 0:
                add_edge(x, v)
            else:
                add_edge(v, x)
            return
        if tree[v].l == tree[v].r == -1:
            if k == 0:
                add_edge(x, v)
            else:
                add_edge(v, x)
            return
        mid = l+(r-l)//2
        add_edges(k, tree[v].l if v != -1 else -1, L, R, l, mid, x)
        add_edges(k, tree[v].r if v != -1 else -1, L, R, mid, r, x)

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
        x_set.add(A[i][X0]), y_set.add(A[i][Y0]), x_set.add(A[i][X1]), y_set.add(A[i][Y1])
        x_set.add(B[i][X0]), y_set.add(B[i][Y0]), x_set.add(B[i][X1]), y_set.add(B[i][Y1])
    sorted_x = sorted(x_set)
    sorted_y = sorted(y_set)
    x_to_idx = {x:i for i, x in enumerate(sorted_x)}  # coordinate compression
    y_to_idx = {x:i for i, x in enumerate(sorted_y)}  # coordinate compression
    for i, ((a_x0, a_y0, a_x1, a_y1), (b_x0, b_y0, b_x1, b_y1)) in enumerate(izip(A, B)):
        A[i] = (x_to_idx[a_x0], y_to_idx[a_y0], x_to_idx[a_x1], y_to_idx[a_y1])
        B[i] = (x_to_idx[b_x0], y_to_idx[b_y0], x_to_idx[b_x1], y_to_idx[b_y1])

    events = []
    for t, X in enumerate([A, B], 1):
        for i, (x0, y0, x1, y1) in enumerate(X):
            events.append((y0, t, x0, x1, i))
            events.append((y1, -t, x0, x1, i))
    events.sort()
    tree, adj = [None]*N, [[] for _ in xrange(N)]
    has_no_overlap = [True]
    r0 = r1 = -1
    for _, t, l, r, i in events:
        if t == 2:
            add_edges(0, r0, l, r, 0, len(x_set)-1, i)
            r1 = update(1, r1, l, r, 0, len(x_set)-1, i)
        elif t == 1:
            add_edges(1, r1, l, r, 0, len(x_set)-1, i)
            r0 = update(0, r0, l, r, 0, len(x_set)-1, i)
        elif t == -1:
            r0 = update(0, r0, l, r, 0, len(x_set)-1, -1)
        elif t == -2:
            r1 = update(1, r1, l, r, 0, len(x_set)-1, -1)
        if not has_no_overlap[0]:
            return "NO"
    return "YES" if has_no_cycle(adj) else "NO"

X0, Y0, X1, Y1 = range(4)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, table_flipping())
