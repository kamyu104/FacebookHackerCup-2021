# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 2 - Problem C. Valet Parking - Chapter 2
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/C2
#
# Time:  O(S * min(R, C) + (R * C + S) * logR)
# Space: O(R * C)
#

from sortedcontainers import SortedList

def update(R, K, r, sl, cnts, left, right, diff):
    A = sl[(len(sl)-(R-K+1)+1)-1] if R-K+1 <= len(sl) else -1
    B = sl[K-1] if K <= len(sl) else R+2
    sl.add(r) if diff > 0 else sl.remove(r)
    if r >= A:
        new_A = sl[(len(sl)-(R-K+1)+1)-1] if R-K+1 <= len(sl) else -1
        nl, nr = (max(left, A+1), min(right, new_A-1)) if diff == 1 else (max(left, new_A+1), min(right, A-1))
        for i in xrange(nl, nr+1):
            cnts[i-left] += diff
        A = new_A
    if r <= B:
        new_B = sl[K-1] if K <= len(sl) else R+2
        nl, nr = (max(left, new_B+1), min(right, B-1)) if diff == 1 else (max(left, B+1), min(right, new_B-1))
        for i in xrange(nl, nr+1):
            cnts[i-left] += diff
        B = new_B
    if not (r < A or r > B):
        if left <= r <= right:
            cnts[r-left] += diff

def valet_parking_chapter_2():
    R, C, K, S = map(int, raw_input().strip().split())
    G = [list(raw_input().strip()) for _ in xrange(R)]

    sls = [SortedList() for _ in xrange(C)]
    left, right = max(K-(C-1), 0), min(K+(C-1), R+1)
    cnts = [abs(i-K) for i in xrange(left, right+1)]
    for j in xrange(C):
        for i in xrange(R):
            if G[i][j] == 'X':
                update(R, K, i+1, sls[j], cnts, left, right, 1)
    result = 0
    for _ in xrange(S):
        i, j = map(lambda x: int(x)-1, raw_input().strip().split())
        G[i][j] = 'X' if G[i][j] == '.' else '.'
        update(R, K, i+1, sls[j], cnts, left, right, 1 if G[i][j] == 'X' else -1)
        result += min(cnts)
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, valet_parking_chapter_2())
