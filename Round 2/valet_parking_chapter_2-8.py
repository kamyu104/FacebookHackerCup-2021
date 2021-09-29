# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 2 - Problem C. Valet Parking - Chapter 2
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/C2
#
# Time:  O(S * min(R, C) + (R * C + S) * logR)
# Space: O(R * C)
#

from heapq import heappush, heappop

# Template:
# https://github.com/kamyu104/GoogleKickStart-2021/blob/main/Round%20F/festival4.py
def update_heaps(K, c, r, heaps):
    topk, topk_to_remove, others, others_to_remove = heaps
    if c == 1:
        heappush(topk[0], r)
        topk[1] += 1
        if topk[1] == K+1:  # keep topk with k elements
            heappush(others, -heappop(topk[0]))
            topk[1] -= 1
    else:
        if others and r <= -others[0]:
            heappush(others_to_remove, -r)
        else:
            heappush(topk_to_remove, r)
            topk[1] -= 1
            if others:
                heappush(topk[0], -heappop(others))  # keep topk with k elements
                topk[1] += 1
    while topk[0] and topk_to_remove and topk[0][0] == topk_to_remove[0]:
        heappop(topk[0]), heappop(topk_to_remove)
    while others and others_to_remove and others[0] == others_to_remove[0]:
        heappop(others), heappop(others_to_remove)

def update(R, K, r, heaps, cnts, left, right, diff):
    h1, h2 = heaps[0][0], heaps[1][0]
    A = h1[0][0] if R-K+1 == h1[1] else -1
    B = -h2[0][0] if K == h2[1] else R+2
    update_heaps(R-K+1, diff, r, heaps[0])
    update_heaps(K, diff, -r, heaps[1])
    if r >= A:
        new_A = h1[0][0] if R-K+1 == h1[1] else -1
        nl, nr = (max(left, A+1), min(right, new_A-1)) if diff == 1 else (max(left, new_A+1), min(right, A-1))
        for i in xrange(nl, nr+1):
            cnts[i-left] += diff
        A = new_A
    if r <= B:
        new_B = -h2[0][0] if K == h2[1] else R+2
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

    heaps = [[[[[], 0], [], [], []] for _ in xrange(2)] for _ in xrange(C)]
    left, right = max(K-(C-1), 0), min(K+(C-1), R+1)
    cnts = [abs(i-K) for i in xrange(left, right+1)]
    for j in xrange(C):
        for i in xrange(R):
            if G[i][j] == 'X':
                update(R, K, i+1, heaps[j], cnts, left, right, 1)
    result = 0
    for _ in xrange(S):
        i, j = map(lambda x: int(x)-1, raw_input().strip().split())
        G[i][j] = 'X' if G[i][j] == '.' else '.'
        update(R, K, i+1, heaps[j], cnts, left, right, 1 if G[i][j] == 'X' else -1)
        result += min(cnts)
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, valet_parking_chapter_2())
