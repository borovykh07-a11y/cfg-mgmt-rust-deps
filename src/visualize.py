"""Генерация Mermaid-диаграммы и её рендеринг в PNG."""
import os
import subprocess
import tempfile

from .graph import DependencyGraph


def to_mermaid(graph: DependencyGraph, root: str) -> str:
    """Строит текст Mermaid-диаграммы для графа."""
    lines = ["graph TD"]
    seen = set()
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node in seen:
            continue
        seen.add(node)
        for child in graph.children(node):
            edge = f"    {node} --> {child}"
            if edge not in lines:
                lines.append(edge)
            queue.append(child)
    return "\n".join(lines)


def _mmdc_available() -> bool:
    """Проверяет наличие mermaid-cli."""
    try:
        subprocess.run(["mmdc", "--version"],
                       capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def render_png(mermaid_text: str, output_path: str) -> None:
    """Рендерит Mermaid-диаграмму в PNG через mmdc.

    Если mmdc недоступен — сохраняет .mmd рядом с целью и
    бросает RuntimeError.
    """
    with tempfile.NamedTemporaryFile(
            "w", suffix=".mmd", delete=False,
            encoding="utf-8") as handle:
        handle.write(mermaid_text)
        mmd_path = handle.name
    try:
        if not _mmdc_available():
            fallback = os.path.splitext(output_path)[0] + ".mmd"
            with open(fallback, "w", encoding="utf-8") as fb:
                fb.write(mermaid_text)
            raise RuntimeError(
                "mermaid-cli (mmdc) не установлен. "
                f"Диаграмма сохранена в {fallback}. "
                "Установите: npm i -g @mermaid-js/mermaid-cli")
        subprocess.run(
            ["mmdc", "-i", mmd_path, "-o", output_path],
            check=True)
    finally:
        os.unlink(mmd_path)