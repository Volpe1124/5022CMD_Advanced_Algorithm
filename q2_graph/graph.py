"""
graph.py
A generic, reusable unweighted DIRECTED graph.

Vertices can be any hashable object (strings, ints, Course objects...).
The graph contains no domain-specific code, so it can be reused in any
context (course prerequisites, task dependencies, social networks, ...).

Both an outgoing and an incoming adjacency set are kept for every vertex:
  _out[v] = vertices v points TO      (v -> w)
  _in[v]  = vertices pointing INTO v  (u -> v)
This makes listing incoming AND outgoing neighbours O(degree) instead of
having to scan every vertex in the graph.
"""


class Graph:
    def __init__(self):
        self._out = {}   # vertex -> set of successors
        self._in = {}    # vertex -> set of predecessors

    # ---------------------------------------------------------------- #
    # Required methods
    # ---------------------------------------------------------------- #
    def addVertex(self, vertex):
        """Add a new vertex. Returns False if it already exists."""
        if vertex in self._out:
            return False
        self._out[vertex] = set()
        self._in[vertex] = set()
        return True

    def addEdge(self, from_vertex, to_vertex):
        """Add a directed edge from_vertex -> to_vertex.

        Both vertices must already exist. Self-loops are rejected.
        Returns True if a new edge was created, False if it already existed.
        """
        self._require(from_vertex)
        self._require(to_vertex)
        if from_vertex == to_vertex:
            raise ValueError("a vertex cannot have an edge to itself")
        if to_vertex in self._out[from_vertex]:
            return False
        self._out[from_vertex].add(to_vertex)
        self._in[to_vertex].add(from_vertex)
        return True

    def listIncomingAdjacentVertex(self, vertex):
        """Return all vertices that have an edge coming INTO vertex."""
        self._require(vertex)
        return list(self._in[vertex])

    # ---------------------------------------------------------------- #
    # Extra methods
    # ---------------------------------------------------------------- #
    def listOutgoingAdjacentVertex(self, vertex):
        """Return all vertices that vertex has an edge going TO."""
        self._require(vertex)
        return list(self._out[vertex])

    def removeEdge(self, from_vertex, to_vertex):
        """Remove the edge from_vertex -> to_vertex. Returns True if removed."""
        self._require(from_vertex)
        self._require(to_vertex)
        if to_vertex not in self._out[from_vertex]:
            return False
        self._out[from_vertex].discard(to_vertex)
        self._in[to_vertex].discard(from_vertex)
        return True

    def hasEdge(self, from_vertex, to_vertex):
        return from_vertex in self._out and to_vertex in self._out[from_vertex]

    def hasPath(self, start, goal):
        """Depth-first search: is goal reachable from start?"""
        stack, seen = [start], set()
        while stack:
            v = stack.pop()
            if v == goal:
                return True
            if v not in seen:
                seen.add(v)
                stack.extend(self._out.get(v, ()))
        return False

    def vertices(self):
        return list(self._out)

    def __contains__(self, vertex):
        return vertex in self._out

    def __len__(self):
        return len(self._out)

    def _require(self, vertex):
        if vertex not in self._out:
            raise KeyError(f"vertex {vertex!r} is not in the graph")
