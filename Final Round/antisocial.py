# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Final Round - Problem E. Antisocial
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/E
#
# Time:  O(NlogN), TLE in both PyPy2 and Python2
# Space: O(N)
#

from heapq import heappush, heappop

# Template translated from:
# https://github.com/zigui-ps/VoronoiDiagram/blob/master/VoronoiDiagram.cpp
def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def mul(b, a):
    return (b * a[0], b * a[1])

def inner_product(a, b):
    return a[0] * b[0] + a[1] * b[1]

def outer_product(a, b):
    return a[0] * b[1] - a[1] * b[0]

def size(p):
    return (p[0]*p[0] + p[1]*p[1])**0.5

def sz2(p):
    return p[0]*p[0] + p[1]*p[1]

def r90(p):
    return (-p[1], p[0])

def dcmp(x):
    return -1 if x < -EPS else 1 if x > EPS else 0

def line_intersect(a, b, u, v):
    return add(u, mul((outer_product(sub(a, u), b) / outer_product(v, b)), v))

def get_circumcenter(p0, p1, p2):
    return line_intersect(mul(0.5, add(p0, p1)), r90(sub(p0, p1)), mul(0.5, add(p1, p2)), r90(sub(p1, p2)))

# https://www.youtube.com/watch?v=h_vvP4ah6Ck
def parabola_intersect(left, right, sweepline):
    if dcmp(left[1] - right[1]) == 0:
        return (left[0] + right[0]) / 2.0

    sign = -1.0 if left[1] < right[1] else 1.0
    v = line_intersect(left, sub(right, left), (0.0, sweepline), (1.0, 0.0))
    d1 = sz2(sub(mul(0.5, add(left, right)), v))
    d2 = sz2(mul(0.5, sub(left, right)))
    return v[0] + sign * ((max(0.0, d1 - d2))**0.5)

class Node(object):
    def __init__(self, point, idx):
        self.point = point
        self.idx = idx
        self.end = 0
        self.link = [None]*2
        self.par = self.prv = self.nxt = None

class Beachline(object):
    def __init__(self):
        self.sweepline = -INF
        self.root = None

    def direction(self, x):
        return x.par.link[0] != x

    def rotate(self, n):
        p = n.par
        d = self.direction(n)
        p.link[d] = n.link[not d]
        if n.link[not d]:
            n.link[not d].par = p
        n.par = p.par
        if p.par:
            p.par.link[self.direction(p)] = n
        n.link[not d] = p
        p.par = n

    def splay(self, x, f=None):
        while x.par != f:
            if x.par.par == f:
                pass
            elif self.direction(x) == self.direction(x.par):
                self.rotate(x.par)
            else:
                self.rotate(x)
            self.rotate(x)
        if f is None:
            self.root = x

    def insert(self, n, p, d):
        self.splay(p)
        c = p.link[d]
        n.link[d] = c
        if c:
            c.par = n
        p.link[d] = n
        n.par = p
        prv = p.prv if not d else p
        nxt = p if not d else p.nxt
        n.prv = prv
        if prv:
            prv.nxt = n
        n.nxt = nxt
        if nxt:
            nxt.prv = n

    def erase(self, n):
        prv, nxt = n.prv, n.nxt
        if (not prv) and (not nxt):
            if n == self.root:
                self.root = None
            return
        n.prv = None
        if prv:
            prv.nxt = nxt
        n.nxt = None
        if nxt:
            nxt.prv = prv
        self.splay(n)
        if not nxt:
            self.root.par = None
            n.link[0] = None
            self.root = prv
        else:
            self.splay(nxt, n)
            c = n.link[0]
            nxt.link[0] = c
            c.par = nxt
            n.link[0] = None
            n.link[1] = None
            nxt.par = None
            self.root = nxt

    def get_event(self, cur, next_sweep):
        if (not cur.prv) or (not cur.nxt):
            return False
        u = r90(sub(cur.point, cur.prv.point))
        v = r90(sub(cur.nxt.point, cur.point))
        if dcmp(outer_product(u, v)) != 1:
            return False
        p = get_circumcenter(cur.point, cur.prv.point, cur.nxt.point)
        next_sweep[0] = p[1] + size(sub(p, cur.point))
        return True

    def find_beachline(self, x):
        cur = self.root
        while cur:
            left = parabola_intersect(cur.prv.point, cur.point, self.sweepline) if cur.prv else -INF
            right = parabola_intersect(cur.point, cur.nxt.point, self.sweepline) if cur.nxt else INF
            if left <= x <= right:
                self.splay(cur)
                return cur
            cur = cur.link[x > right]
        return None

def new_node(arr, point, idx):
    arr.append(Node(point, idx))
    return arr[-1]

def VoronoiDiagram(points):
    vertex, edge, area = [[] for _ in xrange(3)]
    bl = Beachline()
    events = []
    def add_edge(u, v, a, b, c1, c2):
        if c1:
            c1.end = len(edge)*2
        if c2:
            c2.end = len(edge)*2 + 1
        edge.append([u, v])
        area.append((a, b))

    def write_edge(idx, v):
        edge[idx//2][idx%2] = v

    def add_event(cur):
        nxt = [0.0]
        if bl.get_event(cur, nxt):
            heappush(events, (nxt[0], 1, -1, cur.prv.idx, cur.nxt.idx, cur))

    n = len(points)
    arr = []
    points.sort(key=lambda x: (x[1], x[0]))
    tmp = bl.root = new_node(arr, points[0], 0)
    for i in xrange(1, n):
        if dcmp(points[i][1] - points[0][1]) == 0:
            add_edge(-1, -1, i-1, i, 0, tmp)
            t2 = new_node(arr, points[i], i)
            bl.insert(t2, tmp, 1)
            tmp = t2
        else:
            heappush(events, (points[i][1], 0, i, -1, -1, None))
    while events:
        q_sweep, q_type, q_idx, q_prv, q_nxt, q_cur = heappop(events)
        v, idx = len(vertex), q_idx
        bl.sweepline = q_sweep
        if q_type == 0:
            point = points[idx]
            cur = bl.find_beachline(point[0])
            site = new_node(arr, point, idx)
            bl.insert(site, cur, 0)
            prv = new_node(arr, cur.point, cur.idx)
            bl.insert(prv, site, 0)
            add_edge(-1, -1, cur.idx, idx, site, prv)
            add_event(prv)
            add_event(cur)
        else:
            cur, prv, nxt = q_cur, q_cur.prv, q_cur.nxt
            if (not prv) or (not nxt) or (prv.idx != q_prv) or (nxt.idx != q_nxt):
                continue
            vertex.append(get_circumcenter(prv.point, nxt.point, cur.point))
            write_edge(prv.end, v)
            write_edge(cur.end, v)
            add_edge(v, -1, prv.idx, nxt.idx, 0, prv)
            bl.erase(cur)
            add_event(prv)
            add_event(nxt)
    return vertex, edge, area

def project_point_segment(a, b, c):
    r = inner_product(sub(b, a), sub(b, a))
    if abs(r) <= EPS:
        return a
    r = min(max(inner_product(sub(c, a), sub(b, a))/r, 0.0), 1.0)
    return add(a, mul(r, sub(b, a)))

def ccw(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def is_inside_segment_incl(t, a, b):
    return abs(ccw(t, a, b)) <= EPS and inner_product(sub(a, t), sub(t, b)) >= -EPS

def is_inside_triangle_incl(t, a, b, c):
    if is_inside_segment_incl(t, a, b) or is_inside_segment_incl(t, b, c) or is_inside_segment_incl(t, c, a):
        return True
    d1, d2, d3 = ccw(t, a, b), ccw(t, b, c), ccw(t, c, a)
    return (d1 > EPS and d2 > EPS and d3 > EPS) or (d1 < -EPS and d2 < -EPS and d3 < -EPS)

def process_voronoi_diagrams(XR, YR, key_points, P):
    vertex, edge, area = VoronoiDiagram(P)
    key_nodes = [-1]*2
    adj = [[] for _ in xrange(len(vertex))]
    result = INF
    for i in xrange(len(area)):
        e1, e2 = edge[i]
        if e1 == -1 or e2 == -1:
            continue  # infinite edge
        v1, v2 = vertex[e1], vertex[e2]
        if (min(v1[0], v2[0]) < -EPS or max(v1[0], v2[0]) > XR + EPS or
            min(v1[1], v2[1]) < -EPS or max(v1[1], v2[1]) > YR + EPS):
            continue  # edge outside rectangle
        pi1, pi2 = area[i]
        sites = [P[pi1], P[pi2]]
        d = size(sub(sites[0], project_point_segment(v1, v2, sites[0])))
        adj[e1].append((e2, d))
        adj[e2].append((e1, d))
        mid = mul(0.5, add(sites[0], sites[1]))
        for j, kp in enumerate(key_points):
            for p in sites:
                result = min(result, size(sub(kp, p)))
                # if kp is inside in both right triangles:
                # - kp is on (p, mid) perpendicular segment
                # - kp and mid are both outside of (p, v1, v2) triangle
                # => it is safe to choose either of v1, v2 since min(|p-v1|, |p-v2|) >= d
                # if kp is inside only one right triangle:
                # => it is safe to choose corresponding v since |p-v| >= d
                if is_inside_triangle_incl(kp, p, v1, mid):
                    key_nodes[j] = e1
                elif is_inside_triangle_incl(kp, p, mid, v2):
                    key_nodes[j] = e2
    return key_nodes, adj, result

def mst(key_nodes, adj, result):
    lookup = [False]*len(adj)
    max_heap = [(-result, key_nodes[0])]
    while max_heap:
        dist, u = heappop(max_heap)
        result = min(result, -dist)
        if u == key_nodes[1]:
            break
        if lookup[u]:
            continue
        lookup[u] = True
        for v, dist in adj[u]:
            if lookup[v]:
                continue
            heappush(max_heap, (-dist, v))
    return result

def antisocial():
    XR, YR = map(float, raw_input().strip().split())
    XA, YA, XB, YB = map(float, raw_input().strip().split())
    key_points = [(XA, YA), (XB, YB)]
    P = []
    for _ in xrange(input()):
        X, Y = map(float, raw_input().strip().split())
        P.append((X, Y))
        P.append((-X, Y))
        P.append((X, -Y))
        P.append((2*XR - X, Y))
        P.append((X, 2*YR - Y))
    key_nodes, adj, result = process_voronoi_diagrams(XR, YR, key_points, P)
    assert(key_nodes[0] >= 0 and key_nodes[1] >= 0)
    return mst(key_nodes, adj, result)

INF = float("inf")
EPS = 1e-9
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, antisocial())
