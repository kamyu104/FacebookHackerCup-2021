# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Final Round - Problem D. Vacation
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/D
#
# Time:  O(NlogN)
# Space: O(N)
#

def iter_dfs(C, adj, root):
    dp = [None]*len(adj)
    stk = [(1, root, -1)]
    while stk:
        step, u, p = stk.pop()
        if step == 1:
            stk.append((2, u, p))
            for v in adj[u]:
                if v == p:
                    continue
                stk.append((1, v, u))
        elif step == 2:
            cnt, l = max([dp[v] for v in adj[u] if v != p] or [(0, u)])
            dp[u] = (cnt+C[u], l)
    return dp

def vacation():
    N, K = map(int, raw_input().strip().split())
    C = map(int, raw_input().strip().split())
    P = map(lambda x: int(x)-1, raw_input().strip().split())
    adj = [[] for _ in xrange(N)]
    for v, u in enumerate(P, 1):
        adj[u].append(v)
        adj[v].append(u)
    root = iter_dfs(C, adj, 0)[0][1]
    dp = iter_dfs(C, adj, root)
    dp.sort(reverse=True)
    lookup = [False]*N
    curr = leaf_cnt = 0
    for cnt, l in dp:
        if lookup[l]:
            continue
        lookup[l] = True
        leaf_cnt += 1
        curr += cnt
        if curr >= K:
            return leaf_cnt//2
    return -1

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, vacation())
