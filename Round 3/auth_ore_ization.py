# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 1 - Problem B. Auth-ore-ization
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/B
#
# Time:  O((M + N) * log(M + N)), pass in PyPy2 but Python2
# Space: O(M + N)
#

# Template:
# https://github.com/kamyu104/GoogleKickStart-2021/blob/main/Round%20D/final_exam2.py
class SortedList(object):
    def __init__(self, iterable=[], _load=200):
        """Initialize sorted list instance."""
        values = sorted(iterable)
        self._len = _len = len(values)
        self._load = _load
        self._lists = _lists = [values[i:i + _load] for i in xrange(0, _len, _load)]
        self._list_lens = [len(_list) for _list in _lists]
        self._mins = [_list[0] for _list in _lists]

    def _delete(self, pos, idx):
        """Delete value at the given `(pos, idx)`."""
        _lists = self._lists
        _mins = self._mins
        _list_lens = self._list_lens

        self._len -= 1
        del _lists[pos][idx]
        _list_lens[pos] -= 1

        if _list_lens[pos]:
            _mins[pos] = _lists[pos][0]
        else:
            del _lists[pos]
            del _list_lens[pos]
            del _mins[pos]

    def _loc_left(self, value):
        """Return an index pair that corresponds to the first position of `value` in the sorted list."""
        if not self._len:
            return 0, 0

        _lists = self._lists
        _mins = self._mins

        lo, pos = -1, len(_lists) - 1
        while lo + 1 < pos:
            mi = (lo + pos) >> 1
            if value <= _mins[mi]:
                pos = mi
            else:
                lo = mi

        if pos and value <= _lists[pos - 1][-1]:
            pos -= 1

        _list = _lists[pos]
        lo, idx = -1, len(_list)
        while lo + 1 < idx:
            mi = (lo + idx) >> 1
            if value <= _list[mi]:
                idx = mi
            else:
                lo = mi

        return pos, idx

    def _loc_right(self, value):
        """Return an index pair that corresponds to the last position of `value` in the sorted list."""
        if not self._len:
            return 0, 0

        _lists = self._lists
        _mins = self._mins

        pos, hi = 0, len(_lists)
        while pos + 1 < hi:
            mi = (pos + hi) >> 1
            if value < _mins[mi]:
                hi = mi
            else:
                pos = mi

        _list = _lists[pos]
        lo, idx = -1, len(_list)
        while lo + 1 < idx:
            mi = (lo + idx) >> 1
            if value < _list[mi]:
                idx = mi
            else:
                lo = mi

        return pos, idx

    def add(self, value):
        """Add `value` to sorted list."""
        _load = self._load
        _lists = self._lists
        _mins = self._mins
        _list_lens = self._list_lens

        self._len += 1
        if _lists:
            pos, idx = self._loc_right(value)
            _list = _lists[pos]
            _list.insert(idx, value)
            _list_lens[pos] += 1
            _mins[pos] = _list[0]
            if _load + _load < len(_list):
                _lists.insert(pos + 1, _list[_load:])
                _list_lens.insert(pos + 1, len(_list) - _load)
                _mins.insert(pos + 1, _list[_load])
                _list_lens[pos] = _load
                del _list[_load:]
        else:
            _lists.append([value])
            _mins.append(value)
            _list_lens.append(1)

    def discard(self, value):
        """Remove `value` from sorted list if it is a member."""
        _lists = self._lists
        if _lists:
            pos, idx = self._loc_right(value)
            if idx and _lists[pos][idx - 1] == value:
                self._delete(pos, idx - 1)

    def remove(self, value):
        """Remove `value` from sorted list; `value` must be a member."""
        _len = self._len
        self.discard(value)
        if _len == self._len:
            raise ValueError('{0!r} not in list'.format(value))

    def count(self, value):
        """Return number of occurrences of `value` in the sorted list."""
        return self.bisect_right(value) - self.bisect_left(value)

    def lower_bound(self, value):  # added
        """Return the first iter to insert `value` in the sorted list."""
        return self._loc_left(value)

    def upper_bound(self, value):  # added
        """Return the last iter to insert `value` in the sorted list."""
        return self._loc_right(value)

    def val(self, it):  # added
        """Return the value of the `it` in the sorted list."""
        pos, idx = it
        return self._lists[pos][idx]

    def erase(self, it):  # added
        """Remove `it` from sorted list; `it` must be a member."""
        pos, idx = it
        self._delete(pos, idx)

    def begin(self):  # added
        """Return the begin of the it in the sorted list."""
        return (0, 0)

    def end(self):  # added
        """Return the end of the it in the sorted list."""
        return (len(self._lists)-1, len(self._lists[-1])) if self._lists else (0, 0)

    def prev(self, it):  # added
        """Return the previous `it` in the sorted list."""
        pos, idx = it
        return (pos, idx-1) if idx else (pos-1, len(self._lists[pos-1])-1)

    def next(self, it):  # added
        """Return the next `it` in the sorted list."""
        pos, idx = it
        return (pos, idx+1) if pos+1 == len(self._lists) or idx+1 != len(self._lists[pos]) else (pos+1, 0)

    def __len__(self):
        """Return the size of the sorted list."""
        return self._len

    def __contains__(self, value):
        """Return true if `value` is an element of the sorted list."""
        _lists = self._lists
        if _lists:
            pos, idx = self._loc_left(value)
            return idx < len(_lists[pos]) and _lists[pos][idx] == value
        return False

    def __iter__(self):
        """Return an iterator over the sorted list."""
        return (value for _list in self._lists for value in _list)

    def __reversed__(self):
        """Return a reverse iterator over the sorted list."""
        return (value for _list in reversed(self._lists) for value in reversed(_list))

    def __repr__(self):
        """Return string representation of sorted list."""
        return 'SortedList({0})'.format(list(self))

# Template:
# https://github.com/kamyu104/FacebookHackerCup-2021/blob/c53116f2be2ddbafb6d04362a09a03c3659a17dd/Round%202/valet_parking_chapter_2.py
class SegmentTree(object):  # 0-based index
    def __init__(self, N,
                 build_fn=lambda x, y: [y]*(2*x),
                 query_fn=lambda x, y: y if x is None else min(x, y),
                 update_fn=lambda x, y: y if x is None else x+y,
                 default_val=float("inf")):
        self.N = N
        self.query_fn = query_fn
        self.update_fn = update_fn
        self.tree = build_fn(2**((N-1).bit_length()), default_val)  # modified, make it a perfect binary tree rather than complete and full one to make query possible
        self.base = len(self.tree)-N

    def __apply(self, x):
        if x >= self.base:
            self.update_fn(x-self.base, self.tree[x])  # modified

    def update(self, i):  # Time: O(logN), Space: O(N)
        def pull(x):
            while x > 1:
                x //= 2
                self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2+1])

        self.__apply(i+self.base)  # modified
        pull(i+self.base)  # modified

    def query(self, L, R):  # Time: O(logN), Space: O(N)
        if L > R:
            return None
        L += self.base  # modified
        R += self.base  # modified
        left = right = None  # modified
        while L <= R:
            if L & 1:  # is right child
                left = self.query_fn(left, self.tree[L])  # modified
                L += 1
            if R & 1 == 0:  # is left child
                right = self.query_fn(self.tree[R], right)  # modified
                R -= 1
            L //= 2
            R //= 2
        return self.query_fn(left, right)  # modified

    def __str__(self):
        showList = []
        for i in xrange(self.base):
            showList.append(self.query(i, i))
        return ",".join(map(str, showList))

    def get(self, i):  # added
        return self.tree[self.base+i]

def mulmod(a, b):
    return (a*b)%MOD

def add_cell(G, G0, G1, st, r, c):
    G[r][c] = 1
    G0[c].remove(r)
    G1[c].add(r)
    st.update(r)

def query_path(G, G0, G1, st, r1, c1, r2, c2):
    result = INF
    dist = st.query(r1, r2)
    for a in xrange(3):
        for b in xrange(3):
            d1, d2 = st.get(r1)[c1][a], st.get(r2)[c2][b]
            if d1 == INF and abs(a-c1) == 2 and G[r1][c1] and G[r1][a]:
                i = G1[1].val(G1[1].prev(G1[1].lower_bound(r1)))
                if i >= 0 and i > G0[0].val(G0[0].prev(G0[0].lower_bound(r1))) and i > G0[2].val(G0[2].prev(G0[2].lower_bound(r1))):
                    d1 = 2*(r1-i)+2
            if d2 == INF and abs(b-c2) == 2 and G[r2][c2] and G[r2][b]:
                i = G1[1].val(G1[1].lower_bound(r2))
                if i < len(G) and i < G0[0].val(G0[0].lower_bound(r2)) and i < G0[2].val(G0[2].lower_bound(r2)):
                    d2 = 2*(i-r2)+2
            d = d1+dist[a][b]+d2
            if d < result:
                result = d
    return result if result != INF else 1

def auth_ore_ization():
    def build(x, y):
        return [[[y]*3 for _ in xrange(3)] for _ in xrange(2*x)]

    def update(r, x):
        for a in xrange(3):
            for b in xrange(a, 3):
                if not G[r][b]:
                    break
                x[a][b] = x[b][a] = b-a

    def query(x, y):
        return y if x is None else x if y is None else [[min(x[a][c]+1+y[c][b] for c in xrange(3)) for b in xrange(3)] for a in xrange(3)]

    N, M = map(int, raw_input().strip().split())
    events = [(A, 0, r, c) for r in xrange(N) for c, A in enumerate(map(int, raw_input().strip().split()))]
    for _ in xrange(M):
        R1, C1, R2, C2, L = map(int, raw_input().strip().split())
        if R1 > R2:
            R1, R2 = R2, R1
            C1, C2 = C2, C1
        events.append((L, 1, R1-1, C1-1, R2-1, C2-1))
    events.sort()  # Time: O((M + N) * log(M + N))
    G = [[0]*3 for _ in xrange(N)]
    G0 = [SortedList(xrange(-1, N+1)) for _ in xrange(3)]
    G1 = [SortedList([-1, N]) for _ in xrange(3)]
    st = SegmentTree(N, build_fn=build, update_fn=update, query_fn=query, default_val=INF)
    result = 1
    for event in events:  # Time: O((M + N) * logN)
        if not event[1]:
            add_cell(G, G0, G1, st, *event[2:])
        else:
            result = mulmod(result, query_path(G, G0, G1, st, *event[2:]))
    return result

MOD = 10**9+7
MAX_N = 10**6
INF = MAX_N*3
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, auth_ore_ization())
