"""Точка входа CLI-приложения."""
import argparse
import sys

from .cargo_client import get_direct_dependencies
from .config import load_config, print_config


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

    print("\nПрямые зависимости:")
    try:
        deps = get_direct_dependencies(
            cfg.package_name, cfg.package_version,
            cfg.repo_url, cfg.test_mode)
        if not deps:
            print("  (нет зависимостей)")
        for dep in deps:
            print(f"  - {dep}")
    except Exception as exc:  # noqa: BLE001
        print(f"Ошибка получения данных: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())