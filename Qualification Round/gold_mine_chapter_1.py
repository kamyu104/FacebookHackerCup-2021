# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Qualification Round - Problem C1. Gold Mine - Chapter 1
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/qualification-round/problems/C1
#
# Time:  O(N)
# Space: O(N)
#

from heapq import heappush, heappop

def dfs(adj, C, parent, curr):
    min_heap, cnt = [], 2 if not curr else 1
    for child in adj[curr]:
        if child == parent:
            continue
        heappush(min_heap, dfs(adj, C, curr, child))
        if len(min_heap) > cnt:
            heappop(min_heap)
    return C[curr]+sum(min_heap)

def gold_mine_chapter_1():
    N = input()
    C = map(int, raw_input().strip().split())
    adj = [[] for _ in xrange(N)]
    for _ in xrange(N-1):
        A, B = map(lambda x: int(x)-1, raw_input().strip().split())
        adj[A].append(B)
        adj[B].append(A)

    return dfs(adj, C, -1, 0)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, gold_mine_chapter_1())
