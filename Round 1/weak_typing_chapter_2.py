# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 1 - Problem A2. Weak Typing - Chapter 2
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-1/problems/A2
#
# Time:  O(N)
# Space: O(1)
#

def addmod(a, b):
    return (a+b)%MOD

def weak_typing_chapter_2():
    N = input()
    W = raw_input().strip()

    result, accu, prev = 0, 0, -1
    for i, c in enumerate(W):
        if c == 'F':
            result = addmod(result, accu)
            continue
        if prev != -1 and W[prev] != c:
            accu = addmod(accu, prev+1)
        result = addmod(result, accu)
        prev = i
    return result

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, weak_typing_chapter_2())
