# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 2 - Problem C. Valet Parking - Chapter 2
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/C2
#
# Time:  O((R * C + S) * logR), pass in PyPy2 but Python2
# Space: O(R * C + S)
#

from heapq import heappush, heappop, heapify
from collections import defaultdict

# Template:
# https://github.com/kamyu104/GoogleCodeJam-2020/blob/master/Virtual%20World%20Finals/pack_the_slopes.py
class SegmentTree(object):  # 0-based index
    def __init__(self, N,
                 build_fn=lambda x, y: [y]*(2*x),
                 query_fn=lambda x, y: y if x is None else min(x, y),
                 update_fn=lambda x, y: y if x is None else x+y,
                 default_val=float("inf")):
        self.N = N
        self.H = (N-1).bit_length()
        self.query_fn = query_fn
        self.update_fn = update_fn
        self.tree = build_fn(N, default_val)
        self.lazy = [None]*N
        for i in reversed(xrange(1, N)):
            self.tree[i] = query_fn(self.tree[2*i], self.tree[2*i+1])

    def __apply(self, x, val):
        self.tree[x] = self.update_fn(self.tree[x], val)
        if x < self.N:
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
        L += self.N
        R += self.N
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

        L += self.N
        R += self.N
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

    def __str__(self):
        showList = []
        for i in xrange(self.N):
            showList.append(self.query(i, i))
        return ",".join(map(str, showList))

# Template:
# https://github.com/kamyu104/GoogleKickStart-2021/blob/main/Round%20F/festival4.py
def update_heaps(K, c, r, heaps):
    def lazy_delete(heap, to_remove, sign):
        while heap and sign*heap[0] in to_remove:
            to_remove[sign*heap[0]] -= 1
            if not to_remove[sign*heap[0]]:
                del to_remove[sign*heap[0]]
            heappop(heap)

    def full_delete(heap, to_remove, sign):  # Time: O(R), Space: O(R)
        result = []
        for x in heap:
            if sign*x not in to_remove:
                result.append(x)
                continue
            to_remove[sign*x] -= 1
            if not to_remove[sign*x]:
                del to_remove[sign*x]
        heap[:] = result
        heapify(heap)

    topk, others, to_remove = heaps
    if c == 1:
        heappush(topk[0], r)
        topk[1] += 1
        if topk[1] == K+1:  # keep topk with k elements
            heappush(others[0], -heappop(topk[0]))
            topk[1] -= 1
            others[1] += 1
    else:
        to_remove[r] += 1
        if others[0] and -others[0][0] >= r:
            others[1] -= 1
        else:
            topk[1] -= 1
            if others[0]:
                heappush(topk[0], -heappop(others[0]))  # keep topk with k elements
                others[1] -= 1
                topk[1] += 1
    lazy_delete(others[0], to_remove, -1)
    lazy_delete(topk[0], to_remove, 1)
    if len(topk[0])+len(others[0]) > 2*(topk[1]+others[1]):
        full_delete(others[0], to_remove, -1)
        full_delete(topk[0], to_remove, 1)

def update(R, K, r, heaps, st, diff):
    h1, h2 = heaps[0][0], heaps[1][0]
    A = h1[0][0] if R-K+1 == h1[1] else -1
    B = -h2[0][0] if K == h2[1] else R+2
    update_heaps(R-K+1, diff, r, heaps[0])
    update_heaps(K, diff, -r, heaps[1])
    if r >= A:
        new_A = h1[0][0] if R-K+1 == h1[1] else -1
        st.update(A+1, new_A-1, diff) if diff == 1 else st.update(new_A+1, A-1, diff)
        A = new_A
    if r <= B:
        new_B = -h2[0][0] if K == h2[1] else R+2
        st.update(new_B+1, B-1, diff) if diff == 1 else st.update(B+1, new_B-1, diff)
        B = new_B
    if not (r < A or r > B):
        st.update(r, r, diff)

def valet_parking_chapter_2():
    R, C, K, S = map(int, raw_input().strip().split())
    G = [list(raw_input().strip()) for _ in xrange(R)]

    heaps = [[[[[], 0], [[], 0], defaultdict(int)] for _ in xrange(2)] for _ in xrange(C)]
    st = SegmentTree(R+2, build_fn=lambda x, y: [abs((i-x)-K) if i >= x else y for i in xrange(2*x)])
    for j in xrange(C):
        for i in xrange(R):
            if G[i][j] == 'X':
                update(R, K, i+1, heaps[j], st, 1)
    result = 0
    for _ in xrange(S):
        i, j = map(lambda x: int(x)-1, raw_input().strip().split())
        G[i][j] = 'X' if G[i][j] == '.' else '.'
        update(R, K, i+1, heaps[j], st, 1 if G[i][j] == 'X' else -1)
        result += st.query(0, R+1)
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, valet_parking_chapter_2())
