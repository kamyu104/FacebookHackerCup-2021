import Tkinter as tk
from itertools import izip

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

def cross(A, B, C, D):
    return ccw(A,C,D) * ccw(B,C,D) < 0 and ccw(A,B,C) * ccw(A,B,D) < 0

class MainWindow:
    # radius of drawn points on canvas
    RADIUS = 3

    # flag to lock the canvas when drawn
    LOCK_FLAG = False

    points = set()
    
    def __init__(self, master):
        self.master = master
        self.master.title("Voronoi Diagram by Fortune's Algorithm O(NlogN)")
        self.frmMain = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        self.frmMain.pack(fill=tk.BOTH, expand=1)

        self.w = tk.Canvas(self.frmMain, width=XR, height=YR)
        self.w.config(background='white')
        self.w.bind('<Button-1>', self.onClick)
        self.w.pack()       

        self.frmButton = tk.Frame(self.master)
        self.frmButton.pack()
        
        self.btnClear = tk.Button(self.frmButton, text='Clear', width=50, command=self.onClickClear)
        self.btnClear.pack(side=tk.LEFT)
                
    def onClickClear(self):
        self.points = set()
        self.w.delete(tk.ALL)

    def onClick(self, event):
        if (event.x, event.y) in self.points:
            return
        self.points.add((event.x, event.y))
        self.paint()

    def paint(self):
        def get(points, p1, p2):
            return (points[p1][0], points[p1][1], points[p2][0], points[p2][1])

        def inside_rect_incl(points, p1, p2):
            if p1 == -1 or p2 == -1:
                return False
            p1, p2 = points[p1], points[p2]
            return (-EPS <= min(p1[0], p2[0]) and max(p1[0], p2[0]) <= XR+EPS and
                    -EPS <= min(p1[1], p2[1]) and max(p1[1], p2[1]) <= YR+EPS)

        def on_border(p):
            return abs(p[0]-0) <= EPS or abs(p[0]-XR) <= EPS or abs(p[1]-0) <= EPS or abs(p[1]-YR) <= EPS

        def is_border_segment(a, b):
            segments = [(0, 0), (XR, 0), (XR, YR), (0, YR)]
            for i in xrange(len(segments)):
                c, d = segments[i], segments[(i+1)%len(segments)]
                if abs(ccw(a, c, d)) < EPS and abs(ccw(b, c, d)) < EPS:
                    return True
            return False

        self.w.delete(tk.ALL)
        points = []
        for X, Y in self.points:
            points.append((X, Y))
            points.append((-X, Y))
            points.append((X, -Y))
            points.append((2*XR - X, Y))
            points.append((X, 2*YR - Y))
        points = list(set(points))
        vertex, edge, area = VoronoiDiagram(points)  # points should be distinct
        edge_lines = [get(vertex, e1, e2) for e1, e2 in edge if inside_rect_incl(vertex, e1, e2) and not is_border_segment(vertex[e1], vertex[e2])]
        perpendicular_lines = [get(points, p1, p2) for i, (p1, p2) in enumerate(area) if inside_rect_incl(vertex, edge[i][0], edge[i][1]) and cross(vertex[edge[i][0]], vertex[edge[i][1]], points[p1], points[p2])]
        triangular_lines = []
        for (p1, p2), (e1, e2) in izip(area, edge):
            if not inside_rect_incl(vertex, e1, e2):
                continue
            for x in p1, p2:
                for y in e1, e2:
                    a, b = points[x]
                    c, d = vertex[y]
                    triangular_lines.append((a, b, c, d))
        #self.drawLinesOnCanvas(triangular_lines, color='red', dash=(5,2), width=0.5)
        #self.drawLinesOnCanvas(perpendicular_lines, color='black', dash=(5,2), width=0.5)
        self.drawLinesOnCanvas(edge_lines, color='blue')
        self.drawPointsOnCanvas([v for v in vertex if not on_border(v)], color="green")
        self.drawPointsOnCanvas(points, color="black")
        print points

    def drawPointsOnCanvas(self, vertex, color):
        for x, y in vertex:
            self.w.create_oval(x-self.RADIUS, y-self.RADIUS, x+self.RADIUS, y+self.RADIUS, fill=color, outline=color)

    def drawLinesOnCanvas(self, lines, color='black', dash=None, width=1.5):
        for l in lines:
            self.w.create_line(l[0], l[1], l[2], l[3], fill=color, width=width, dash=dash)

def main(): 
    root = tk.Tk()
    app = MainWindow(root)
    root.resizable(0, 0)
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    root.mainloop()

INF = float("inf")
EPS = 1e-9
XR = YR = 500
if __name__ == '__main__':
    main()
