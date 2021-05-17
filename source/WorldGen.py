import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue

def np_to_points(p):
    l = []
    for i in range(p.shape[0]):
        l += [Point(p[i, :])]
    return l

class SiteSet:
    def __init__(self, sites):
        self.sites = {}
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

class EdgeSet:
    def __init__(self, edges):
        self.edges = {}
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

class CellSet:
    def __init__(self, cells):
        self.cells = {}
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


class Point:
    def __init__(self, p):
        self.p = p
    def __getitem__(self, key):
        return self.p[key]
    def __hash__(self):
        return int(self.p.sum() * 1000)
    def __eq__(self, other):
        if ((self.p == other.p).all()):
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
    def __init__(self, site, edges):
        self.site = site
        self.edges = edges
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
        return str(self.site) + ": " + str(self.edges)


class Voronoi:
    def __init__(self, w, h, sites):
        pass

s = np.random.rand(1000, 2)
sp = np_to_points(s)
ss = SiteSet(sp)
e = [Edge(ss[0], ss[5]), Edge(ss[65], ss[93]), Edge(ss[2], ss[234])]
es = EdgeSet(e)
c = [Cell(ss[1], es), Cell(ss[2], es), Cell(ss[3], es)]
cs = CellSet(c)
print(cs)
for c, v in enumerate(cs):
    print(c, v)
