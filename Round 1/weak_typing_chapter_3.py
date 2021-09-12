# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 1 - Problem A3. Weak Typing - Chapter 3
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-1/problems/A3
#
# Time:  O(N)
# Space: O(1)
#

from itertools import izip

def matrix_mult(A, B):
    ZB = zip(*B)
    return [[sum(a*b % MOD for a, b in izip(row, col)) % MOD for col in ZB] for row in A]

def identity_matrix(N):
    return [[int(i == j) for j in xrange(N)] for i in xrange(N)]

def solution():
    N = input()
    W = raw_input().strip()

    result = identity_matrix(6)
    for c in W:
        result = matrix_mult(result, T[c] if c != '.' else result)
    return matrix_mult([[0, 0, 0, 0, 0, 1]], result)[0][0]

# state: [total, per_step, os, unknowns, xs, 1]
T = {
     'O': [[1, 0, 0, 0, 0, 0],
           [1, 1, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0],
           [0, 0, 1, 0, 0, 0],
           [1, 1, 1, 0, 0, 0],
           [0, 0, 1, 0, 0, 1]],
     'F': [[1, 0, 0, 0, 0, 0],
           [1, 1, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0],
           [0, 0, 0, 1, 0, 0],
           [0, 0, 0, 0, 1, 0],
           [0, 0, 0, 1, 0, 1]],
     'X': [[1, 0, 0, 0, 0, 0],
           [1, 1, 0, 0, 0, 0],
           [1, 1, 0, 0, 1, 0],
           [0, 0, 0, 0, 1, 0],
           [0, 0, 0, 0, 1, 0],
           [0, 0, 0, 0, 1, 1]]
    }
MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, solution())
