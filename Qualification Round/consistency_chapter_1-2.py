# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Qualification Round - Problem A1. Consistency - Chapter 1
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/qualification-round/problems/A1
#
# Time:  O(|S|)
# Space: O(1)
#

from string import ascii_uppercase

def time_to_replace(S, target):  # Time: O(|S|)
    return sum(2 if (c in VOWELS) == (target in VOWELS) else 1 for c in S if c != target)

def consistency_chapter_1():
    S = raw_input().strip()

    result = min(time_to_replace(S, target) for target in ascii_uppercase)
    return result if result != float("inf") else -1

VOWELS = {'A', 'E', 'I', 'O', 'U'}
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, consistency_chapter_1())
