"""Точка входа CLI-приложения."""
import argparse
import sys
from .config import load_config, print_config

def build_parser() -> argparse.ArgumentParser:
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Визуализатор графа зависимостей Cargo")
    parser.add_argument("--config", required=True, help="путь к INI-файлу конфигурации")
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
    return 0

if __name__ == "__main__":
    sys.exit(main())