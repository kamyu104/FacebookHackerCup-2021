# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 3 - Problem D. Expl-ore-ation Chapter 3
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/D3
#
# Time:  O((R * C) * log(R * C) + R * C * alpha(R * C) + (R * C + K) * log(R * C)^2) = O((R * C + K) * log(R * C)^2)
# Space: O(R * C)
#

from functools import partial

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
        self.adj = [[] for _ in xrange(n)]  # added
        self.height = [INF]*n  # added
        self.node = range(n)  # added

    def find_set(self, x):
        stk = []
        while self.set[x] != x:  # path compression
            stk.append(x)
            x = self.set[x]
        while stk:
            self.set[stk.pop()] = x
        return x

    def union_set(self, x, y, h):
        x, y = self.find_set(x), self.find_set(y)
        if x == y:
            return False
        if self.rank[x] > self.rank[y]:  # union by rank
            x, y = y, x
        self.set[x] = self.set[y]
        if self.rank[x] == self.rank[y]:
            self.rank[y] += 1

        # belows are all added
        self.adj.append([self.node[x], self.node[y]])
        self.height.append(h)
        self.node[y] = len(self.adj)-1
        return True

# Template: https://github.com/kamyu104/GoogleCodeJam-2020/blob/master/Virtual%20World%20Finals/pack_the_slopes.py
class HLD(object):  # Heavy-Light Decomposition
    def __init__(self, root, adj):
        self.__children = adj
        self.__size = [-1]*len(adj)  # Space: O(N)
        self.__chain = [-1]*len(adj)

        # belows are added
        self.L = [-1]*len(adj)
        self.R = [-1]*len(adj)
        self.P = [[] for _ in xrange(len(adj))]
        self.inv = [-1]*len(adj)
        self.S = SortedList([-1])
        self.S2 = SortedList()

        self.__find_heavy_light(root)
        self.__decompose(root)

    def __find_heavy_light(self, i):  # Time: O(N)
        def divide(curr):
            size[curr] = 1
            stk.append(partial(postprocess, curr))
            for child in reversed(children[curr]):
                stk.append(partial(divide, child))

        def postprocess(curr):
            for i, child in enumerate(children[curr]):
                size[curr] += size[child]
                if size[child] > size[children[curr][0]]:
                    children[curr][0], children[curr][i] = children[curr][i], children[curr][0]  # make the first child heaviest

        stk, children, size = [], self.__children, self.__size
        stk.append(partial(divide, i))
        while stk:
            stk.pop()()

    def __decompose(self, i):  # Time: O(N)
        def divide(curr, parent):
            # ancestors of the node i
            if parent != -1:
                P[curr].append(parent)
            i = 0
            while i < len(P[curr]) and i < len(P[P[curr][i]]):
                P[curr].append(P[P[curr][i]][i])
                i += 1
            # the subtree of the node i is represented by traversal index L[i]..R[i]
            C[0] += 1
            L[curr] = C[0]
            inv[C[0]] = curr
            chain[curr] = curr if parent == -1 or children[parent][0] != curr else chain[parent]  # create a new chain if it is not the first child which is heavy
            stk.append(partial(postprocess, curr))
            for child in reversed(children[curr]):
                stk.append(partial(divide, child, curr))

        def postprocess(curr):
            R[curr] = C[0]

        stk, children, chain, L, R, P, inv, C = [], self.__children, self.__chain, self.L, self.R, self.P, self.inv, [-1]
        stk.append(partial(divide, i, -1))
        while stk:
            stk.pop()()

    def highest_valid_ancestor(self, S, uf, i):  # added, Time: O(log(R * C))
        s = S[i]
        for j in reversed(xrange(len(self.P[i]))):
            if j < len(self.P[i]) and uf.height[self.P[i][j]] > s:  # find highest ancestor x s.t. uf.height[x] > s
                i = self.P[i][j]
        return i

    def update(self, i, d):  # added, Time: O(log(R * C))
        if d == 1:
            self.S.add(self.L[i])
            self.S2.add(self.L[i])
        else:
            self.S.remove(self.L[i])
            self.S2.remove(self.L[i])

    def subtree_has_robot(self, i, exclude_root):  # added, Time: O(log(R * C))
        i, r = self.S2.bisect_left(self.L[i]+exclude_root), self.R[i]
        return i != len(self.S2) and self.S2[i] <= r

    def find_closest_ancestor_has_robot(self, i):  # added, Time: O(log(R * C)^2)
        while i >= 0:
            j = self.__chain[i]
            k = self.S[self.S.bisect_left(self.L[i]+1)-1]  # Time: O(log(R * C))
            if k >= self.L[j]:
                return self.inv[k]
            i = self.P[j][0] if self.P[j] else -1  # O(log(R * C)) times
        return -1

def update_cell(H, S, uf, hld, i, d):
    dx = dy = 0
    if S[i] >= H[i]:
        return dx, dy
    dx += d
    i = hld.highest_valid_ancestor(S, uf, i)
    if d == -1:
        hld.update(i, d)
    if not hld.subtree_has_robot(i, 0):
        a = hld.find_closest_ancestor_has_robot(i)
        if a < 0 or hld.subtree_has_robot(a, 1):
            dy += d
    if d == 1:
        hld.update(i, d)
    return dx, dy

def expl_ore_ation_chapter_3():
    R, C = map(int, raw_input().strip().split())
    H = []
    for _ in xrange(R):
        H.extend(map(int, raw_input().strip().split()))
    S = []
    for _ in xrange(R):
        S.extend(map(int, raw_input().strip().split()))

    events = []
    for i in xrange(R*C):
        if i-C >= 0:  # up
            events.append((min(H[i], H[i-C]), i, i-C))
        if i%C-1 >= 0:  # left
            events.append((min(H[i], H[i-1]), i, i-1))
    events.sort(reverse=True)
    uf = UnionFind(R*C)
    for h, a, b in events:
        uf.union_set(a, b, h)
    hld = HLD(len(uf.adj)-1, uf.adj)

    X, Y = 0, 0
    for i in xrange(R*C):
        dx, dy = update_cell(H, S, uf, hld, i, 1)
        X += dx
        Y += dy
    result = total = 0
    for idx in xrange(input()):
        A, B, U = map(int, raw_input().strip().split())
        A, B, U = ((A^Y)-1, (B^Y)-1, U^Y) if idx else (A-1, B-1, U)
        i = A*C+B
        dx, dy = update_cell(H, S, uf, hld, i, -1)  # remove
        X += dx
        Y += dy
        S[i] = U  # update
        dx, dy = update_cell(H, S, uf, hld, i, 1)  # add
        X += dx
        Y += dy
        result += X
        total += Y
    return "%s %s" % (result, total)

INF = float("inf")
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, expl_ore_ation_chapter_3())
