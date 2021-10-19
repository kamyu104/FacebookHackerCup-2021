# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 3 - Problem D. Expl-ore-ation Chapter 3
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/D3
#
# Time:  O((R * C) * log(R * C) + R * C * alpha(R * C) + (R * C + K) * log(R * C)^2) = O((R * C + K) * log(R * C)^2)
# Space: O(R * C)
#

from functools import partial

# Template:
# https://github.com/kamyu104/FacebookHackerCup-2021/blob/main/Round%202/valet_parking_chapter_2.py
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

    def kth_element(self, k):
        floor_log2_n = (len(self.__bit)-1).bit_length()-1
        pow_i = 2**floor_log2_n
        total = pos = 0  # 1-indexed
        for _ in reversed(xrange(floor_log2_n+1)):  # O(logN)
            if pos+pow_i < len(self.__bit) and total+self.__bit[pos+pow_i] < k:  # find max pos s.t. total < k
                total += self.__bit[pos+pow_i]
                pos += pow_i
            pow_i >>= 1
        return (pos+1)-1  # 0-indexed, return min pos s.t. total >= k if pos exists else n

class UnionFind(object):  # Time: O(n * alpha(n)), Space: O(n)
    def __init__(self, n):
        self.set = range(n)
        self.rank = [0]*n
        self.adj = [[] for _ in xrange(n)]  # added
        self.height = [INF]*n  # added
        self.node = range(n)  # added

    def find_set(self, x):
        stk = []
        while self.set[x] != x:  # path compression
            stk.append(x)
            x = self.set[x]
        while stk:
            self.set[stk.pop()] = x
        return x

    def union_set(self, x, y, h):
        x, y = self.find_set(x), self.find_set(y)
        if x == y:
            return False
        if self.rank[x] > self.rank[y]:  # union by rank
            x, y = y, x
        self.set[x] = self.set[y]
        if self.rank[x] == self.rank[y]:
            self.rank[y] += 1

        # belows are all added
        self.adj.append([self.node[x], self.node[y]])
        self.height.append(h)
        self.node[y] = len(self.adj)-1
        return True

# Template: https://github.com/kamyu104/GoogleCodeJam-2020/blob/master/Virtual%20World%20Finals/pack_the_slopes.py
class HLD(object):  # Heavy-Light Decomposition
    def __init__(self, root, adj):
        self.__children = adj
        self.__size = [-1]*len(adj)  # Space: O(N)
        self.__chain = [-1]*len(adj)
        self.L = [-1]*len(adj)
        self.R = [-1]*len(adj)
        self.P = [[] for _ in xrange(len(adj))]
        self.inv = [-1]*len(adj)
        self.bit = BIT(len(adj))  # added

        self.__find_heavy_light(root)
        self.__decompose(root)

    def __find_heavy_light(self, root):  # Time: O(N)
        def divide(curr):
            size[curr] = 1
            stk.append(partial(postprocess, curr))
            for child in reversed(children[curr]):
                stk.append(partial(divide, child))

        def postprocess(curr):
            for i, child in enumerate(children[curr]):
                size[curr] += size[child]
                if size[child] > size[children[curr][0]]:
                    children[curr][0], children[curr][i] = children[curr][i], children[curr][0]  # make the first child heavy

        stk, children, size = [], self.__children, self.__size
        stk.append(partial(divide, root))
        while stk:
            stk.pop()()

    def __decompose(self, root):  # Time: O(N)
        def divide(curr, parent):
            # ancestors of the node i
            if parent != -1:
                P[curr].append(parent)
            i = 0
            while i < len(P[curr]) and i < len(P[P[curr][i]]):
                P[curr].append(P[P[curr][i]][i])
                i += 1
            # the subtree of the node curr is represented by preorder traversal index L[curr]..R[curr]
            C[0] += 1
            L[curr] = C[0]
            inv[C[0]] = curr
            chain[curr] = curr if parent == -1 or children[parent][0] != curr else chain[parent]  # create a new chain if it is not the first child which is heavy
            stk.append(partial(postprocess, curr))
            for child in reversed(children[curr]):
                stk.append(partial(divide, child, curr))

        def postprocess(curr):
            R[curr] = C[0]

        stk, children, chain, L, R, P, inv, C = [], self.__children, self.__chain, self.L, self.R, self.P, self.inv, [-1]
        stk.append(partial(divide, root, -1))
        while stk:
            stk.pop()()

    def highest_valid_ancestor(self, S, uf, i):  # added, Time: O(log(R * C))
        s = S[i]
        for j in reversed(xrange(len(self.P[i]))):
            if j < len(self.P[i]) and uf.height[self.P[i][j]] > s:  # find highest ancestor x s.t. uf.height[x] > s
                i = self.P[i][j]
        return i

    def update(self, i, d):  # added, Time: O(log(R * C))
        self.bit.add(self.L[i], d)

    def subtree_has_robot(self, i, exclude_root):  # added, Time: O(log(R * C))
        return self.bit.query(self.R[i])-self.bit.query((self.L[i]+exclude_root)-1) > 0

    def find_closest_ancestor_has_robot(self, i):  # added, Time: O(log(R * C)^2)
        while i >= 0:
            j = self.__chain[i]
            cnt = self.bit.query(self.L[i])
            if cnt-self.bit.query(self.L[j]-1) > 0:  # Time: O(log(R * C))
                return self.inv[self.bit.kth_element(cnt)]
            i = self.P[j][0] if self.P[j] else -1  # O(log(R * C)) times
        return -1

def update_cell(H, S, uf, hld, i, d):
    dx = dy = 0
    if S[i] >= H[i]:
        return dx, dy
    dx += d
    i = hld.highest_valid_ancestor(S, uf, i)
    if d == -1:
        hld.update(i, d)
    if not hld.subtree_has_robot(i, 0):
        a = hld.find_closest_ancestor_has_robot(i)
        if a < 0 or hld.subtree_has_robot(a, 1):
            dy += d
    if d == 1:
        hld.update(i, d)
    return dx, dy

def expl_ore_ation_chapter_3():
    R, C = map(int, raw_input().strip().split())
    H = []
    for _ in xrange(R):
        H.extend(map(int, raw_input().strip().split()))
    S = []
    for _ in xrange(R):
        S.extend(map(int, raw_input().strip().split()))

    events = []
    for i in xrange(R*C):
        if i-C >= 0:  # up
            events.append((min(H[i], H[i-C]), i, i-C))
        if i%C-1 >= 0:  # left
            events.append((min(H[i], H[i-1]), i, i-1))
    events.sort(reverse=True)  # Time: O((R * C) * log(R * C)), Space: O(R * C)
    uf = UnionFind(R*C)
    for h, a, b in events:
        uf.union_set(a, b, h)
    hld = HLD(len(uf.adj)-1, uf.adj)

    X, Y = 0, 0
    for i in xrange(R*C):
        dx, dy = update_cell(H, S, uf, hld, i, 1)
        X += dx
        Y += dy
    result = total = 0
    for idx in xrange(input()):
        A, B, U = map(int, raw_input().strip().split())
        A, B, U = ((A^Y)-1, (B^Y)-1, U^Y) if idx else (A-1, B-1, U)
        i = A*C+B
        dx, dy = update_cell(H, S, uf, hld, i, -1)  # remove
        X += dx
        Y += dy
        S[i] = U  # update
        dx, dy = update_cell(H, S, uf, hld, i, 1)  # add
        X += dx
        Y += dy
        result += X
        total += Y
    return "%s %s" % (result, total)

INF = float("inf")
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, expl_ore_ation_chapter_3())
