# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Qualification Round - Problem A1. Consistency - Chapter 1
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/qualification-round/problems/A1
#
# Time:  O(|S|)
# Space: O(1)
#

from string import ascii_uppercase
from collections import defaultdict

def time_to_replace(S, dist, target):  # Time: O(|S|)
    return sum(dist[c][target] for c in S)

def consistency_chapter_1():
    S = raw_input().strip()

    dist = defaultdict(lambda:defaultdict(lambda: float("inf")))
    for a in ascii_uppercase:
        for b in ascii_uppercase:
            if a == b:
                dist[a][b] = 0
            else:
                dist[a][b] = 2 if (a in VOWELS) == (b in VOWELS) else 1
    result = min(time_to_replace(S, dist, target) for target in ascii_uppercase)
    return result if result != float("inf") else -1

VOWELS = {'A', 'E', 'I', 'O', 'U'}
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, consistency_chapter_1())
