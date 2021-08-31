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
    target = max([kvp for kvp in cnts.iteritems() if check(kvp[0])] or [(target, 0)], key=lambda x: x[1])[0]
    return sum((2 if check(c) else 1) for c in S if c != target)

def consistency_chapter_1():
    S = raw_input().strip()

    cnts = Counter(S)
    return min(time_to_replace(S, cnts, 'A', lambda x: x in VOWELS),
               time_to_replace(S, cnts, 'B', lambda x: x not in VOWELS))

VOWELS = {'A', 'E', 'I', 'O', 'U'}
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, consistency_chapter_1())
