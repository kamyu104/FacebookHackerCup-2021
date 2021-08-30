# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Qualification Round - Problem A1. Consistency - Chapter 1
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/qualification-round/problems/A1
#
# Time:  O(|S|)
# Space: O(1)
#

from collections import Counter

def time_to_replace(S, cnts, target, check):  # Time: O(|S|)
    max_cnt = 0
    for k, v in cnts.iteritems():
        if not check(k):
            continue
        if v > max_cnt:
            max_cnt, target = v, k
    return sum((2 if check(c) else 1) for c in S if c != target)

def consistency_chapter_1():
    S = raw_input().strip()

    cnts = Counter(S)
    return min(time_to_replace(S, cnts, 'A', lambda x: x in VOWELS),
               time_to_replace(S, cnts, 'B', lambda x: x not in VOWELS))

VOWELS = {'A', 'E', 'I', 'O', 'U'}
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, consistency_chapter_1())
