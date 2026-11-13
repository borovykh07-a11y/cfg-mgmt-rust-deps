"""Точка входа CLI-приложения."""
import argparse
import sys

from .config import load_config, print_config
from .graph import load_test_graph
from .load_order import load_order
from .traversal import dfs_traverse


def build_parser() -> argparse.ArgumentParser:
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Визуализатор графа зависимостей Cargo")
    parser.add_argument("--config", required=True,
                        help="путь к INI-файлу конфигурации")
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
        if cfg.test_mode:
            graph = load_test_graph(cfg.repo_url)
            
            print("\nDFS-обход:")
            traversal = dfs_traverse(graph, cfg.package_name, 
                                     cfg.max_depth)
            for node, depth in traversal:
                print(f"  {node} (глубина {depth})")

            print("\nПорядок загрузки:")
            order = load_order(graph, cfg.package_name, 
                               cfg.max_depth)
            for name in order:
                print(f"  {name}")
        else:
            print("  (Режим реального репозитория будет в след. этапах)")
    except Exception as exc:
        print(f"Ошибка графа: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())