# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 3 - Problem D. Expl-ore-ation Chapter 2
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/D2
#
# Time:  O((R * C + S + K) * log(R * C + S + K) + R * C * alpha(R * C) + (R * C + S + K) * log(R * C + S + K) * logK) = O((R * C + S + K) * log(R * C + S + K) * logK)
# Space: O(R * C + S + K)
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

class UnionFind(object):  # Time: O(n * alpha(n)), Space: O(n)
    def __init__(self, n):
        self.set = range(n)
        self.rank = [0]*n
        self.intervals = [SortedList([(-INF, -INF), (INF, INF)]) for _ in xrange(n)]  # modified

    def find_set(self, x):
        stk = []
        while self.set[x] != x:  # path compression
            stk.append(x)
            x = self.set[x]
        while stk:
            self.set[stk.pop()] = x
        return x

    def union_set(self, x, y):
        x, y = self.find_set(x), self.find_set(y)
        if x == y:
            return False
        if self.rank[x] > self.rank[y]:  # union by rank
            x, y = y, x
        self.set[x] = self.set[y]
        if self.rank[x] == self.rank[y]:
            self.rank[y] += 1

        # belows are all added
        if len(self.intervals[x]) > len(self.intervals[y]):
            self.intervals[x], self.intervals[y] = self.intervals[y], self.intervals[x]
        for a, b in self.intervals[x]:  # merge smaller self.intervals[x] into larger self.intervals[y]
            if a in (-INF, INF):
                continue
            self.__add_interval(a, b, self.intervals[y])
        self.intervals[x] = SortedList()  # clear
        return True

    def __add_interval(self, a, b, interval):  # Total Time: O((R * C + K) * log(R * C) * logK)
        i = interval.bisect_left((a+1,))-1
        c, d = interval[i]
        if d < a-1:
            i += 1
            c, d = interval[i]
        overlapped = 0
        while c <= b+1:
            a, b = min(a, c), max(b, d)
            del interval[i]
            overlapped += d-c+1
            c, d = interval[i]
        interval.add((a, b))  # O((R * C + K) * log(R * C)) times, each costs Time: O(logK)
        return (b-a+1)-overlapped

    def add_robot(self, x, a, b):  # added
        return self.__add_interval(a, b, self.intervals[self.find_set(x)])

def expl_ore_ation_chapter_2():
    R, C = map(int, raw_input().strip().split())
    H = []
    for _ in xrange(R):
        H.extend(map(int, raw_input().strip().split()))
    S = []
    for _ in xrange(R):
        S.extend(map(int, raw_input().strip().split()))
    K = input()
    changes = [map(int, raw_input().strip().split()) for _ in xrange(K)]

    intervals = [[] for _ in xrange(R*C)]
    for i, s in enumerate(S):
        intervals[i].append((0, s))
    for idx, (A, B, U) in enumerate(changes):
        A -= 1
        B -= 1
        i = A*C+B
        if not idx:
            intervals[i][:] = []
        intervals[i].append((idx, U))
    events = []
    for i in xrange(R*C):
        if i-C >= 0:  # up
            events.append((min(H[i], H[i-C]), -1, i, i-C))
        if i%C-1 >= 0:  # left
            events.append((min(H[i], H[i-1]), -1, i, i-1))
    for i, interval in enumerate(intervals):
        for j, (a, u) in enumerate(interval):
            b = interval[j+1][0]-1 if j+1 < len(interval) else K-1
            events.append((u, i, a, b))
    events.sort(reverse=True)

    uf = UnionFind(R*C)
    result = total = 0
    for h, i, a, b in events:
        if i == -1:
            uf.union_set(a, b)
            continue
        if H[i] <= h:
            continue
        result += b-a+1
        total += uf.add_robot(i, a, b)
    return "%s %s" % (result, total)

INF = float("inf")
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, expl_ore_ation_chapter_2())
