# -*- coding:utf-8 -*-

from __future__ import print_function

import itertools
import collections
import random
import string
import Queue


def rand_str(n):
    return ''.join(random.sample(string.letters + string.digits, n))


def rand_graph(vnum, min_order=0, max_order=None, max_weight=10):
    vertices = set()
    # automatically check against duplicates
    while len(vertices) < vnum:
        vertices.add(rand_str(10))
    # min_order and max_order None, eq vnum, fully connected graph
    if max_order is None:
        max_order = vnum
    if min_order is None:
        min_order = vnum
    graph = {}
    for vertex in vertices:
        graph[vertex] = {}
        neighbours = random.sample(vertices, random.randint(min_order, max_order))
        # do not add itself
        if vertex in neighbours:
            neighbours.remove(vertex)
        for neighbour in neighbours:
            weight = random.randint(0, max_weight)
            graph[vertex][neighbour] = weight
    return graph

def dijkstra(graph, source):
    # init
    if source not in graph:
        raise KeyError("Source {0} not present in graph".format(source))
    dist = {}
    visited = set()
    previous = {}
    q = Queue.PriorityQueue()
    for vertex in graph.iterkeys():
        dist[vertex] = float("infinity")
        previous[vertex] = None
    dist[source] = 0
    pq_put = lambda v: q.put((dist[v], v))
    pq_put(source)
    while q.qsize():
        (current_dist, current_vertex) = q.get()
        visited.add(current_vertex)
        for (neighbour, neighbour_weight) in graph[current_vertex].iteritems():
            alt = current_dist + neighbour_weight
            if alt < dist[neighbour]:
                dist[neighbour] = alt
                previous[neighbour] = current_vertex
                if neighbour not in visited:
                    pq_put(neighbour)
    return (dist, previous)

def shortest_path(g, source, target, weight_func=lambda x:x):
    (_, p) = dijkstra(g, source)
    res = [target]
    prev = p[target]
    res.insert(0, prev)
    while prev is not None and prev != source:
        current = prev
        prev = p[current]
        res.insert(0, prev)
    return res

def out_degree(g, v):
    return len(g[v])

def in_degree(g, v):
    degree = 0
    for neighbours in g.itervalues():
        if v in neighbours:
            degree += 1
    return degree

def to_matrix(g):
    vnum = len(g)
    matrix = [[0] * vnum for _ in range(vnum)]
    m = {}
    for (number, vertex) in enumerate(g.iterkeys()):
        m[vertex] = number
    for (row_number, neighbours) in enumerate(g.itervalues()):
        for (vertex, weight) in neighbours.iteritems():
            col_number = m[vertex]
            matrix[row_number][col_number] = weight
    return matrix

def bfs(g, source):
    white = object()
    gray = object()
    black = object()
    Q = []
    colors = {}
    pred = {}
    dist = {}
    for vertex in g:
        colors[vertex] = white
        dist[vertex] = float("infinity")
        pred[vertex] = None
    colors[source] = gray
    dist[source] = 0
    Q.append(source)
    while len(Q):
        current = Q.pop(0)
        for neighbour in g[current]:
            if colors[neighbour] is white:
                colors[neighbour] = gray
                dist[neighbour] = dist[current] + 1
                pred[neighbour] = current
                Q.append(neighbour)
        colors[current] = black
    return (dist, pred)

def dfs(g):
    colors = {}
    pred = {}
    discover = {}
    finish = {}
    time = 0
    white = object()
    gray = object()
    black = object()
    def dfs_visit(g, v, time):
        # хэндлим "висячие" рёбра
        if v not in g:
            return time
        tmie = time + 1
        discover[v] = time
        colors[v] = gray
        for neighbour in g[v]:
            # и тут тоже
            if neighbour not in g:
                continue
            if colors[neighbour] is white:
                pred[neighbour] = v
                time = dfs_visit(g, neighbour, time)
        colors[v] = black
        time = time + 1
        finish[v] = time
        return time
    for vertex in g:
        colors[vertex] = white
        pred[vertex] = None
    for vertex in g:
        if colors[vertex] is white:
            time = dfs_visit(g, vertex, time)
    return (pred, discover, finish)

def generate_graph(max_num):
    from collections import defaultdict
    g = defaultdict(list)
    def algo(n):
        if not (n % 2):
            return n / 2
        else:
            return 3*n + 1
    g[1] = []
    for i in range(2, max_num + 1):
        g[i].append(algo(i))
    return dict(g)
