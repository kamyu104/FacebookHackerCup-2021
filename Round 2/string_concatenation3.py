# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 2 - Problem D. String Concatenation
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/D
#
# Time:  O(N + L*(logN1)^2 + N2*sqrt(N2*L) + X*2^X*(N3-X)/C) ~= O(1e8) on average, O(2e9) at worst
# Space: O(N)
#

from random import seed, randint

# Template:
# https://github.com/kamyu104/LeetCode-Solutions/blob/master/Python/range-sum-query-mutable.py
class BIT(object):  # 0-indexed.
    def __init__(self, nums):
        self.__bit = [0]*(len(nums)+1)  # Extra one for dummy node.
        for i in xrange(1, len(self.__bit)):
            self.__bit[i] = nums[i-1] + self.__bit[i-1]
        for i in reversed(xrange(1, len(self.__bit))):
            last_i = i - (i & -i)
            self.__bit[i] -= self.__bit[last_i]

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

    # Template:
    # https://github.com/kamyu104/GoogleKickStart-2021/blob/main/Round%20F/festival.py
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

def update_remains(A, B, R):
    R[:] = [i for i in R if i not in A and i not in B]

def add_equal_1sums(L, A, B, R):  # Time: O(N), N1 = O(N)
    lookup = {}
    for a in R:
        total = L[a]
        if total not in lookup:
            lookup[total] = a
            continue
        A.add(a)
        B.add(lookup[total])
        del lookup[total]
    update_remains(A, B, R)
    return R

def add_equal_2sums(L, A, B, R):  # Time: O(N1) + O((2 * L) * (1/N1 + 1/(N1-1) + ... + 1/1)) * O(logN1) = O(N1 + L * (logN1)^2) ~= O(6e7), N2 = O(894)
    cnt = None
    while len(R) != cnt:  # O(c) times, c ~= 4 at most, first run removes most equal sum pairs, run once is actually enough
        cnt = len(R)
        lookup = {}
        R_inv = {x:i for i, x in enumerate(R)}
        bit = BIT([1]*len(R))
        l = 1
        while l < bit.query(len(R)-1):
            i = 0
            while i < bit.query(len(R)-1):
                if l == bit.query(len(R)-1):
                    break
                j = (i+l)%bit.query(len(R)-1)
                a, b = R[bit.kth_element(i+1)], R[bit.kth_element(j+1)]
                total = L[a]+L[b]
                if total in lookup:
                    for x in lookup[total]:
                        if x in (a, b) or x in A or x in B:
                            del lookup[total]
                            break
                if total not in lookup:
                    lookup[total] = (a, b)
                    i += 1
                    continue
                A.add(a), A.add(b)
                c, d = lookup[total]
                B.add(c), B.add(d)
                del lookup[total]
                for x in (a, b, c, d):
                    bit.add(R_inv[x], -1)
                i += 1
            l += 1
        update_remains(A, B, R)
    assert(len(R) <= 894)  # max v s.t. v(v-1)/2! <= 2*MAX_L
    return R

def add_equal_random_subsets(L, A, B, R):  # Time: O(N2 * sqrt(N2 * L)) ~= O(1e7), N3 = O(TARGET)
    curr = R
    while len(curr) > TARGET: # O(N2 + N2/2 + N2/4 + ... + TARGET)) = O(N2) times on average
        lookup = {}
        while True:  # O(sqrt(N2 * L)) times on average by birthday paradox
            total = 0
            subset_A = set()
            for i in curr:
                if randint(0, 1):
                    subset_A.add(i)
                    total += L[i]
            if total not in lookup:
                lookup[total] = subset_A
                continue
            subset_B = lookup[total]
            nxt = []
            for i in curr:
                if i in subset_A and i not in subset_B:
                    A.add(i)
                elif i in subset_B and i not in subset_A:
                    B.add(i)
                else:
                    nxt.append(i)
            curr = nxt
            break
    update_remains(A, B, R)
    assert(len(R) <= TARGET)
    return R

def find_equal_sum_masks(L, idxs):  # Time: O(X*2^X)
    lookup = {}
    for mask in xrange(1, 1<<len(idxs)):
        total, bit = 0, 1
        for i in idxs:
            if mask&bit:
                total += L[i]
            bit <<= 1
        if total in lookup:
            return mask, lookup[total]
        lookup[total] = mask
    return None

def add_remains(N, K, L, A, B, R):  # Time: O(X*2^X) * O((N3-X)/C) = O(23*2^23 * (100-23)/6) ~= O(1e8) on average, O(2e9) at worst, C = 6 on average
    curr = []
    for i in xrange(len(R)):
        curr.append(R[i])
        if N-(len(A)+len(B)) <= K:
            break
        if len(curr) == X or i == len(R)-1:
            pair_masks = find_equal_sum_masks(L, curr)
            if not pair_masks:
                return "Impossible"
            mask_A, mask_B = pair_masks
            nxt = []
            bit = 1
            for i in curr:
                if (mask_A&bit) and not (mask_B&bit):
                    A.add(i)
                elif (mask_B&bit) and not (mask_A&bit):
                    B.add(i)
                else:
                    nxt.append(i)
                bit <<= 1
            curr = nxt
    return "Possible\n%s\n%s" % (" ".join(map(lambda x: str(x+1), A)), " ".join(map(lambda x: str(x+1), B)))

def string_concatenation():
    N, K = map(int, raw_input().strip().split())
    L = map(int, raw_input().strip().split())

    A, B, R = set(), set(), range(N)
    add_equal_1sums(L, A, B, R)
    add_equal_2sums(L, A, B, R)
    add_equal_random_subsets(L, A, B, R)
    return add_remains(N, K, L, A, B, R)

seed(0)
TARGET = 100
MAX_L = 200000
X = 1
while 2**X < X*MAX_L+1:  # pigeonhole principle
    X += 1
assert(X == 23)  # we can always find equal sum subsets by 23 or more strings
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, string_concatenation())
