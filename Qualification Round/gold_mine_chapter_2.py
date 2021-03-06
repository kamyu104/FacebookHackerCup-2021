# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Qualification Round - Problem C2. Gold Mine - Chapter 2
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/qualification-round/problems/C2
#
# Time:  O(N * K^2)
# Space: O(N * K)
#

# merged_dp[k][c][p] = max value after merging children of current node,
# with k new paths present,
# and with at least one child connected if c=1,
# and with a path connecting some node of i's subtree to node i available for use if p=1
def merge_dp(K, merged_dp, dp):  # Time: O(K^2), Space: O(K)
    new_merged_dp = [[[-1]*2 for _ in xrange(2)] for _ in xrange(K+1)]
    for k1 in xrange(K+1):
        for c in xrange(2):
            for p in xrange(2 if c else 1):
                if merged_dp[k1][c][p] == -1:
                    continue
                for k2 in xrange(K+1-k1):
                    if dp[k2][1] >= 0 and k1+k2+(1-p) <= K:  # connect to child
                        new_merged_dp[k1+k2+(1-p)][1][1-p] = max(new_merged_dp[k1+k2+(1-p)][1][1-p], merged_dp[k1][c][p]+dp[k2][1])
                    if dp[k2][0] >= 0:  # don't connect to child
                        new_merged_dp[k1+k2][c][p] = max(new_merged_dp[k1+k2][c][p], merged_dp[k1][c][p]+dp[k2][0])
    return new_merged_dp

# dp_i[k][o] = max value in i's subtree,
# with k new paths present,
# and with a free path ongoing from i's parent to node i if o=1
def find_dp_i(K, merged_dp, i, v):  # Time: O(K), Space: O(K)
    dp_i = [[-1]*2 for _ in xrange(K+1)]
    for o in xrange(2):
        for k in xrange(K+1):
            for c in xrange(2):
                for p in xrange(2 if c else 1):
                    if not i and not c:  # root must connect to at least one child
                        continue
                    if merged_dp[k][c][p] == -1:
                        continue
                    f = int(o and p)  # free path ongoing from parent
                    dp_i[k-f][o] = max(dp_i[k-f][o], merged_dp[k][c][p]+(v if o or c else 0))
    return dp_i

def dfs(adj, C, K, parent, i):
    merged_dp = [[[-1]*2 for _ in xrange(2)] for _ in xrange(K+1)]
    merged_dp[0][0][0] = 0
    for child in adj[i]:
        if child == parent:
            continue
        merged_dp = merge_dp(K, merged_dp, dfs(adj, C, K, i, child))
    return find_dp_i(K, merged_dp, i, C[i])

def gold_mine_chapter_2():
    N, K = map(int, raw_input().strip().split())
    C = map(int, raw_input().strip().split())
    adj = [[] for _ in xrange(N)]
    for _ in xrange(N-1):
        A, B = map(lambda x: int(x)-1, raw_input().strip().split())
        adj[A].append(B)
        adj[B].append(A)

    return max(max(dp_0_k[0] for dp_0_k in dfs(adj, C, K, -1, 0)), C[0])

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, gold_mine_chapter_2())
