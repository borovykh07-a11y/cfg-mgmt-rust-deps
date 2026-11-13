"""Определение порядка загрузки зависимостей (post-order DFS)."""
from .graph import DependencyGraph


def _visit(node: str, graph: DependencyGraph, depth: int,
           max_depth: int, visiting: set, visited: set,
           order: list) -> None:
    """Рекурсивный post-order обход узла."""
    if node in visited:
        return
    if depth > max_depth:
        return
    if node in visiting:
        return

    visiting.add(node)
    for child in graph.children(node):
        _visit(child, graph, depth + 1, max_depth,
               visiting, visited, order)
    visiting.discard(node)
    visited.add(node)
    order.append(node)


def load_order(graph: DependencyGraph, start: str,
               max_depth: int) -> list:
    """Возвращает порядок загрузки: зависимости раньше пакета.

    :param graph: граф зависимостей
    :param start: стартовый пакет
    :param max_depth: ограничение глубины
    """
    order = []
    _visit(start, graph, 0, max_depth, set(), set(), order)
    return order