// Copyright (c) 2021 kamyu. All rights reserved.

/*
 * Facebook Hacker Cup 2021 Final Round - Antisocial
 * https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/E
 *
 * Time:  O(NlogN)
 * Space: O(N)
 *
 */

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <cassert>
#include <cmath>

using namespace std;

// Template: https://github.com/zigui-ps/VoronoiDiagram/blob/master/VoronoiDiagram.cpp
typedef pair<int, int> pii;
typedef pair<double, double> pdd;

const double EPS = 1e-9;
int dcmp(double x){ return x < -EPS? -1 : x > EPS ? 1 : 0; }

double operator / (pdd a,    pdd b){ return a.first * b.second - a.second * b.first; }
pdd    operator * (double b, pdd a){ return pdd(b * a.first, b * a.second); }
pdd    operator + (pdd a,    pdd b){ return pdd(a.first + b.first, a.second + b.second); }
pdd    operator - (pdd a,    pdd b){ return pdd(a.first - b.first, a.second - b.second); }

double sq(double x){ return x*x; }
double size(pdd p){ return hypot(p.first, p.second); }
double sz2(pdd p){ return sq(p.first) + sq(p.second); }
pdd r90(pdd p){ return pdd(-p.second, p.first); }

pdd line_intersect(pdd a, pdd b, pdd u, pdd v){ return u + (((a-u)/b) / (v/b))*v; }
pdd get_circumcenter(pdd p0, pdd p1, pdd p2){
    return line_intersect(0.5 * (p0+p1), r90(p0-p1), 0.5 * (p1+p2), r90(p1-p2));
}

// https://www.youtube.com/watch?v=h_vvP4ah6Ck
double parabola_intersect(pdd left, pdd right, double sweepline){
    /*
    if(dcmp(left.second - right.second) == 0) return (left.first + right.first) / 2.0; /*/
    auto f2 = [](pdd left, pdd right, double sweepline){
        int sign = left.first < right.first ? 1 : -1;
        pdd m = 0.5 * (left+right);
        pdd v = line_intersect(m, r90(right-left), pdd(0, sweepline), pdd(1, 0));
        pdd w = line_intersect(m, r90(left-v), v, left-v);
        double l1 = size(v-w), l2 = sqrt(sq(sweepline-m.second) - sz2(m-w)), l3 = size(left-v);
        return v.first + (m.first - v.first) * l3 / (l1 + sign * l2);
    };
    if(fabs(left.second - right.second) < fabs(left.first - right.first) * EPS) return f2(left, right, sweepline);// */
    int sign = left.second < right.second ? -1 : 1;
    pdd v = line_intersect(left, right-left, pdd(0, sweepline), pdd(1, 0));
    double d1 = sz2(0.5 * (left+right) - v), d2 = sz2(0.5 * (left-right));
    return v.first + sign * sqrt(max(0.0, d1 - d2));
}

class Beachline{
    public:
        struct node{
            node(){}
            node(pdd point, int idx):point(point), idx(idx), end(0), 
                link{0, 0}, par(0), prv(0), nxt(0) {}
            pdd point; int idx; int end;
            node *link[2], *par, *prv, *nxt;
        };
        node *root;
        double sweepline;

        Beachline() : sweepline(-1e20), root(NULL){ }
        inline int dir(node *x){ return x->par->link[0] != x; }

        //     p        n          p            n
        //    / \      / \        / \          / \
        //   n   d => a   p   or a   n   =>   p   d
        //  / \          / \        / \      / \
        // a   b        b   d      c   d    a   c

        void rotate(node *n){
            node *p = n->par;         int d = dir(n);
            p->link[d] = n->link[!d]; if(n->link[!d]) n->link[!d]->par = p;
            n->par = p->par;          if(p->par) p->par->link[dir(p)] = n;
            n->link[!d] = p;          p->par = n;
        }

        void splay(node *x, node *f = NULL){
            while(x->par != f){
                if(x->par->par == f);
                else if(dir(x) == dir(x->par)) rotate(x->par);
                else rotate(x);
                rotate(x);
            }
            if(f == NULL) root = x;
        }

        void insert(node *n, node *p, int d){
            splay(p); node* c = p->link[d];
            n->link[d] = c; if(c) c->par = n;
            p->link[d] = n; n->par = p;

            node *prv = !d?p->prv:p, *nxt = !d?p:p->nxt;
            n->prv = prv;   if(prv) prv->nxt = n;
            n->nxt = nxt;   if(nxt) nxt->prv = n;
        }

        void erase(node* n){
            node *prv = n->prv, *nxt = n->nxt;
            if(!prv && !nxt){ if(n == root) root = NULL; return; }
            n->prv = NULL;   if(prv) prv->nxt = nxt;
            n->nxt = NULL;   if(nxt) nxt->prv = prv;
            splay(n);
            if(!nxt){
                root->par = NULL; n->link[0] = NULL;
                root = prv;
            }
            else{
                splay(nxt, n);     node* c = n->link[0];
                nxt->link[0] = c;  c->par = nxt;         n->link[0] = NULL;
                n->link[1] = NULL; nxt->par = NULL;
                root = nxt;
            }
        }
        bool get_event(node* cur, double &next_sweep){
            if(!cur->prv || !cur->nxt) return false;
            pdd u = r90(cur->point - cur->prv->point);
            pdd v = r90(cur->nxt->point - cur->point);
            if(dcmp(u/v) != 1) return false;
            pdd p = get_circumcenter(cur->point, cur->prv->point, cur->nxt->point);
            next_sweep = p.second + size(p - cur->point);
            return true;
        }
        node* find_beachline(double x){
            node* cur = root;
            while(cur){
                double left = cur->prv ? parabola_intersect(cur->prv->point, cur->point, sweepline) : -1e30;
                double right = cur->nxt ? parabola_intersect(cur->point, cur->nxt->point, sweepline) : 1e30;
                if(left <= x && x <= right){ splay(cur); return cur; }
                cur = cur->link[x > right];
            }
            return NULL;
        }
}; using BeachNode = Beachline::node;

static BeachNode* arr;
static int sz;
static BeachNode* new_node(pdd point, int idx){
    arr[sz] = BeachNode(point, idx);
    return arr + (sz++);
}

struct event{
    event(double sweep, int idx):type(0), sweep(sweep), idx(idx){}
    event(double sweep, BeachNode* cur):type(1), sweep(sweep), prv(cur->prv->idx), cur(cur), nxt(cur->nxt->idx){}
    int type, idx, prv, nxt;
    BeachNode* cur;
    double sweep;
    bool operator>(const event &l)const{ return sweep > l.sweep; }
};

void VoronoiDiagram(vector<pdd> &input, vector<pdd> &vertex, vector<pii> &edge, vector<pii> &area){
    Beachline beachline = Beachline();
    priority_queue<event, vector<event>, greater<event>> events;

    auto add_edge = [&](int u, int v, int a, int b, BeachNode* c1, BeachNode* c2){
        if(c1) c1->end = edge.size()*2;
        if(c2) c2->end = edge.size()*2 + 1;
        edge.emplace_back(u, v);
        area.emplace_back(a, b);
    };
    auto write_edge = [&](int idx, int v){ idx%2 == 0 ? edge[idx/2].first = v : edge[idx/2].second = v; };
    auto add_event = [&](BeachNode* cur){ double nxt; if(beachline.get_event(cur, nxt)) events.emplace(nxt, cur); };

    int n = input.size(), cnt = 0;
    arr = new BeachNode[n*4]; sz = 0;
    sort(input.begin(), input.end(), [](const pdd &l, const pdd &r){
            return l.second != r.second ? l.second < r.second : l.first < r.first;
            });

    BeachNode* tmp = beachline.root = new_node(input[0], 0), *t2;
    for(int i = 1; i < n; i++){
        if(dcmp(input[i].second - input[0].second) == 0){
            add_edge(-1, -1, i-1, i, 0, tmp);
            beachline.insert(t2 = new_node(input[i], i), tmp, 1);
            tmp = t2;
        }
        else events.emplace(input[i].second, i);
    }
    while(events.size()){
        event q = events.top(); events.pop();
        BeachNode *prv, *cur, *nxt, *site;
        int v = vertex.size(), idx = q.idx;
        beachline.sweepline = q.sweep;
        if(q.type == 0){
            pdd point = input[idx];
            cur = beachline.find_beachline(point.first);
            beachline.insert(site = new_node(point, idx), cur, 0);
            beachline.insert(prv = new_node(cur->point, cur->idx), site, 0);
            add_edge(-1, -1, cur->idx, idx, site, prv);
            add_event(prv); add_event(cur);
        }
        else{
            cur = q.cur, prv = cur->prv, nxt = cur->nxt;
            if(!prv || !nxt || prv->idx != q.prv || nxt->idx != q.nxt) continue;
            vertex.push_back(get_circumcenter(prv->point, nxt->point, cur->point));
            write_edge(prv->end, v); write_edge(cur->end, v);
            add_edge(v, -1, prv->idx, nxt->idx, 0, prv);
            beachline.erase(cur);
            add_event(prv); add_event(nxt);
        }
    }
    delete arr;
}
// end of Template

constexpr double INF = numeric_limits<double>::infinity();

double inner_product(const pdd& a, const pdd& b) {
    return a.first * b.first + a.second * b.second;
}

pdd project_point_segment(const pdd& a, const pdd& b, const pdd& c) {
    double r = inner_product(b - a, b - a);
    if (fabs(r) <= EPS) {
        return a;
    }
    r = min(max(inner_product(c - a, b - a) / r, 0.0), 1.0);
    return a + r * (b - a);
}

double ccw(const pdd&a, const pdd&b, const pdd&c) {
    return (b.first - a.first) * (c.second-a.second) - (b.second - a.second) * (c.first - a.first);
}

bool is_inside_segment_incl(const pdd&t, const pdd&a, const pdd&b) {
    return fabs(ccw(t, a, b)) <= EPS && inner_product(a - t, t - b) >= -EPS;
}

bool is_inside_triangle_incl(const pdd& t, const pdd&a, const pdd&b, const pdd&c) {
    if (is_inside_segment_incl(t, a, b) ||
        is_inside_segment_incl(t, b, c) ||
        is_inside_segment_incl(t, c, a)) {
        return true;
    }
    double d1 = ccw(t, a, b), d2 = ccw(t, b, c), d3 = ccw(t, c, a);
    return (d1 > EPS && d2 > EPS && d3 > EPS) || (d1 < -EPS && d2 < -EPS && d3 < -EPS);
}

void process_voronoi_diagrams(
    double XR, double YR,
    const vector<pdd>& key_points,
    vector<pdd> P,
    vector<int> *key_nodes,
    vector<vector<pair<int, double>>> *adj,
    double *result) {

    vector<pdd> vertex;
    vector<pii> edge, area;
    VoronoiDiagram(P, vertex, edge, area);
    (*adj).resize(size(vertex));
    for (int i = 0; i < size(area); ++i) {
        const auto& [e1, e2] = edge[i];
        if (e1 == -1 || e2 == -1) {
            continue;  // infinite edge
        }
        const auto& v1 = vertex[e1];
        const auto& v2 = vertex[e2];
        if (min(v1.first, v2.first) < -EPS || max(v1.first, v2.first) > XR + EPS ||
            min(v1.second, v2.second) < -EPS || max(v1.second, v2.second) > YR + EPS) {
            continue;  // edge outside rectangle
        }
        const auto& [pi1, pi2] = area[i];
        vector<pdd> center_points = {P[pi1], P[pi2]};
        const auto& d = size(center_points[0] - project_point_segment(v1, v2, center_points[1]));
        (*adj)[e1].emplace_back(e2, d);
        (*adj)[e2].emplace_back(e1, d);
        const auto& mid = 0.5 * (center_points[0] + center_points[1]);
        for (int j : {0, 1}) {
            for (const auto& p : center_points) {
                const auto& kp = key_points[j];
                *result = min(*result, size(kp - p));
                if (is_inside_triangle_incl(kp, p, v1, mid)) {
                    (*key_nodes)[j] = e1;
                } else if (is_inside_triangle_incl(kp, p, mid, v2)) {
                    (*key_nodes)[j] = e2;
                }
            }
        }
    }
}

double mst(
    const vector<int>& key_nodes,
    const vector<vector<pair<int, double>>>& adj,
    double result) {

    vector<bool> lookup(size(adj));
    priority_queue<pair<double, int>> max_heap;
    max_heap.emplace(result, key_nodes[0]);
    while (!empty(max_heap)) {
        const auto [dist, u] = max_heap.top();
        max_heap.pop();
        result = min(result, dist);
        if (u == key_nodes[1]) {
            break;
        }
        if (lookup[u]) {
            continue;
        }
        lookup[u] = true;
        for (const auto& [v, dist] : adj[u]) {
            if (lookup[v]) {
                continue;
            }
            max_heap.emplace(dist, v);
        }
    }
    return result;
}

double antisocial() {
    int XR, YR;
    cin >> XR >> YR;
    vector<pdd> key_points(2);
    cin >> key_points[0].first >> key_points[0].second
        >> key_points[1].first >> key_points[1].second;
    int N;
    cin >> N;
    vector<pdd> P;
    for (int i = 0; i < N; ++i) {
        int X, Y;
        cin >> X >> Y;
        P.emplace_back(X, Y);
        P.emplace_back(-X, Y);
        P.emplace_back(X, -Y);
        P.emplace_back(2 * XR - X, Y);
        P.emplace_back(X, 2 * YR - Y);
    }
    vector<int> key_nodes(2, -1);
    vector<vector<pair<int, double>>> adj;
    double result = INF;
    process_voronoi_diagrams(XR, YR, key_points, P, &key_nodes, &adj, &result);
    assert(key_nodes[0] >= 0 && key_nodes[1] >= 0);
    return mst(key_nodes, adj, result);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.precision(10);
    int T;
    cin >> T;
    for (int test = 1; test <= T; ++test) {
        cout << "Case #" << test << ": " << antisocial() << endl;
    }
    return 0;
}
