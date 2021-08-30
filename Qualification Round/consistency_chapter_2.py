# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Qualification Round - Problem A2. Consistency - Chapter 2
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/qualification-round/problems/A2
#
# Time:  O(|S|)
# Space: O(1)
#

def floydWarshall(graph):  # Time: O(n^3) = O(26^3) = O(1), Space: O(n^2) = O(26^2) = O(1)
    dist = [row[:] for row in graph]
    for k in xrange(len(dist[0])):
        for i in xrange(len(dist)):
            for j in xrange((len(dist[i]))):
                dist[i][j] = min(dist[i][j], dist[i][k]+dist[k][j])
    return dist

def time_to_replace(S, dist, target):  # Time: O(|S|)
    return sum(dist[ord(c)-ord('A')][target] for c in S)

def consistency_chapter_2():
    S = raw_input().strip()
    K = input()
    graph = [[(float("inf") if i != j else 0) for j in xrange(26)] for i in xrange(26)]
    for _ in xrange(K):
        A, B = list(raw_input().strip())
        graph[ord(A)-ord('A')][ord(B)-ord('A')] = 1

    dist = floydWarshall(graph)
    result = min(time_to_replace(S, dist, target) for target in xrange(26))
    return result if result != float("inf") else -1

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, consistency_chapter_2())
