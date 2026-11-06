class Graph:
    def __init__(self):
        self._out = {}   # vertex -> set of successors
        self._in = {}    # vertex -> set of predecessors

    # ---------------------------------------------------------------- #
    # Required methods
    # ---------------------------------------------------------------- #
    def addVertex(self, vertex):
        if vertex in self._out:
            return False
        self._out[vertex] = set()
        self._in[vertex] = set()
        return True

    def addEdge(self, from_vertex, to_vertex):
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
        self._require(vertex)
        return list(self._in[vertex])

    # ---------------------------------------------------------------- #
    # Extra methods
    # ---------------------------------------------------------------- #
    def listOutgoingAdjacentVertex(self, vertex):
        self._require(vertex)
        return list(self._out[vertex])

    def removeEdge(self, from_vertex, to_vertex):
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
