"""Точка входа CLI-приложения."""
import argparse
import sys

from .ascii_tree import render_ascii_tree
from .config import load_config, print_config
from .graph import load_test_graph
from .load_order import load_order
from .traversal import dfs_traverse
from .visualize import render_png, to_mermaid


def build_parser() -> argparse.ArgumentParser:
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Визуализатор графа зависимостей Cargo")
    parser.add_argument("--config", required=True,
                        help="путь к INI-файлу")
    return parser


def main(argv=None) -> int:
    """Запускает приложение. Возвращает код выхода."""
    args = build_parser().parse_args(argv)
    try:
        cfg = load_config(args.config)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Ошибка конфигурации: {exc}", file=sys.stderr)
        return 1

    print_config(cfg)

    try:
        graph = load_test_graph(cfg.repo_url)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Ошибка графа: {exc}", file=sys.stderr)
        return 1

    traversal = dfs_traverse(graph, cfg.package_name, cfg.max_depth)
    print("\nDFS-обход:")
    for node, depth in traversal:
        print(f"  {node} (глубина {depth})")

    order = load_order(graph, cfg.package_name, cfg.max_depth)
    print("\nПорядок загрузки:")
    for name in order:
        print(f"  {name}")

    if cfg.ascii_tree:
        print("\nASCII-дерево:")
        print(render_ascii_tree(graph, cfg.package_name,
                                cfg.max_depth))

    mermaid = to_mermaid(graph, cfg.package_name)
    try:
        render_png(mermaid, cfg.output_image)
        print(f"\nPNG сохранён: {cfg.output_image}")
    except RuntimeError as exc:
        print(f"\n{exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())