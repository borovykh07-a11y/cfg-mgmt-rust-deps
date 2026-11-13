"""Вывод зависимостей в виде ASCII-дерева."""
from .graph import DependencyGraph


def _render(node: str, graph: DependencyGraph, prefix: str,
            is_last: bool, visited: set, depth: int,
            max_depth: int, lines: list) -> None:
    """Рекурсивно добавляет строки дерева."""
    connector = "└── " if is_last else "├── "
    lines.append(f"{prefix}{connector}{node}")
    if node in visited or depth >= max_depth:
        return
    visited.add(node)
    children = graph.children(node)
    if not children:
        return
    child_prefix = prefix + ("    " if is_last else "│   ")
    for index, child in enumerate(children):
        _render(child, graph, child_prefix,
                index == len(children) - 1,
                visited, depth + 1, max_depth, lines)


def render_ascii_tree(graph: DependencyGraph, root: str,
                      max_depth: int = 5) -> str:
    """Возвращает ASCII-дерево зависимостей от корня."""
    lines = [root]
    visited = {root}
    children = graph.children(root)
    for index, child in enumerate(children):
        _render(child, graph, "", index == len(children) - 1,
                visited, 1, max_depth, lines)
    return "\n".join(lines)