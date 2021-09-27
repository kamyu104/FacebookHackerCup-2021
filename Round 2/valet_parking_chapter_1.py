# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 2 - Problem C. Valet Parking - Chapter 1
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/C1
#
# Time:  O(R * C)
# Space: O(min(R, C))
#

from collections import Counter

def valet_parking_chapter_1():
    R, C, K = map(int, raw_input().strip().split())
    G = [raw_input().strip() for _ in xrange(R)]

    cnts = Counter()
    left, right = max(K-(C-1), 0), min(K+(C-1), R+1)
    for j in xrange(C):
        total = sum(G[i][j] == 'X' for i in xrange(R))
        curr = sum(1 <= i <= R and G[i-1][j] == 'X' for i in xrange(left))
        for i in xrange(left, right+1):
            has_x = (1 <= i <= R and G[i-1][j] == 'X')
            curr += has_x
            if has_x or curr >= K or total-curr >= R-K+1:
                cnts[i] += 1
    return min(abs(i-K)+cnts[i] for i in xrange(left, right+1))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, valet_parking_chapter_1())
