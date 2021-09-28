# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2021 Round 2 - Problem D. String Concatenation
# https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/D
#
# Time:  O(N + L*(logN1)^2 + N2^3/6 + 2^X*(N3-X)/C) ~= O(1e8) at worst
# Space: O(N)
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

def update_remains(A, B, R):
    R[:] = [i for i in R if i not in A and i not in B]

def add_equal_1sums(L, A, B, R):  # Time: O(N), N1 = O(N)
    lookup = {}
    for a in R:
        total = L[a]
        if total not in lookup:
            lookup[total] = a
            continue
        A.add(a)
        B.add(lookup[total])
        del lookup[total]
    update_remains(A, B, R)
    return R

def add_equal_2sums(L, A, B, R):  # Time: O(N1logN1) + O((2 * L) * (1/N1 + 1/(N1-1) + ... + 1/1)) * O(logN1) = O(N1logN1 + L * (logN1)^2) ~= O(6e7), N2 = O(894)
    lookup = {}
    R_inv = {x:i for i, x in enumerate(R)}
    sl = SortedList()
    nxt = {}
    for i in xrange(len(R)):
        sl.add(i)
        nxt[i] = i+1
    sl.add(len(R))
    done = False
    while not done and len(sl) != 1:
        i = next(iter(sl))
        while i != len(R):
            a = R[i]
            j = sl[sl.bisect_left(nxt[i])]
            if j == len(R):
                if i == next(iter(sl)):
                    done = True
                break
            b = R[j]
            total = L[a]+L[b]
            if total in lookup:
                for x in lookup[total]:
                    assert(x not in (a, b))
                    if x in A or x in B:
                        del lookup[total]
                        break
            if total not in lookup:
                lookup[total] = (a, b)
                nxt[i] = sl[sl.bisect_right(j)]
                i = sl[sl.bisect_right(i)]
                continue
            A.add(a), A.add(b)
            c, d = lookup[total]
            B.add(c), B.add(d)
            del lookup[total]
            for x in (a, b, c, d):
                sl.remove(R_inv[x])
            i = sl[sl.bisect_right(i)]
    update_remains(A, B, R)
    assert(len(R) <= 894)  # max v s.t. v(v-1)/2! <= 2*MAX_L
    return R

def add_equal_3sums(L, A, B, R):  # Time: O(N2^3/3!) = O(894^3/6) ~= O(1e8), N3 = O(154)
    lookup = {}
    for i in xrange(len(R)):
        a = R[i]
        for j in xrange(i):
            if a in A or a in B:
                break
            b = R[j]
            for k in xrange(j):
                if b in A or b in B:
                    break
                c = R[k]
                if c in A or c in B:
                    continue
                total = L[a]+L[b]+L[c]
                if total in lookup:
                    for x in lookup[total]:
                        if x in (a, b, c) or x in A or x in B:
                            del lookup[total]
                            break
                if total not in lookup:
                    lookup[total] = (a, b, c)
                    continue
                A.add(a), A.add(b), A.add(c)
                d, e, f = lookup[total]
                B.add(d), B.add(e), B.add(f)
                del lookup[total]
    update_remains(A, B, R)
    assert(len(R) <= 154)  # max v s.t. v(v-1)(v-3)/3! <= 3*MAX_L
    return R

def find_equal_sum_masks(L, idxs):  # Time: O(2^X * (N3-X)/C) = O(2^23 * (154-23)/6) ~= O(2e8) at worst, C = 6 on average
    lookup = {}
    for mask in xrange(1, 1<<len(idxs)):
        total, bit = 0, 1
        for i in idxs:
            if mask&bit:
                total += L[i]
            bit <<= 1
        if total in lookup:
            return mask, lookup[total]
        lookup[total] = mask
    return None

def add_remains(N, K, L, A, B, R):
    curr = []
    for i in xrange(len(R)):
        curr.append(R[i])
        if N-(len(A)+len(B)) <= K:
            break
        if len(curr) == X or i == len(R)-1:
            pair_masks = find_equal_sum_masks(L, curr)
            if not pair_masks:
                return "Impossible"
            mask_A, mask_B = pair_masks
            nxt = []
            bit = 1
            for i in curr:
                if (mask_A&bit) and not (mask_B&bit):
                    A.add(i)
                elif (mask_B&bit) and not (mask_A&bit):
                    B.add(i)
                else:
                    nxt.append(i)
                bit <<= 1
            curr = nxt
    return "Possible\n%s\n%s" % (" ".join(map(lambda x: str(x+1), A)), " ".join(map(lambda x: str(x+1), B)))

def string_concatenation():
    N, K = map(int, raw_input().strip().split())
    L = map(int, raw_input().strip().split())

    A, B, R = set(), set(), range(N)
    add_equal_1sums(L, A, B, R)
    add_equal_2sums(L, A, B, R)
    add_equal_3sums(L, A, B, R)
    return add_remains(N, K, L, A, B, R)

MAX_L = 200000
X = 1
while 2**X < X*MAX_L+1:  # pigeonhole principle
    X += 1
assert(X == 23)  # we can always find equal sum subsets by 23 or more strings
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, string_concatenation())
