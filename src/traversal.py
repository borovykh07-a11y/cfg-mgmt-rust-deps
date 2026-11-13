"""Обход графа зависимостей алгоритмом DFS (рекурсивный)."""
from .graph import DependencyGraph


def _dfs(node: str, graph: DependencyGraph, depth: int,
         max_depth: int, visited: set, on_stack: set,
         result: list) -> None:
    """Рекурсивный обход DFS от узла node."""
    if node in visited:
        return
    if depth > max_depth:
        return

    visited.add(node)
    on_stack.add(node)
    result.append((node, depth))

    for child in graph.children(node):
        if child in on_stack:
            continue
        _dfs(child, graph, depth + 1, max_depth,
             visited, on_stack, result)

    on_stack.discard(node)


def dfs_traverse(graph: DependencyGraph, start: str,
                 max_depth: int) -> list:
    """Возвращает список (узел, глубина) в порядке DFS.

    :param graph: граф зависимостей
    :param start: стартовый пакет
    :param max_depth: максимальная глубина
    """
    visited = set()
    on_stack = set()
    result = []
    _dfs(start, graph, 0, max_depth, visited, on_stack, result)
    return result