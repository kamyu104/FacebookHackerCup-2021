# [FacebookHackerCup-2021](https://www.facebook.com/hackercup/past_rounds/) ![Language](https://img.shields.io/badge/language-Python-orange.svg) [![License](https://img.shields.io/badge/license-CC%203.0-blue.svg)](https://creativecommons.org/licenses/by-nc/3.0/) ![Progress](https://img.shields.io/badge/progress-15%20%2F%2015-ff69b4.svg) ![Visitors](https://visitor-badge.laobi.icu/badge?page_id=kamyu104.facebookhackercup.2021)

Python solutions of Facebook Hacker Cup 2021. Solution begins with `*` means it will get TLE in the largest data set (total computation amount > `10^8`, which is not friendly for Python to solve in 5 ~ 15 seconds). A `6-minute` timer is set for uploading the result this year.

* [Hacker Cup 2020](https://github.com/kamyu104/FacebookHackerCup-2020)
* [Qualification Round](https://github.com/kamyu104/FacebookHackerCup-2021#qualification-round)
* [Round 1](https://github.com/kamyu104/FacebookHackerCup-2021#round-1)
* [Round 2](https://github.com/kamyu104/FacebookHackerCup-2021#round-2)

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
|C2| [Valet Parking - Chapter 2](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/C2)| [PyPy](./Round%202/valet_parking_chapter_2.py) [PyPy](./Round%202/valet_parking_chapter_2-2.py) [PyPy](./Round%202/valet_parking_chapter_2-3.py) [PyPy](./Round%202/valet_parking_chapter_2-4.py) [Python](./Round%202/valet_parking_chapter_2-5.py) | _O((R * C + S) * logR)_ | _O(R * C)_ | Hard | | Array, BIT, Fenwick Tree, Skip List, Sorted List, Heap, Segment Tree |
|D| [String Concatenation](https://www.facebook.com/codingcompetitions/hacker-cup/2021/round-2/problems/D)| [PyPy](./Round%202/string_concatenation.py) [Python](./Round%202/string_concatenation2.py) [Python](./Round%202/string_concatenation3.py) | _O(N + L*(logN1)^2 + N2^3/6 + X*2^X*(N3-X)/C)_ | _O(N)_ | Hard | | Array, Pigeonhole Principle, Birthday Paradox, Sorted List, BIT, Fenwick Tree, Bitmask |