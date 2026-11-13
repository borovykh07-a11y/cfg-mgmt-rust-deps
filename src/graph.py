"""Структура графа зависимостей и его загрузка."""
import os


class DependencyGraph:
    """Направленный граф «пакет → его прямые зависимости»."""

    def __init__(self) -> None:
        """Создаёт пустой граф."""
        self._edges = {}

    def add_node(self, node: str) -> None:
        """Добавляет узел без рёбер (если его ещё нет)."""
        self._edges.setdefault(node, [])

    def add_edge(self, src: str, dst: str) -> None:
        """Добавляет ребро src → dst."""
        self.add_node(src)
        self.add_node(dst)
        if dst not in self._edges[src]:
            self._edges[src].append(dst)

    def children(self, node: str) -> list:
        """Возвращает прямых зависимостей узла."""
        return list(self._edges.get(node, []))


def load_test_graph(path: str) -> DependencyGraph:
    """Загружает граф из текстового файла вида 'A -> B, C'.

    :raises FileNotFoundError: если файл не существует.
    :raises ValueError: при некорректном формате строки.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Файл графа не найден: {path}")
    
    graph = DependencyGraph()
    with open(path, encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            
            parts = line.split("->")
            if len(parts) != 2:
                raise ValueError(
                    f"Строка {line_no}: ожидался формат 'A -> B, C'")
            
            src = parts[0].strip()
            if not src.isalpha() or not src.isupper():
                raise ValueError(
                    f"Строка {line_no}: имя '{src}' не заглавные буквы")
                
            for dst in parts[1].split(","):
                dst = dst.strip()
                if not dst:
                    continue
                if not dst.isalpha() or not dst.isupper():
                    raise ValueError(
                        f"Строка {line_no}: имя '{dst}' "
                        f"не заглавные буквы")
                graph.add_edge(src, dst)
    return graph