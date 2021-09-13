# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 1 - Problem A3. Weak Typing - Chapter 3
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-1/problems/A3
#
# Time:  O(N)
# Space: O(1)
#
# faster but harder to write
#

def addmod(a, b):
    return (a+b)%MOD

def submod(a, b):
    return (a-b)%MOD

def mulmod(a, b):
    return (a*b)%MOD

def merge(A, B):
    C = [addmod(addmod(addmod(A[RES], B[RES]), mulmod(A[LEFT_SUM], B[LEN])), mulmod(A[LEN], B[RIGHT_SUM])),
         addmod(A[LEN], B[LEN]),
         addmod(A[SWITCH], B[SWITCH]),
         addmod(addmod(A[LEFT_SUM], B[LEFT_SUM]), mulmod(A[LEN], B[SWITCH])),
         addmod(addmod(A[RIGHT_SUM], B[RIGHT_SUM]), mulmod(A[SWITCH], B[LEN])),
         [addmod(A[LEN], B[FIRST][0]), B[FIRST][1]] if A[FIRST][0] == -1 and B[FIRST][0] != -1 else A[FIRST][:],
         [addmod(A[LEN], B[LAST][0]), B[LAST][1]] if B[LAST][0] != -1 else A[LAST][:]]
    if A[LAST][0] != -1 and B[FIRST][0] != -1 and A[LAST][1] != B[FIRST][1]:
        C[SWITCH] = addmod(C[SWITCH], 1)
        left, right = addmod(A[LAST][0], 1), submod(B[LEN], B[FIRST][0])
        C[LEFT_SUM] = addmod(C[LEFT_SUM], left)
        C[RIGHT_SUM] = addmod(C[RIGHT_SUM], right)
        C[RES] = addmod(C[RES], mulmod(left, right))
    return C

def weak_typing_chapter_3():
    N = input()
    W = raw_input().strip()

    result = [0, 0, 0, 0, 0, [-1, '-'], [-1, '-']]
    for c in W:
        result = merge(result, result if c == '.' else [0, 1, 0, 0, 0, [0 if c != 'F' else -1, c], [0 if c != 'F' else -1, c]])
    return result[RES]

MOD = 10**9+7
RES, LEN, SWITCH, LEFT_SUM, RIGHT_SUM, FIRST, LAST = range(7)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, weak_typing_chapter_3())
