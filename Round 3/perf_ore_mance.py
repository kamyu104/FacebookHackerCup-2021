# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 3 - Problem C. Perf-ore-mance
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/C
#
# Time:  O(N * K^2)
# Space: O(N * K)
#

from functools import partial

def iter_dfs(N, K, adj):
    def divide(i):
        stk.append(partial(postprocess, i))
        for child in reversed(adj[i]):
            stk.append(partial(divide, child))

    def postprocess(i):
        dp2 = [[-INF]*2 for _ in xrange(K+1)]  # dp[c][b]: max number of determined nodes by using current node's subtree with c children, b = 1 if only if one of which has subtree size 2 and the others of which have subtree sizes either 1 or > K
        dp2[0][0] = 0
        for child in adj[i]:
            for c in reversed(xrange(len(dp2))):
                for b in reversed(xrange(2)):
                    if not b:
                        dp2[min(c+1, K)][1] = max(dp2[min(c+1, K)][1], dp2[c][b]+dp[child][2])
                    dp2[min(c+1, K)][b] = max(dp2[min(c+1, K)][b], dp2[c][b]+max(dp[child][1], dp[child][K+1]))

        dp3 = [-INF]*((K+1)+1)  # dp[s]: max number of determined nodes by using current node's subtree with size s
        dp3[1] = 0
        for child in adj[i]:
            for s1 in reversed(xrange(len(dp3))):
                cnt = dp3[s1]
                for s2 in xrange(len(dp[child])):
                    dp3[min(s1+s2, K+1)] = max(dp3[min(s1+s2, K+1)], cnt+dp[child][s2])

        # dp[i] merges all above dp[child], dp2, dp3
        for child in adj[i]:
            dp[i][K+1] = max(dp[i][K+1], dp[child][K+1]+1)  # case child: node i has 1 child which has subtree size > K
        dp[i][K+1] = max(dp[i][K+1], dp2[K][1]+1)  # case grandchild: node i has K children, one of which has subtree size 2 and the others of which have subtree sizes either 1 or > K
        for s1 in xrange(len(dp3)):
            dp[i][s1] = max(dp[i][s1], dp3[s1])  # case neither: no new determined nodes

    dp = [[-INF]*(K+2) for _ in xrange(N)]  # dp[i][s]: max number of determined nodes by using i's subtree with size s
    stk = [partial(divide, 0)]
    while stk:
        stk.pop()()
    return max(dp[0])

def perf_ore_mance():
    N, K = map(int, raw_input().strip().split())
    adj = [[] for _ in xrange(N)]
    for i, M in enumerate(map(int, raw_input().strip().split()), 1):
        adj[M-1].append(i)

    return iter_dfs(N, K, adj)

INF = float("inf")
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, perf_ore_mance())
