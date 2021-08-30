# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Qualification Round - Problem C2. Gold Mine - Chapter 2
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/qualification-round/problems/C2
#
# Time:  O(N * K^2)
# Space: O(N * K)
#

# merged_dp[k][o][c] = max. value after merging children of current node,
# with k new paths present,
# and with a free path connecting to i's parent if o=1,
# and with at least one child connected if c=1
def merge_dp(K, merged_dp, dp):  # Time: O(K^2)
    new_merged_dp = [[[-1]*2 for _ in xrange(2)] for _ in xrange(K+1)]
    for k1 in xrange(K+1):
        for o in xrange(2):
            for c in xrange(2):
                if merged_dp[k1][o][c] == -1:
                    continue
                for k2 in xrange(K+1-k1):
                    if dp[k2][1] >= 0 and k1+k2+(1-o) <= K:  # connect to child
                        new_merged_dp[k1+k2+(1-o)][1-o][1] = max(new_merged_dp[k1+k2+(1-o)][1-o][1], merged_dp[k1][o][c]+dp[k2][1])
                    if dp[k2][0] >= 0:  # don't connect to child
                        new_merged_dp[k1+k2][o][c] = max(new_merged_dp[k1+k2][o][c], merged_dp[k1][o][c]+dp[k2][0])
    return new_merged_dp

# dp[i][k][o] = max. value in i's subtree,
# with k new paths present,
# and with a free path connecting to i's parent if o=1
def combine_dp_i(C, K, i, merged_dp):  # Time: O(K)
    dp_i = [[-1]*2 for _ in xrange(K+1)]
    for new_o in xrange(2):
        for k in xrange(K+1):
            for o in xrange(2):
                for c in xrange(2):
                    if not i and not c:  # root must connect to at least one child
                        continue
                    if merged_dp[k][o][c] == -1:
                        continue
                    f = int(new_o and o)  # free path ongoing from parent
                    dp_i[k-f][new_o] = max(dp_i[k-f][new_o], merged_dp[k][o][c]+(C[i] if new_o or c else 0))
    return dp_i

def dfs(adj, C, K, parent, i, dp):
    merged_dp = [[[-1]*2 for _ in xrange(2)] for _ in xrange(K+1)]
    merged_dp[0][0][0] = 0
    for child in adj[i]:
        if child == parent:
            continue
        dfs(adj, C, K, i, child, dp)
        merged_dp = merge_dp(K, merged_dp, dp[child])
    dp[i] = combine_dp_i(C, K, i, merged_dp)

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
