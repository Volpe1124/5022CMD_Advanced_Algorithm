# 5022CMD Advanced Algorithms – Portfolio

Python 3.10+ (tested on Python 3.13). No external libraries are needed.

| Folder | Question | Run |
|---|---|---|
| `q1_hashing/` | Hash table (open addressing, linear probing) + Pharmacy Inventory System + search performance experiment | `python inventory_system.py`  /  `python performance_test.py` |
| `q2_graph/` | Generic directed graph + University Course Prerequisite System | `python course_system.py` |
| `q3_concurrency/` | Fibonacci with and without multithreading (10 rounds each) | `python fibonacci_threads.py` (takes several minutes) |

## Files

```
q1_hashing/
  hash_table.py        generic HashTable (open addressing + linear probing, tombstone deletion, resizing)
  medicine.py          Medicine entity class
  inventory_system.py  command-line inventory: insert, search, edit, delete, list
  performance_test.py  hash table vs 1-D array search experiment
q2_graph/
  graph.py             generic unweighted directed Graph (addVertex, addEdge, listIncomingAdjacentVertex, ...)
  course.py            Course entity class
  course_system.py     menu-driven prerequisite system (all mandatory + all 4 advanced features)
q3_concurrency/
  fibonacci_threads.py recursive Fibonacci, 3 threads vs sequential, timing in nanoseconds
```
