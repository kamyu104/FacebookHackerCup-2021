# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 2 - Problem B. Chainblock
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/B
#
# Time:  O(N)
# Space: O(N)
#

from collections import defaultdict
from functools import partial

class UnionFind(object):  # Time: O(n * alpha(n)), Space: O(n)
    def __init__(self, n):
        self.set = range(n)
        self.rank = [0]*n
        self.ancestor = range(n)  # modified

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
        elif self.rank[x_root] > self.rank[y_root]:
            self.set[y_root] = x_root
        else:
            self.set[y_root] = x_root
            self.rank[x_root] += 1
        return True

    def find_ancestor_of_set(self, x):  # modified
        return self.ancestor[self.find_set(x)]

    def update_ancestor_of_set(self, x):  # modified
        self.ancestor[self.find_set(x)] = x

# Template:
# https://github.com/kamyu104/GoogleCodeJam-2020/blob/master/Round%202/emacs++2_concise.py
class TreeInfos(object):  # Time: O(NlogN), Space: O(NlogN), N is the number of nodes
    def __init__(self, children, cb=lambda *x:None):
        def preprocess(curr, parent):
            # visited order of the nodes
            O.append(curr)  # modified
            # depth of the node i
            D[curr] = 1 if parent == -1 else D[parent]+1
            # parent of the node i
            P[curr] = parent  # modified

        def divide(curr, parent):
            for i in reversed(xrange(len(children[curr]))):
                child = children[curr][i]
                if child == parent:
                    continue
                stk.append(partial(divide, child, curr))
            stk.append(partial(preprocess, curr, parent))

        N = len(children)
        D, P, O = [0]*N, [-1]*N, []
        stk = []
        stk.append(partial(divide, 0, -1))
        while stk:
            stk.pop()()
        self.D, self.P, self.O = D, P, O

def iter_tarjan_offline_lca(adj, cb):  # Time: O(N)
    def divide(parent, i):
        stk.append(partial(conquer, i))
        for child in reversed(adj[i]):
            if child == parent:
                continue
            stk.append(partial(merge, i, child))
            stk.append(partial(divide, i, child))

    def merge(parent, i):
        uf.union_set(parent, i)
        uf.update_ancestor_of_set(parent)

    def conquer(i):
        cb(i, uf, lookup)

    N = len(adj)
    uf = UnionFind(N)
    stk, lookup = [], [False]*N
    stk.append(partial(divide, -1, 0))
    while stk:
        stk.pop()()

def chainblock():
    N = input()
    adj = [[] for _ in xrange(N)]
    for _ in xrange(N-1):
        A, B = map(int, raw_input().strip().split())
        adj[A-1].append(B-1)
        adj[B-1].append(A-1)
    F = map(lambda x: int(x)-1, raw_input().strip().split())

    tree_infos = TreeInfos(adj)
    groups = [[] for _ in xrange(N)]
    for i, f in enumerate(F):
        groups[f].append(i)
    pairs = [defaultdict(list) for _ in xrange(N)]
    for f, idxs in enumerate(groups):
        for i in xrange(len(idxs)-1):
            pairs[f][idxs[i]].append(idxs[i+1])
            pairs[f][idxs[i+1]].append(idxs[i])
    min_depth = [float("inf")]*N
    def cb(i, uf, lookup):
        lookup[i] = True
        min_depth[F[i]] = min(min_depth[F[i]], tree_infos.D[i])
        for j in pairs[F[i]][i]:
            if not lookup[j]:
                continue
            min_depth[F[i]] = min(min_depth[F[i]], tree_infos.D[uf.find_ancestor_of_set(j)])

    iter_tarjan_offline_lca(adj, cb)
    A = [float("inf")]*N
    for f, idxs in enumerate(groups):
        for i in idxs:
            A[i] = min_depth[f]
    result = 0
    for i in reversed(tree_infos.O):
        if not i:
            break
        if A[i] == tree_infos.D[i]:
            result += 1
        else:
            A[tree_infos.P[i]] = min(A[tree_infos.P[i]], A[i])
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, chainblock())
