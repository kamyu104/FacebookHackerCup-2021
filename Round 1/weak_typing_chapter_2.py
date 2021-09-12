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

    result = accu = os = xs = unknowns = 0
    for c in W:
        if c == 'F':
            unknowns = addmod(unknowns, 1)
        elif c == 'O':
            accu = addmod(accu, xs)
            os = addmod(addmod(addmod(os, xs),  unknowns), 1)
            xs = unknowns = 0
        elif c == 'X':
            accu = addmod(accu, os)
            xs = addmod(addmod(addmod(os, xs),  unknowns), 1)
            os = unknowns = 0
        result = addmod(result, accu)
    return result

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, weak_typing_chapter_2())
