import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue

def np_to_points(p):
    l = []
    for i in range(p.shape[0]):
        l += [Point(p[i, :])]
    return l

class SiteSet:
    def __init__(self, sites = None):
        self.sites = {}
        if (sites == None or len(sites) == 0):
            return
        for p in sites:
            self.sites[p] = None
    def __iter__(self):
        self.i = 0
        return self
    def __next__(self):
        k = list(self.sites.keys())
        if (self.i < len(k)):
            result = k[self.i]
            self.i += 1
            return result
        else:
            raise StopIteration
    def __getitem__(self, ind):
        k = list(self.sites.keys())
        return k[ind]
    def __len__(self):
        return len(list(self.sites.keys()))
    def __str__(self):
        result = ""
        for i in range(len(self)):
            result += str(self[i]) + ", "
        return result[:-2]
    def add(self, p):
        self.sites[p] = None

class EdgeSet:
    def __init__(self, edges = None):
        self.edges = {}
        if (edges == None or len(edges) == 0):
            return
        for e in edges:
            self.edges[e] = None
    def __iter__(self):
        self.i = 0
        return self
    def __next__(self):
        k = list(self.edges.keys())
        if (self.i < len(k)):
            result = k[self.i]
            self.i += 1
            return result
        else:
            raise StopIteration
    def __getitem__(self, ind):
        k = list(self.edges.keys())
        return k[ind]
    def __len__(self):
        return len(list(self.edges.keys()))
    def __str__(self):
        result = ""
        for i in range(len(self)):
            result += str(self[i]) + " + "
        return result[:-3]
    def add(self, e):
        self.edges[e] = None

class CellSet:
    def __init__(self, cells = None):
        self.cells = {}
        if (cells == None or len(cells) == 0):
            return
        for c  in cells:
            self.cells[c] = None
    def __iter__(self):
        self.i = 0
        return self
    def __next__(self):
        k = list(self.cells.keys())
        if (self.i < len(k)):
            result = k[self.i]
            self.i += 1
            return result
        else:
            raise StopIteration
    def __getitem__(self, ind):
        k = list(self.cells.keys())
        return k[ind]
    def __len__(self):
        return len(list(self.cells.keys()))
    def __str__(self):
        result = ""
        for i in range(len(self)):
            result += str(self[i]) + "\n"
        return result[:-1]
    def add(self, c):
        self.cells[c] = None


class Point:
    def __init__(self, p):
        self.p = p
    def __getitem__(self, key):
        return self.p[key]
    def __hash__(self):
        return int((self.p[0] + self.p[1]) * 1000)
    def __eq__(self, other):
        if (self.p[0] == other.p[0] and self.p[1] == other.p[1]):
            return True
        return False
    def __str__(self):
        return "(" + str(self.p[0]) + ", " + str(self.p[1]) + ")"

class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def __hash__(self):
        return hash(self.p1) + hash(self.p2)
    def __eq__(self, other):
        if (self.p1 == other.p1 and self.p2 == other.p2):
            return True
        if (self.p1 == other.p2 and self.p2 == other.p1):
            return True
        return False
    def __str__(self):
        return str(self.p1) + " <--> " + str(self.p2)

class Cell:
    def __init__(self, site, edges = None):
        self.site = site
        if (edges):
            self.edges = edges
        else:
            self.edges = EdgeSet()
    def add_edge(self, e):
        self.edges.add(e)
    def __hash__(self):
        result = hash(self.site)
        for e in self.edges:
            result += hash(e)
        return result
    def __eq__(self, other):
        if (self.site != other.site):
            return False
        if (len(self.edges) != len(other.edges)):
            return False
        for e in self.edges:
            if (not e in other.edges):
                return False
        return True
    def __str__(self):
        return str(self.site) + ": [" + str(self.edges) + "]"


def generate_voronoi(w, h, sites):
    S = SiteSet(sites)
    E = EdgeSet()
    C = CellSet()
    signs = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    mpx, mpy = (w / 2, h / 2)
    for i in range(4):
        x, y = signs[i]
        sx, sy = mpx, mpy
        sx += 1.5 * w * x
        sy += 1.5 * h * y
        s = Point((sx, sy))
        ps = [Point((mpx, mpy)), Point((x * 10 * w, mpy)), Point((mpx, y * 10 * h))]
        e = EdgeSet([Edge(ps[0], ps[1]), Edge(ps[1], ps[2]), Edge(ps[2], ps[0])])
        C.add(Cell(s, e))
    for c, s in enumerate(S):
        new_cell = Cell(s)
        print(c, new_cell)

points = np.random.rand(1000, 2)
sites = np_to_points(s)
r = generate_voronoi(1, 1, sites)
