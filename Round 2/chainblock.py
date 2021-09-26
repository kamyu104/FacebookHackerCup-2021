# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 2 - Problem B. Chainblock
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/B
#
# Time:  O(NlogN)
# Space: O(N)
#

from functools import partial

# Template:
# https://github.com/kamyu104/GoogleCodeJam-2020/blob/2631d31657f3c32acc7ff1af43ce9a41f6b9530d/Round%202/emacs%2B%2B2_concise.py
class TreeInfos(object):  # Time: O(NlogN), Space: O(NlogN), N is the number of nodes
    def __init__(self, children, cb=lambda *x:None):
        def preprocess(curr, parent):
            # visited order of the nodes
            O.append(curr)  # modified
            # depth of the node i
            D[curr] = 1 if parent == -1 else D[parent]+1
            # ancestors of the node i
            if parent != -1:
                P[curr].append(parent)
            i = 0
            while i < len(P[curr]) and i < len(P[P[curr][i]]):
                P[curr].append(P[P[curr][i]][i])
                i += 1
            # the subtree of the node i is represented by traversal index L[i]..R[i]
            C[0] += 1
            L[curr] = C[0]

        def divide(curr, parent):
            stk.append(partial(postprocess, curr))
            for i in reversed(xrange(len(children[curr]))):
                child = children[curr][i]
                if child == parent:
                    continue
                stk.append(partial(divide, child, curr))
            stk.append(partial(preprocess, curr, parent))

        def postprocess(curr):
            R[curr] = C[0]

        N = len(children)
        L, R, D, P, C, O = [0]*N, [0]*N, [0]*N, [[] for _ in xrange(N)], [-1], []
        stk = []
        stk.append(partial(divide, 0, -1))
        while stk:
            stk.pop()()
        assert(C[0] == N-1)
        self.L, self.R, self.D, self.P, self.O = L, R, D, P, O

    # Template:
    # https://github.com/kamyu104/FacebookHackerCup-2019/blob/master/Final%20Round/little_boat_on_the_sea.py
    def is_ancestor(self, a, b):  # includes itself
        return self.L[a] <= self.L[b] <= self.R[b] <= self.R[a]

    def lca(self, a, b):
        if self.D[a] > self.D[b]:
            a, b = b, a
        if self.is_ancestor(a, b):
            return a
        for i in reversed(xrange(len(self.P[a]))):  # O(logN)
            if i < len(self.P[a]) and not self.is_ancestor(self.P[a][i], b):
                a = self.P[a][i]
        return self.P[a][0]

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
    A = [float("inf")]*N
    for f, idxs in enumerate(groups):
        if not idxs:
            continue
        lca = reduce(lambda lca, x: tree_infos.lca(lca, x), idxs)
        for i in idxs:
            A[i] = tree_infos.D[lca]
    result = 0
    for i in reversed(tree_infos.O):
        if not i:
            break
        if A[i] == tree_infos.D[i]:
            result += 1
        else:
            A[tree_infos.P[i][0]] = min(A[tree_infos.P[i][0]] , A[i])
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, chainblock())
