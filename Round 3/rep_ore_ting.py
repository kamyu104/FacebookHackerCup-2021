# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 1 - Problem A. Rep-ore-ting
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/A
#
# Time:  O(M + N * alpha(N)) = O(M + N)
# Space: O(N)
#

# Template:
# https://github.com/kamyu104/FacebookHackerCup-2021/blob/e354101c2e6eac7bc7fe647f09bebb579406261f/Round%201/blockchain.py
class UnionFind(object):  # Time: O(n * alpha(n)), Space: O(n)
    def __init__(self, n):
        self.set = range(n)
        self.rank = [0]*n
        self.size = [1]*n  # modified
        self.right = range(n)  # modified

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
            return 0
        cnt = self.size[x_root]*self.size[y_root]  # modified
        if self.rank[x_root] < self.rank[y_root]:  # union by rank
            self.set[x_root] = y_root
            self.size[y_root] += self.size[x_root]  # modified
            self.right[y_root] = max(self.right[x_root], self.right[y_root])  # modified
        elif self.rank[x_root] > self.rank[y_root]:
            self.set[y_root] = x_root
            self.size[x_root] += self.size[y_root]  # modified
            self.right[x_root] = max(self.right[x_root], self.right[y_root])  # modified
        else:
            self.set[y_root] = x_root
            self.rank[x_root] += 1
            self.size[x_root] += self.size[y_root]  # modified
            self.right[x_root] = max(self.right[x_root], self.right[y_root])  # modified
        return cnt  # modified

    def right_set(self, x):  # modified
        return self.right[self.find_set(x)]

def mulmod(a, b):
    return (a*b)%MOD

def rep_ore_ting():
    N, M = map(int, raw_input().strip().split())
    uf = UnionFind(N)
    result, total = 1, N*(N-1)//2
    for _ in xrange(M):
        A, B = map(int, raw_input().strip().split())
        A -= 1
        B -= 1
        if A > B:
            A, B = B, A
        A = uf.right_set(A)
        while A < B:
            total += uf.union_set(A, A+1)
            A = uf.right_set(A)
        result = mulmod(result, total)
    return result

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, rep_ore_ting())
