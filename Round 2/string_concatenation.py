# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 2 - Problem D. String Concatenation
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/D
#
# Time:  O(2^X * (N - X) / C) ~= O(1e8) on average, pass in PyPy2 but Python2
# Space: O(N)
#

def find_equal_sum_masks(L, idxs):  # Time: O(2^X * (N-X)/C) = O(2^23 * (2e5-23)/6) ~= O(1e8) on average, O(1e11) at worst, C = 6 on average
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

def add_remains(N, K, L, A, B, R):
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
                if (mask_A&bit) and not ((mask_B&bit)):
                    A.add(i)
                elif (mask_B&bit) and not ((mask_A&bit)):
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
    return add_remains(N, K, L, A, B, R)

MAX_L = 200000
X = 1
while 2**X < X*MAX_L+1:  # pigeonhole principle
    X += 1
assert(X == 23)  # we can always find equal sum subsets by 23 or more strings
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, string_concatenation())
