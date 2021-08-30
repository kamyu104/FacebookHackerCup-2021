# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Qualification Round - Problem C2. Gold Mine - Chapter 2
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/qualification-round/problems/C2
#
# Time:  O(N * K^2)
# Space: O(N * K)
#

# merged_dp[k][p][c] = max value after merging children of current node,
# with k new paths present,
# and with a free path connecting to i's parent if p=1,
# and with at least one child connected if c=1
def merge_dp(adj, K, parent, i, dp):  # Time: O(K^2), Space: O(K)
    merged_dp = [[[-1]*2 for _ in xrange(2)] for _ in xrange(K+1)]
    merged_dp[0][0][0] = 0
    for child in adj[i]:
        if child == parent:
            continue
        new_merged_dp = [[[-1]*2 for _ in xrange(2)] for _ in xrange(K+1)]
        for k1 in xrange(K+1):
            for p in xrange(2):
                for c in xrange(2):
                    if merged_dp[k1][p][c] == -1:
                        continue
                    for k2 in xrange(K+1-k1):
                        if dp[child][k2][1] >= 0 and k1+k2+(1-p) <= K:  # connect to child
                            new_merged_dp[k1+k2+(1-p)][1-p][1] = max(new_merged_dp[k1+k2+(1-p)][1-p][1], merged_dp[k1][p][c]+dp[child][k2][1])
                        if dp[child][k2][0] >= 0:  # don't connect to child
                            new_merged_dp[k1+k2][p][c] = max(new_merged_dp[k1+k2][p][c], merged_dp[k1][p][c]+dp[child][k2][0])
        merged_dp = new_merged_dp
    return merged_dp

# dp[i][k][p] = max value in i's subtree,
# with k new paths present,
# and with a free path connecting to i's parent if p=1
def find_dp_i(K, merged_dp, i, v):  # Time: O(K), Space: O(K)
    dp_i = [[-1]*2 for _ in xrange(K+1)]
    for new_p in xrange(2):
        for k in xrange(K+1):
            for p in xrange(2):
                for c in xrange(2):
                    if not i and not c:  # root must connect to at least one child
                        continue
                    if merged_dp[k][p][c] == -1:
                        continue
                    f = int(new_p and p)  # free path ongoing from parent
                    dp_i[k-f][new_p] = max(dp_i[k-f][new_p], merged_dp[k][p][c]+(v if new_p or c else 0))
    return dp_i

def dfs(adj, C, K, parent, i, dp):
    for child in adj[i]:
        if child == parent:
            continue
        dfs(adj, C, K, i, child, dp)
    dp[i] = find_dp_i(K, merge_dp(adj, K, parent, i, dp), i, C[i])

def gold_mine_chapter_2():
    N, K = map(int, raw_input().strip().split())
    C = map(int, raw_input().strip().split())
    adj = [[] for _ in xrange(N)]
    for _ in xrange(N-1):
        A, B = map(lambda x: int(x)-1, raw_input().strip().split())
        adj[A].append(B)
        adj[B].append(A)

    dp = {}
    dfs(adj, C, K, -1, 0, dp)
    return max(max(dp[0][k][0] for k in xrange(K+1)), C[0])

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, gold_mine_chapter_2())
