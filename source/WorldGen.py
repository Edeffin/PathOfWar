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
    def __repr__(self):
        return str(self)
    def add(self, p):
        self.sites[p] = None
    def to_np(self):
        result = np.zeros((len(self), 2))
        for i in range(len(self)):
            result[i, 0] = self[i][0]
            result[i, 1] = self[i][1]
        return result

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
    def __repr__(self):
        return str(self)
    def add(self, e):
        self.edges[e] = None
    def __add__(self, other):
        new_set = EdgeSet()
        for c, e in enumerate(self):
            new_set.add(e)
        for c, e in enumerate(other):
            new_set.add(e)
        return new_set
    def replace(self, old_e, new_e):
        if (not old_e in self.edges):
            return
        del self.edges[old_e]
        self.edges[new_e] = None
    def delete(self, e):
        if (not e in self.edges):
            return
        del self.edges[e]

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
    def __repr__(self):
        return str(self)
    def add(self, c):
        self.cells[c] = None
    def replace_edge(self, old_edge, new_edge):
        for c, cell in enumerate(self.cells):
            cell.edges.replace(old_edge, new_edge)
    def delete_edge(self, e):
        for c, cell in enumerate(self.cells):
            cell.edges.delete(e)


class Point:
    def __init__(self, p, py = None):
        if (py != None):
            self.p = (p, py)
        else:
            self.p = tuple(p)
        self.p = round(self.p[0], 6), round(self.p[1], 6)
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
    def __repr__(self):
        return str(self)
    def __add__(self, other):
        return Point(self[0] + other[0], self[1] + other[1])
    def __sub__(self, other):
        return Point(self[0] - other[0], self[1] - other[1])
    def __truediv__(self, factor):
        return Point(self[0] / factor, self[1] / factor)
    def __mul__(self, factor):
        return Point(self[0] * factor, self[1] * factor)
    def mag_square(self):
        return self.p[0] ** 2 + self.p[1] ** 2

class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        rs = p1 - p2
        if (rs[0] == 0):
            self.slope = float("inf")
            self.offset = p1[0]
        else:
            self.slope = rs[1] / rs[0]
            self.offset = p1[1] - self.slope * p1[0]
        self.minx = min(self.p1[0], self.p2[0])
        self.maxx = max(self.p1[0], self.p2[0])
        self.miny = min(self.p1[1], self.p2[1])
        self.maxy = max(self.p1[1], self.p2[1])
    def __getitem__(self, ind):
        return (self.p1[ind], self.p2[ind])
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
    def __repr__(self):
        return str(self)
    def in_bounds(self, p):
        if (p[0] >= self.minx - 10e-6 and p[0] <= self.maxx + 10e-6 and p[1] >= self.miny - 10e-6 and p[1] <= self.maxy + 10e-6):
            return True
        return False
    def clip_far_side(self, s, b):
        dist_p1 = (self.p1 - s).mag_square()
        dist_p2 = (self.p2 - s).mag_square()
        if (dist_p1 < dist_p2):
            return Edge(b, self.p2)
        else:
            return Edge(self.p1, b)

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
    def __repr__(self):
        return str(self)

def near_point(p, t1, t2):
    dist_p1 = (p - t1).mag_square()
    dist_p2 = (p - t2).mag_square()
    if (dist_p1 < dist_p2):
        return 1
    elif (dist_p2 < dist_p1):
        return -1
    else:
        return 0


def generate_voronoi(w, h, sites):
    plt.figure(figsize = (20, 20))
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
        s = Point(sx, sy)
        ps = [Point(mpx, mpy), Point(x * 10 * w, mpy), Point(mpx, y * 10 * h)]
        e = EdgeSet([Edge(ps[0], ps[1]), Edge(ps[1], ps[2]), Edge(ps[2], ps[0])])
        E += e
        C.add(Cell(s, e))
    for s_count, s in enumerate(S):
        new_cell = Cell(s)
        for c_count, c in enumerate(C):
            xy = (c.site + s) / 2
            axy = c.site - s
            ani = axy[1] / axy[0]
            bni = xy[1] - ani * xy[0]
            a = -1 / ani
            b = xy[1] - a * xy[0]
            critical_points = SiteSet()
            cell_edges = c.edges
            swap_edges = {}
            delete_edges = {}
            for e_count, e in enumerate(cell_edges):
                e_swap_edges = {}
                if (e.slope == float("inf")):
                    intercept = Point(e.offset, a * e.offset + b)
                else:
                    if (e.slope == a):
                        continue
                    else:
                        intercept_x = (b - e.offset) / (e.slope - a)
                    intercept = Point(intercept_x, a * intercept_x + b)
                in_seg = e.in_bounds(intercept)
                if (in_seg):
                    critical_points.add(intercept)
                    print(s_count, c_count, e_count, e, critical_points)
                    new_edge = e.clip_far_side(s, intercept)
                    swap_edges[e] = new_edge
                    e_swap_edges[e] = new_edge
                    l = np.linspace(-10, 10, 2)
                    ly = a * l + b
                    #plt.plot(l, ly, c = "purple")
                    plt.scatter(intercept[0], intercept[1], c = "b")
                else:
                    if (near_point(e.p1, s, c.site) == 1):
                        delete_edges[e] = None
            if (len(critical_points) == 2):
                new_edge = Edge(critical_points[0], critical_points[1])
                new_cell.add_edge(new_edge)
                E.add(new_edge)
            #for e in delete_edges:
                #C.delete_edge(e)
                #E.delete(e)
            #for e in swap_edges:
                #E.replace(e, swap_edges[e])
                #C.replace_edge(e, swap_edges[e])
        C.add(new_cell)

    for cc, c in enumerate(C):
        plt.scatter(*c.site, c = "y")
    for ec, e in enumerate(E):
        plt.plot(e[0], e[1], c = "r")
    #for ec, e in enumerate(E):
    #    plt.plot(e[0], e[1], c = "r")
    plt.scatter(S.to_np()[:, 0], S.to_np()[:, 1], c = "g")
    ax = plt.gca()
    ax.set_aspect("equal", "box")
    plt.savefig("debug.png")



np.random.seed(1)
points = np.random.rand(2 , 2)
sites = np_to_points(points)
r = generate_voronoi(1, 1, sites)
