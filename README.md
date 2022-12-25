# [FacebookHackerCup-2021](https://www.facebook.com/hackercup/past_rounds/) ![Language](https://img.shields.io/badge/language-Python-orange.svg) [![License](https://img.shields.io/badge/license-CC%203.0-blue.svg)](https://creativecommons.org/licenses/by-nc/3.0/) ![Progress](https://img.shields.io/badge/progress-27%20%2F%2027-ff69b4.svg) ![Visitors](https://visitor-badge.laobi.icu/badge?page_id=kamyu104.facebookhackercup.2021)

Python solutions of Facebook Hacker Cup 2021. Solution begins with `*` means it will get TLE in the largest data set (total computation amount > `10^8`, which is not friendly for Python to solve in 5 ~ 15 seconds). A `6-minute` timer is set for uploading the result this year.

* [Hacker Cup 2020](https://github.com/kamyu104/FacebookHackerCup-2020)
* [Qualification Round](https://github.com/kamyu104/FacebookHackerCup-2021#qualification-round)
* [Round 1](https://github.com/kamyu104/FacebookHackerCup-2021#round-1)
* [Round 2](https://github.com/kamyu104/FacebookHackerCup-2021#round-2)
* [Round 3](https://github.com/kamyu104/FacebookHackerCup-2021#round-3)
* [Final Round](https://github.com/kamyu104/FacebookHackerCup-2021#final-round)
* [Hacker Cup 2022](https://github.com/kamyu104/MetaHackerCup-2022)

## Qualification Round
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A1| [Consistency - Chapter 1](https://www.facebook.com/codingcompetitions/hacker-cup/2021/qualification-round/problems/A1)| [Python](./Qualification%20Round/consistency_chapter_1.py) [Python](./Qualification%20Round/consistency_chapter_1-2.py) | _O(\|S\|)_ | _O(1)_ | Easy | | Greedy |
|A2| [Consistency - Chapter 2](https://www.facebook.com/codingcompetitions/hacker-cup/2021/qualification-round/problems/A2)| [Python](./Qualification%20Round/consistency_chapter_2.py) [Python](./Qualification%20Round/consistency_chapter_2-2.py) | _O(\|S\|)_ | _O(1)_ | Easy | | Floyd-Warshall Algorithm, Dijkstra's Algorithm |
|B| [Xs and Os](https://www.facebook.com/codingcompetitions/hacker-cup/2021/qualification-round/problems/B)| [Python](./Qualification%20Round/xs_and_os.py) | _O(N^2)_ | _O(1)_ | Easy | | Array |
|C1| [Gold Mine - Chapter 1](https://www.facebook.com/codingcompetitions/hacker-cup/2021/qualification-round/problems/C1)| [Python](./Qualification%20Round/gold_mine_chapter_1.py) | _O(N)_ | _O(N)_ | Easy | | Tree, DFS |
|C2| [Gold Mine - Chapter 2](https://www.facebook.com/codingcompetitions/hacker-cup/2021/qualification-round/problems/C2)| [Python](./Qualification%20Round/gold_mine_chapter_2.py) | _O(N * K^2)_ | _O(N * K)_ | Hard | | Tree, DFS, DP |

## Round 1
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A1| [Weak Typing - Chapter 1](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-1/problems/A1)| [Python](./Round%201/weak_typing_chapter_1.py) | _O(N)_ | _O(1)_ | Easy | | Array |
|A2| [Weak Typing - Chapter 2](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-1/problems/A2)| [Python](./Round%201/weak_typing_chapter_2.py) [Python](./Round%201/weak_typing_chapter_2-2.py) | _O(N)_ | _O(1)_ | Easy | | DP, Math, Counting |
|A3| [Weak Typing - Chapter 3](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-1/problems/A3)| [Python](./Round%201/weak_typing_chapter_3.py) [Python](./Round%201/weak_typing_chapter_3-2.py)  | _O(N)_ | _O(1)_ | Medium | | DP, Matrix Exponentiation, Math, Counting |
|B| [Traffic Control](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-1/problems/B)| [Python](./Round%201/traffic_control.py) | _O(N * M)_ | _O(1)_ | Easy | | Array, Constructive Algorithms |
|C| [Blockchain](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-1/problems/C)| [Python](./Round%201/blockchain.py) | _O(N * MAX_C)_ | _O(N * MAX_C)_ | Hard | | Sort, Union Find, Tree, DFS, DP |

## Round 2
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A| [Runway](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/A)| [Python](./Round%202/runway.py) | _O(N * M)_ | _O(M)_ | Easy | | Simulation, Greedy |
|B| [Chainblock](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/B)| [Python](./Round%202/chainblock.py) [Python](./Round%202/chainblock2.py) | _O(N)_ | _O(N)_ | Medium | | Tree Traversal, Tree Ancestors (Binary Lifting), Tarjan's Offline LCA Algorithm, Union Find |
|C1| [Valet Parking - Chapter 1](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/C1)| [Python](./Round%202/valet_parking_chapter_1.py) | _O(R * C)_ | _O(min(R, C))_ | Medium | | Array |
|C2| [Valet Parking - Chapter 2](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/C2)| ([PyPy](./Round%202/valet_parking_chapter_2.py), [Python](./Round%202/valet_parking_chapter_2-5.py)) ([PyPy](./Round%202/valet_parking_chapter_2-2.py), [PyPy](./Round%202/valet_parking_chapter_2-6.py)) ([PyPy](./Round%202/valet_parking_chapter_2-3.py), [Python](./Round%202/valet_parking_chapter_2-7.py)) ([PyPy](./Round%202/valet_parking_chapter_2-4.py), [Python](./Round%202/valet_parking_chapter_2-8.py)) | _O((R * C + S) * logR)_ | _O(R * C)_ | Hard | | Array, BIT, Fenwick Tree, Skip List, Sorted List, Heap, Segment Tree |
|D| [String Concatenation](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/D)| [PyPy](./Round%202/string_concatenation.py) [Python](./Round%202/string_concatenation2.py) [Python](./Round%202/string_concatenation3.py) | _O(N + L*(logN1)^2 + N2^3/6 + X\*2^X*(N3-X)/C)_ | _O(N)_ | Hard | | Array, Pigeonhole Principle, Birthday Paradox, Sorted List, BIT, Fenwick Tree, Bitmask |

## Round 3
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A| [Rep-ore-ting](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/A)| [Python](./Round%203/rep_ore_ting.py) | _O(M + N)_ | _O(N)_ | Easy | | Intervals, Union Find, Counting |
|B| [Auth-ore-ization](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/B)| [PyPy](./Round%203/auth_ore_ization.py) | _O((M + N) * log(M + N))_ | _O(M + N)_ | Medium | | Sorted List, Segment Tree |
|C| [Perf-ore-mance](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/C)| [Python](./Round%203/perf_ore_mance.py) | _O(N * K^2)_ | _O(N * K)_ | Hard | | Tree, DP |
|D1| [Expl-ore-ation - Chapter 1](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/D1)| [Python](./Round%203/expl_ore_ation_chapter_1.py) | _O((R * C) * log(R * C))_ | _O(R * C)_ | Easy | | Union Find |
|D2| [Expl-ore-ation - Chapter 2](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/D2)| [Python](./Round%203/expl_ore_ation_chapter_2.py) | _O((R * C + K) * log(R * C + K) + ((R * C) * log(R * C) + K) * logK)_ | _O(R * C + K)_ | Medium | | Union Find, Intervals, Sorted List |
|D3| [Expl-ore-ation - Chapter 3](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-3/problems/D3)| [Python](./Round%203/expl_ore_ation_chapter_3.py) [Python](./Round%203/expl_ore_ation_chapter_3-2.py) | _O((R * C + K) * log(R * C)^2)_ | _O(R * C)_ | Hard | | Union Find, Tree Traversal, Tree Ancestors (Binary Lifting), Heavy-Light Decomposition, Sorted List, BIT, Fenwick Tree |

## Final Round
You can relive the magic of the 2021 Hacker Cup World Finals by watching the [Live Stream Recording](https://www.facebook.com/hackercup/videos/627360278409896) of the announcement of winners.

| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A| [And](https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/A)| [Python](./Final%20Round/and.py) | _O(L * N)_ | _O(L * N)_ | Medium | | Greedy, Union Find |
|B| [SSSSSS](https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/B)| [Python](./Final%20Round/ssssss.py) | _O(NlogN)_ | _O(N)_ | Hard | | Greedy, Line Sweep |
|C| [Hire Flyers](https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/C)| [PyPy](./Final%20Round/hire_flyers.py) | _O(N * (logN)^2)_ | _O(NlogN)_ | Hard | | Line Sweep, 2D Segment Tree, BIT, Fenwick Tree |
|D| [Vacation](https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/D)| [Python](./Final%20Round/vacation.py)  | _O(NlogN)_ | _O(N)_ | Medium | | Tree, DFS, DP, Greedy |
|E| [Antisocial](https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/E)| [*PyPy](./Final%20Round/antisocial.py) [C++](./Final%20Round/antisocial.cpp) | _O(NlogN)_ | _O(N)_ | Hard | | Geometry, [Voronoi Diagram (Fortune's Algorithm)](./Final%20Round/voronoi.py), Graph, Maximum Spanning Tree (Kruskal's Algorithm) |
|F| [Table Flipping](https://www.facebook.com/codingcompetitions/hacker-cup/2021/final-round/problems/F)| [*PyPy](./Final%20Round/table_flipping.py) [PyPy](./Final%20Round/table_flipping2.py) [PyPy](./Final%20Round/table_flipping3.py) | _O(NlogN)_ | _O(NlogN)_| Hard | | 2D Line Sweep, 2D Segment Tree, Implicit Segment Tree, Graph, DFS, BFS |
