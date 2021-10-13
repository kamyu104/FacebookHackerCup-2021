# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 1 - Problem B. Auth-ore-ization
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/B
#
# Time:  O((M + N) * log(M + N)), pass in PyPy2 but Python2
# Space: O(M + N)
#

# Template:
# https://github.com/cheran-senthil/PyRival/blob/master/pyrival/data_structures/SortedList.py
class SortedList(object):
    def __init__(self, iterable=[], _load=200):
        """Initialize sorted list instance."""
        values = sorted(iterable)
        self._len = _len = len(values)
        self._load = _load
        self._lists = _lists = [values[i:i + _load] for i in xrange(0, _len, _load)]
        self._list_lens = [len(_list) for _list in _lists]
        self._mins = [_list[0] for _list in _lists]
        self._fen_tree = []
        self._rebuild = True

    def _fen_build(self):
        """Build a fenwick tree instance."""
        self._fen_tree[:] = self._list_lens
        _fen_tree = self._fen_tree
        for i in xrange(len(_fen_tree)):
            if i | i + 1 < len(_fen_tree):
                _fen_tree[i | i + 1] += _fen_tree[i]
        self._rebuild = False

    def _fen_update(self, index, value):
        """Update `fen_tree[index] += value`."""
        if not self._rebuild:
            _fen_tree = self._fen_tree
            while index < len(_fen_tree):
                _fen_tree[index] += value
                index |= index + 1

    def _fen_query(self, end):
        """Return `sum(_fen_tree[:end])`."""
        if self._rebuild:
            self._fen_build()

        _fen_tree = self._fen_tree
        x = 0
        while end:
            x += _fen_tree[end - 1]
            end &= end - 1
        return x

    def _fen_findkth(self, k):
        """Return a pair of (the largest `idx` such that `sum(_fen_tree[:idx]) <= k`, `k - sum(_fen_tree[:idx])`)."""
        _list_lens = self._list_lens
        if k < _list_lens[0]:
            return 0, k
        if k >= self._len - _list_lens[-1]:
            return len(_list_lens) - 1, k + _list_lens[-1] - self._len
        if self._rebuild:
            self._fen_build()

        _fen_tree = self._fen_tree
        idx = -1
        for d in reversed(xrange(len(_fen_tree).bit_length())):
            right_idx = idx + (1 << d)
            if right_idx < len(_fen_tree) and k >= _fen_tree[right_idx]:
                idx = right_idx
                k -= _fen_tree[idx]
        return idx + 1, k

    def _delete(self, pos, idx):
        """Delete value at the given `(pos, idx)`."""
        _lists = self._lists
        _mins = self._mins
        _list_lens = self._list_lens

        self._len -= 1
        self._fen_update(pos, -1)
        del _lists[pos][idx]
        _list_lens[pos] -= 1

        if _list_lens[pos]:
            _mins[pos] = _lists[pos][0]
        else:
            del _lists[pos]
            del _list_lens[pos]
            del _mins[pos]
            self._rebuild = True

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
            self._fen_update(pos, 1)
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
                self._rebuild = True
        else:
            _lists.append([value])
            _mins.append(value)
            _list_lens.append(1)
            self._rebuild = True

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

    def pop(self, index=-1):
        """Remove and return value at `index` in sorted list."""
        pos, idx = self._fen_findkth(self._len + index if index < 0 else index)
        value = self._lists[pos][idx]
        self._delete(pos, idx)
        return value

    def bisect_left(self, value):
        """Return the first index to insert `value` in the sorted list."""
        pos, idx = self._loc_left(value)
        return self._fen_query(pos) + idx

    def bisect_right(self, value):
        """Return the last index to insert `value` in the sorted list."""
        pos, idx = self._loc_right(value)
        return self._fen_query(pos) + idx

    def count(self, value):
        """Return number of occurrences of `value` in the sorted list."""
        return self.bisect_right(value) - self.bisect_left(value)

    def __len__(self):
        """Return the size of the sorted list."""
        return self._len

    def __getitem__(self, index):
        """Lookup value at `index` in sorted list."""
        pos, idx = self._fen_findkth(self._len + index if index < 0 else index)
        return self._lists[pos][idx]

    def __delitem__(self, index):
        """Remove value at `index` from sorted list."""
        pos, idx = self._fen_findkth(self._len + index if index < 0 else index)
        self._delete(pos, idx)

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
        def ceil_log2(x):
            return (x-1).bit_length()

        self.H = (N-1).bit_length()  # modified
        size = 2*(2**ceil_log2(N))-1  # modified, make it a perfect (full and complete) binary tree to make query possible
        self.base = size-N  # modified
        self.query_fn = query_fn
        self.update_fn = update_fn
        self.tree = build_fn(size, default_val)  # modified

    def __apply(self, x, val):
        if x >= self.base:
            self.tree[x] = self.update_fn(x-self.base, self.tree[x], val)  # modified

    def update(self, i, h):  # Time: O(logN), Space: O(N)
        def pull(x):
            while x:
                x = (x-1)//2  # modified
                self.tree[x] = self.query_fn(self.tree[x*2+1], self.tree[x*2+2])  # modified

        self.__apply(i+self.base, h)  # modified
        pull(i+self.base)  # modified

    def query(self, L, R):  # Time: O(logN), Space: O(N)
        if L > R:
            return None
        L += self.base  # modified
        R += self.base  # modified
        left = right = None  # modified
        while L <= R:
            if L & 1 == 0:  # is right child, modified
                left = self.query_fn(left, self.tree[L])
                L += 1
            if R & 1:  # is left child, modified
                right = self.query_fn(self.tree[R], right)
                R -= 1
            L = (L-1)//2  # modified
            R = (R-1)//2  # modified
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
    st.update(r, 1)

def query_path(G, G0, G1, st, r1, c1, r2, c2):
    result = INF
    dist = st.query(r1, r2)
    for a in xrange(3):
        for b in xrange(3):
            d1, d2 = st.get(r1)[c1][a], st.get(r2)[c2][b]
            if d1 == INF and abs(a-c1) == 2 and G[r1][c1] and G[r1][a]:
                i = G1[1][G1[1].bisect_left(r1)-1]
                if i >= 0 and i > G0[0][G0[0].bisect_left(r1)-1] and i > G0[2][G0[2].bisect_left(r1)-1]:
                    d1 = 2*(r1-i)+2
            if d2 == INF and abs(b-c2) == 2 and G[r2][c2] and G[r2][b]:
                i = G1[1][G1[1].bisect_left(r2)]
                if i < len(G) and i < G0[0][G0[0].bisect_left(r2)] and i < G0[2][G0[2].bisect_left(r2)]:
                    d2 = 2*(i-r2)+2
            result = min(result, d1+dist[a][b]+d2)
    return result if result != INF else 1

def auth_ore_ization():
    def build(x, y):
        return [[[y]*3 for _ in xrange(3)] for _ in xrange(x)]

    def update(r, x, _):
        for a in xrange(3):
            for b in xrange(a, 3):
                if not G[r][b]:
                    break
                x[a][b] = x[b][a] = b-a
        return x

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

INF = float("inf")
MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, auth_ore_ization())
