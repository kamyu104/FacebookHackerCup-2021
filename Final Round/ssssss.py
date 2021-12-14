# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Final Round - Problem B. SSSSSS
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/B
#
# Time:  O(NlogN)
# Space: O(N)
#

from heapq import heappush, heappop

def ssssss():
    N = input()
    A_B = [map(int, raw_input().strip().split()) for _ in xrange(N)]
    intervals = []
    result = [0]*2
    max_idx = max_b = -1
    for i, (A, B) in enumerate(A_B):
        if not A:
            if max_b == -1 or max_b < B:
                max_b, max_idx = B, i
            result[0] += 1
        else:
            intervals.append((A, 0, i))
            intervals.append((B, 1, i))
    if max_idx == -1:
        return " ".join(map(str, result))
    intervals.append((max_b, 1, max_idx))
    intervals.sort()
    a = b = max_idx
    lookup = [False]*N
    min_heap = []
    for _, t, i in intervals:
        if t == 0:
            heappush(min_heap, (A_B[i][1], i))
            lookup[i] = True
            continue
        if A_B[a][1] > A_B[b][1]:
            a, b = b, a
        if lookup[i]:
            a = i
            lookup[a] = False
            result[0] += 1
            result[1] += 1
        elif i == b:
            a, b = b, a
        elif i != a:  # (not lookup[i]) and (i != a) and (i != b)
            continue
        while min_heap and not lookup[min_heap[0][1]]:
            heappop(min_heap)
        if min_heap:  # a must go to another lowest ladder
            same = (a == b)
            a = heappop(min_heap)[1]
            lookup[a] = False
            result[0] += 1
            result[1] += 1
            if not same:
                continue
            while min_heap and not lookup[min_heap[0][1]]:
                heappop(min_heap)
            if min_heap:  # b must go to another lowest ladder
                b = heappop(min_heap)[1]
                lookup[b] = False
                result[0] += 1
                result[1] += 1
            else:  # b must go to a since there is no other new ladder to go
                assert(a != b)
                b = a
                result[1] += 1
        elif a != b:  # a must go to b since there is no other new ladder to go
            a = b
            result[1] += 1
        else:  # (not min_heap) and (a == b) => no ladder to go
            break
    assert(a == b)
    return " ".join(map(str, result))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ssssss())
