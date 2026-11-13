"""Модуль загрузки и валидации INI-конфигурации."""
import configparser
import os
from dataclasses import dataclass

SEMVER_PARTS = 3
MIN_DEPTH = 1

@dataclass
class Config:
    """Настраиваемые пользователем параметры."""
    package_name: str
    repo_url: str
    test_mode: bool
    package_version: str
    output_image: str
    ascii_tree: bool
    max_depth: int

def _parse_bool(raw: str, key: str) -> bool:
    """Преобразует строку в bool или бросает ValueError."""
    value = raw.strip().lower()
    if value in ("true", "1", "yes"):
        return True
    if value in ("false", "0", "no"):
        return False
    raise ValueError(f"Параметр '{key}' должен быть true/false, получено: {raw!r}")

def _parse_int(raw: str, key: str) -> int:
    """Преобразует строку в int или бросает ValueError."""
    try:
        value = int(raw.strip())
    except ValueError as exc:
        raise ValueError(f"Параметр '{key}' должен быть целым, получено: {raw!r}") from exc
    return value

def load_config(path: str) -> Config:
    """Читает INI-файл и возвращает валидированный Config.
    :raises FileNotFoundError: файл не найден.
    :raises ValueError: параметр отсутствует или невалиден.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Конфиг не найден: {path}")

    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")
    if "main" not in parser:
        raise ValueError("В INI отсутствует секция [main]")

    section = parser["main"]
    required = ["package_name", "repo_url", "test_mode", "package_version", 
                "output_image", "ascii_tree", "max_depth"]
    for key in required:
        if key not in section:
            raise ValueError(f"В [main] отсутствует ключ '{key}'")

    package_name = section["package_name"].strip()
    if not package_name:
        raise ValueError("package_name не может быть пустым")

    repo_url = section["repo_url"].strip()
    if not repo_url:
        raise ValueError("repo_url не может быть пустым")
    if not (repo_url.startswith("http://") or repo_url.startswith("https://") or os.path.exists(repo_url)):
        raise ValueError(f"repo_url должен быть URL или существующим путём: {repo_url!r}")

    version = section["package_version"].strip()
    parts = version.split(".")
    if len(parts) != SEMVER_PARTS or not all(p.isdigit() for p in parts):
        raise ValueError(f"package_version должен быть semver (X.Y.Z): {version!r}")

    output_image = section["output_image"].strip()
    if not output_image.lower().endswith(".png"):
        raise ValueError(f"output_image должен оканчиваться на .png: {output_image!r}")

    test_mode = _parse_bool(section["test_mode"], "test_mode")
    ascii_tree = _parse_bool(section["ascii_tree"], "ascii_tree")
    max_depth = _parse_int(section["max_depth"], "max_depth")
    
    if max_depth < MIN_DEPTH:
        raise ValueError("max_depth должен быть >= 1")

    return Config(package_name=package_name, repo_url=repo_url, test_mode=test_mode,
                  package_version=version, output_image=output_image,
                  ascii_tree=ascii_tree, max_depth=max_depth)

def print_config(cfg: Config) -> None:
    """Выводит все параметры в формате ключ-значение."""
    for field_name, field_value in cfg.__dict__.items():
        print(f"{field_name} = {field_value}")