# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Final Round - Problem A. And
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/A
#
# Time:  O(L * N * alpha(N)) = O(L * N), L is the max length of the result bitstring
# Space: O(L * N)
#

from copy import deepcopy

class UnionFind(object):  # Time: O(n * alpha(n)), Space: O(n)
    def __init__(self, n):
        self.set = range(n)
        self.rank = [0]*n
        self.count = [1]*n
        self.diff_to_root = [0]*n  # added
        self.diff_count = [0]*n  # added

    def find_set(self, x):
        stk = []
        while self.set[x] != x:  # path compression
            stk.append(x)
            x = self.set[x]
        while stk:
            self.diff_to_root[stk[-1]] ^= self.diff_to_root[self.set[stk[-1]]]  # added
            self.set[stk.pop()] = x
        return x

    def union_set(self, x, y, d):  # modified
        i, j = x, y  # added
        x, y = self.find_set(x), self.find_set(y)
        d ^= self.diff_to_root[i] ^ self.diff_to_root[j]  # added
        if x == y:
            return not d  # modified
        if self.rank[x] > self.rank[y]:  # union by rank
            x, y = y, x
        self.set[x] = self.set[y]
        if self.rank[x] == self.rank[y]:
            self.rank[y] += 1
        self.count[y] += self.count[x]
        self.diff_to_root[x] = d  # added
        self.diff_count[y] += self.count[x]-self.diff_count[x] if d else self.diff_count[x]  # added
        return True

def and_():
    N, K = map(int, raw_input().strip().split())
    A_B = [raw_input().strip().split() for _ in xrange(N)]
    max_l = min(max(len(a), len(b)) for a, b in A_B)
    A_B = [(a[::-1][:max_l]+"0"*(max_l-len(a)), b[::-1][:max_l]+"0"*(max_l-len(b))) for a, b in A_B]
    uf = UnionFind(N)
    result = [0]*(max_l+1)
    for bit in reversed(xrange(max_l)):
        if all(a[bit] == b[bit] == '1' for a, b in A_B):
            result[bit] = 2
            continue
        if any(a[bit] == b[bit] == '0' for a, b in A_B):
            continue
        possible = True
        new_uf = deepcopy(uf)
        j = -1
        for i, (a, b) in enumerate(A_B):
            if a[bit] == b[bit]:
                continue
            if j == -1:
                j = i
                continue
            possible = new_uf.union_set(i, j, A_B[i][0][bit] != A_B[j][0][bit])
            if not possible:
                break
        if not possible:
            continue
        if sum(min(new_uf.diff_count[i], new_uf.count[i]-new_uf.diff_count[i]) for i in xrange(N) if new_uf.find_set(i) == i) > K:
            continue
        uf = new_uf
        result[bit] = 1
    for i in xrange(max_l):
        result[i+1] += result[i]//2
        result[i] %= 2
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    result.reverse()
    return "".join(map(str, result))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, and_())
