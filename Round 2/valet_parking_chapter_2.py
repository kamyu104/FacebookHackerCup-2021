# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 2 - Problem C. Valet Parking - Chapter 2
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/D
#
# Time:  O((C * R + S) * logR), pass in PyPy2 but Python2
# Space: O(C * R)
#

# Template:
# https://github.com/kamyu104/GoogleKickStart-2021/blob/main/Round%20F/festival.py
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

    def binary_lift(self, k):
        floor_log2_n = (len(self.__bit)-1).bit_length()-1
        pow_i = 2**floor_log2_n
        total = pos = 0  # 1-indexed
        for _ in reversed(xrange(floor_log2_n+1)):  # O(logN)
            if pos+pow_i < len(self.__bit) and total+self.__bit[pos+pow_i] < k:  # find max pos s.t. total < k
                total += self.__bit[pos+pow_i]
                pos += pow_i
            pow_i >>= 1
        return (pos+1)-1  # 0-indexed, return min pos s.t. total >= k if pos exists else n

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

def update(R, K, i, bit, st, diff):
    r = i+1
    total = bit.query(R-1)
    A = bit.binary_lift(total-(R-K+1)+1)+1 if R-K+1 <= total else -1
    B = bit.binary_lift(K)+1 if K <= total else R+2
    bit.add(i, diff)
    total += diff
    if r >= A:
        new_A = bit.binary_lift(total-(R-K+1)+1)+1 if R-K+1 <= total else -1
        st.update(A+1, new_A-1, diff) if diff == 1 else st.update(new_A+1, A-1, diff) 
        A = new_A
    if r <= B:
        new_B = bit.binary_lift(K)+1 if K <= total else R+2
        st.update(new_B+1, B-1, diff) if diff == 1 else st.update(B+1, new_B-1, diff)
        B = new_B
    if not (r < A or r > B):
        st.update(r, r, diff)

def valet_parking_chapter_2():
    R, C, K, S = map(int, raw_input().strip().split())
    G = [list(raw_input().strip()) for _ in xrange(R)]

    bits = [BIT(R) for _ in xrange(C)]
    st = SegmentTree(R+2, build_fn=lambda x, y: [abs((i-x)-K) if i >= x else y for i in xrange(2*x)], default_val=float("inf"))
    for j in xrange(C):
        for i in xrange(R):
            if G[i][j] == 'X':
                update(R, K, i, bits[j], st, 1)
    result = 0
    for _ in xrange(S):
        i, j = map(lambda x: int(x)-1, raw_input().strip().split())
        G[i][j] = 'X' if G[i][j] == '.' else '.'
        update(R, K, i, bits[j], st, 1 if G[i][j] == 'X' else -1)
        result += st.query(0, R+1)
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, valet_parking_chapter_2())
