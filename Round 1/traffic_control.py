# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 1 - Problem B. Traffic Control
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-1/problems/B
#
# Time:  O(N * M)
# Space: O(1)
#

def traffic_control():
    N, M, A, B = map(int, raw_input().strip().split())

    if min(A, B) < (N+M-1):
        return "Impossible"
    result = [[1 for j in xrange(M)] for i in xrange(N)]
    result[0][0] += A-(N+M-1)
    result[0][-1] += B-(N+M-1)
    return "%s\n%s" % ("Possible", "\n".join(" ".join(map(str, row)) for row in result))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, traffic_control())
