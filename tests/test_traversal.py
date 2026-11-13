"""Тесты DFS-обхода графа."""
import os
import pytest

from src.graph import load_test_graph
from src.traversal import dfs_traverse

HERE = os.path.dirname(__file__)
REPO = os.path.join(HERE, "fixtures", "test_repo.graph")


@pytest.fixture()
def graph():
    """Граф из фикстуры."""
    return load_test_graph(REPO)


def test_dfs_order(graph):
    """Порядок DFS от A корректен."""
    order = [n for n, _ in dfs_traverse(graph, "A", 10)]
    assert order[0] == "A"
    assert "B" in order and "C" in order


def test_depth_limit(graph):
    """Глубина не превышает max_depth."""
    depths = [d for _, d in dfs_traverse(graph, "A", 1)]
    assert max(depths) <= 1


def test_cycle_does_not_hang(graph):
    """Цикл B→D→E→B не приводит к зависанию."""
    order = [n for n, _ in dfs_traverse(graph, "B", 10)]
    assert order.count("B") == 1