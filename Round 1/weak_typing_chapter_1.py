# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 1 - Problem A1. Weak Typing - Chapter 1
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-1/problems/A1
#
# Time:  O(N)
# Space: O(1)
#

def weak_typing_chapter_1():
    N = input()
    W = raw_input().strip()

    result, prev = 0, -1
    for i, c in enumerate(W):
        if c == 'F':
            continue
        if prev != -1 and W[prev] != c:
            result += 1
        prev = i
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, weak_typing_chapter_1())
