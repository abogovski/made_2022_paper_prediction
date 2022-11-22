from collections import deque


def dfs(_graph, _v, _color, _current_color):
    stack = [_v]

    while stack:
        vertex = stack.pop()
        if _color[vertex] != 0:
            continue
        _color[vertex] = _current_color
        for neighbor in _graph[vertex]:
            stack.append(neighbor)


def components(_graph):
    colors = [0 for _ in range(len(_graph))]
    current_color = 0
    for v in range(len(_graph)):
        if colors[v] == 0:
            current_color += 1
            dfs(_graph, v, colors, current_color)

    return colors


def bfs(_graph, _v, _connected_component=None, lim=None):
    """
    Breadth-first search
    stopping on lim
    """
    q = deque()
    _discovered = [False for _ in range(len(_graph))]
    _discovered[_v] = True
    q.append(_v)
    step = 0
    while q:
        if lim and step > lim:
            break
        _v = q.popleft()
        for u in _graph[_v]:
            if _connected_component and u in _connected_component:
                if lim and step > lim:
                    break
                if not _discovered[u]:
                    step += 1
                    _discovered[u] = True
                    q.append(u)
    res = []
    for i in range(len(_discovered)):
        if _discovered[i]:
            res.append(i)
    return res
