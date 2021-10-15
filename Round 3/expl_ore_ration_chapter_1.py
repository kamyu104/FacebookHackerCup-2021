# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 3 - Problem D. Expl-ore-ration Chapter 1
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/D1
#
# Time:  O(R * C * log(R * C) + R * C * alpha(R * C)) = O(R * C * log(R * C))
# Space: O(R * C)
#

class UnionFind(object):  # Time: O(n * alpha(n)), Space: O(n)
    def __init__(self, n):
        self.set = range(n)
        self.rank = [0]*n
        self.has_robot = [0]*n  # modified

    def find_set(self, x):
        stk = []
        while self.set[x] != x:  # path compression
            stk.append(x)
            x = self.set[x]
        while stk:
            self.set[stk.pop()] = x
        return x

    def union_set(self, x, y):
        x, y = self.find_set(x), self.find_set(y)
        if x == y:
            return False
        if self.rank[x] > self.rank[y]:  # union by rank
            x, y = y, x
        self.set[x] = self.set[y]
        if self.rank[x] == self.rank[y]:
            self.rank[y] += 1
        self.has_robot[y] = self.has_robot[x] | self.has_robot[y]  # modified
        return True

    def add_robot(self, x):  # added
        x = self.find_set(x)
        if self.has_robot[x]:
            return 0
        self.has_robot[x] = 1
        return 1

def expl_ore_ration_chapter_1():
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
    for i, s in enumerate(S):
        events.append((s, len(H), i))
    events.sort(reverse=True)

    uf = UnionFind(R*C)
    result = total = 0
    for h, a, b in events:
        if a != len(H):
            uf.union_set(a, b)
            continue
        if H[b] <= h:
            continue
        result += 1
        total += uf.add_robot(b)
    return "%s %s" % (result, total)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, expl_ore_ration_chapter_1())
