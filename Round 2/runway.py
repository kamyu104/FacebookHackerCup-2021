# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 2 - Problem A. Runway
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/A
#
# Time:  O(N * M)
# Space: O(M)
#

from collections import Counter

def runway():
    N, M = map(int, raw_input().strip().split())
    result = 0
    prev = unchanged_cnts = Counter(map(int, raw_input().strip().split()))
    for _ in xrange(N):
        curr = Counter(map(int, raw_input().strip().split()))
        result += sum(cnt-prev[s] if s in prev else cnt for s, cnt in curr.iteritems() if s not in prev or cnt-prev[s] > 0)
        for s in unchanged_cnts.keys():
            changed_cnt = prev[s]-curr[s] if s in curr else prev[s]
            if changed_cnt <= 0:
                continue
            free_cnt = min(unchanged_cnts[s], changed_cnt)
            unchanged_cnts[s] -= free_cnt
            result -= free_cnt
            if not unchanged_cnts[s]:
                del unchanged_cnts[s]
        prev = curr
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, runway())
