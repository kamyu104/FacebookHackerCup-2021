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
    C = [addmod(addmod(addmod(A[TOTAL], B[TOTAL]), mulmod(A[TOTAL_LEFT], B[LEN])), mulmod(A[LEN], B[TOTAL_RIGHT])),
         addmod(A[LEN], B[LEN]),
         addmod(A[ACCU], B[ACCU]),
         addmod(addmod(A[TOTAL_LEFT], B[TOTAL_LEFT]), mulmod(A[LEN], B[ACCU])),
         addmod(addmod(A[TOTAL_RIGHT], B[TOTAL_RIGHT]), mulmod(A[ACCU], B[LEN])),
         [addmod(A[LEN], B[FIRST][0]), B[FIRST][1]] if A[FIRST][0] == -1 and B[FIRST][0] != -1 else A[FIRST][:],
         [addmod(A[LEN], B[LAST][0]), B[LAST][1]] if B[LAST][0] != -1 else A[LAST][:]]
    if A[LAST][0] != -1 and B[FIRST][0] != -1 and A[LAST][1] != B[FIRST][1]:
        C[ACCU] = addmod(C[ACCU], 1)
        left, right = addmod(A[LAST][0], 1), submod(B[LEN], B[FIRST][0])
        C[TOTAL_LEFT] = addmod(C[TOTAL_LEFT], left)
        C[TOTAL_RIGHT] = addmod(C[TOTAL_RIGHT], right)
        C[TOTAL] = addmod(C[TOTAL], mulmod(left, right))
    return C

def weak_typing_chapter_3():
    N = input()
    W = raw_input().strip()

    result = [0, 0, 0, 0, 0, [-1, '-'], [-1, '-']]
    for c in W:
        if c == '.':
            result = merge(result, result)
        elif c == 'F':
            result = merge(result, [0, 1, 0, 0, 0, [-1, '-'], [-1, '-']])
        else:
            result = merge(result, [0, 1, 0, 0, 0, [0, c], [0, c]])
    return result[TOTAL]

MOD = 10**9+7
TOTAL, LEN, ACCU, TOTAL_LEFT, TOTAL_RIGHT, FIRST, LAST = range(7)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, weak_typing_chapter_3())
