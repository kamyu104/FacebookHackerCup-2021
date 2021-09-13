# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 1 - Problem C. Blockchain
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-1/problems/C
#
# Time:  O(N * (logN + MAX_C))
# Space: O(N * MAX_C)
#

from collections import defaultdict
from functools import partial

class UnionFind(object):  # Time: O(n * alpha(n)), Space: O(n)
    def __init__(self, n):
        self.set = range(n)
        self.rank = [0]*n
        self.size = [1]*n  # modified

    def find_set(self, x):
        stk = []
        while self.set[x] != x:  # path compression
            stk.append(x)
            x = self.set[x]
        while stk:
            self.set[stk.pop()] = x
        return x

    def union_set(self, x, y):
        x_root, y_root = map(self.find_set, (x, y))
        if x_root == y_root:
            return False
        if self.rank[x_root] < self.rank[y_root]:  # union by rank
            self.set[x_root] = y_root
            self.size[y_root] += self.size[x_root]  # modified
        elif self.rank[x_root] > self.rank[y_root]:
            self.set[y_root] = x_root
            self.size[x_root] += self.size[y_root]  # modified
        else:
            self.set[y_root] = x_root
            self.size[x_root] += self.size[y_root]  # modified
            self.rank[x_root] += 1
        return True

    def size_set(self, x):  # modified
        return self.size[self.find_set(x)]

def addmod(a, b):
    return (a+b)%MOD

def submod(a, b):
    return (a-b)%MOD

def mulmod(a, b):
    return (a*b)%MOD

def iter_postorder_traversal(adj, max_c):  # Time: O(N)
    def divide(parent, i):
        stk.append(partial(conquer, parent, i))
        for j in reversed(xrange(len(adj[i]))):
            child, _ = adj[i][j]
            if child == parent:
                continue
            stk.append(partial(divide, i, child))

    def conquer(parent, i):
        for child, c in adj[i]:
            if child == parent:
                continue
            for j in xrange(1, c+1):
                dp1[i][j] = addmod(dp1[i][j], dp1[child][j])

    stk, dp1 = [], [[int(j != 0) for j in xrange(max_c+1)] for _ in xrange(len(adj))]  # dp1[i][j] = number of nodes reachable down from i via capacity >= j edges
    stk.append(partial(divide, -1, 0))
    while stk:
        stk.pop()()
    return dp1

def iter_preorder_traversal(adj, total, dp1):  # Time: O(N)
    def divide(parent, i):
        for j in reversed(xrange(len(adj[i]))):
            child, _ = adj[i][j]
            if child == parent:
                continue
            stk.append(partial(divide, i, child))
        stk.append(partial(init, parent, i))

    def init(parent, i):
        for child, c in adj[i]:
            if child == parent:
                continue
            for j in xrange(1, len(dp2[i])):
                if j <= c:
                    dp2[child][j] = addmod(dp2[i][j], submod(dp1[i][j], dp1[child][j]))
            total_i_child, prev = total, 0
            for j in reversed(xrange(1, c+1)):
                curr = mulmod(dp1[child][j], dp2[child][j])
                cnt = submod(curr, prev)
                total_i_child = submod(total_i_child, mulmod(j, cnt))
                prev = curr
            result[0] = mulmod(result[0], total_i_child)

    result = [1]
    stk, dp2 = [], [[0]*len(dp1[0]) for _ in xrange(len(adj))]  # dp2[i][j] = number of nodes reachable up from i via capacity >= j edges
    stk.append(partial(divide, -1, 0))
    while stk:
        stk.pop()()
    return result[0]

def blockchain():
    N = input()

    adj = defaultdict(list)
    edges = []
    for _ in xrange(N-1):
        A, B, C = map(int, raw_input().strip().split())
        adj[A-1].append((B-1, C))
        adj[B-1].append((A-1, C))
        edges.append((C, (A-1, B-1)))
    edges.sort(reverse=True)
    total = 0
    uf = UnionFind(N)
    for c, (a, b) in edges:
        total = addmod(total, mulmod(c, mulmod(uf.size_set(a), uf.size_set(b))))
        uf.union_set(a, b)
    dp1 = iter_postorder_traversal(adj, edges[0][0])
    return iter_preorder_traversal(adj, total, dp1)

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, blockchain())
