"""Тесты порядка загрузки."""
import os

from src.graph import load_test_graph
from src.load_order import load_order

HERE = os.path.dirname(__file__)
REPO = os.path.join(HERE, "fixtures", "test_repo.graph")


def test_dependencies_before_package():
    """Зависимости в порядке загрузки идут раньше пакета."""
    graph = load_test_graph(REPO)
    order = load_order(graph, "A", 10)
    assert order.index("E") < order.index("D")
    assert order.index("D") < order.index("B")
    assert order[-1] == "A"