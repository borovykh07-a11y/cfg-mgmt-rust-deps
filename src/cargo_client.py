"""Получение прямых зависимостей пакета Rust (Cargo)."""
import io
import os
import tarfile
import tomllib
import urllib.request

CRATES_DOWNLOAD = (
    "https://crates.io/api/v1/crates/{name}/{version}/download"
)

_DEP_SECTIONS = (
    "dependencies",
    "dev-dependencies",
    "build-dependencies",
)


def _download_crate(name: str, version: str) -> bytes:
    """Скачивает .crate-архив пакета с crates.io."""
    url = CRATES_DOWNLOAD.format(name=name, version=version)
    request = urllib.request.Request(
        url, headers={"User-Agent": "cfg-mgmt-tool/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def _extract_cargo_toml(crate_bytes: bytes) -> bytes:
    """Извлекает Cargo.toml из tar.gz-архива .crate."""
    with tarfile.open(fileobj=io.BytesIO(crate_bytes),
                      mode="r:gz") as archive:
        for member in archive.getmembers():
            if member.name.endswith("/Cargo.toml") and \
               member.name.count("/") == 1:
                return archive.extractfile(member).read()
    raise ValueError("В .crate-архиве нет Cargo.toml")


def _dependency_names(toml_data: dict) -> set:
    """Собирает имена зависимостей из всех секций Cargo.toml."""
    names = set()
    for section in _DEP_SECTIONS:
        block = toml_data.get(section, {})
        if not isinstance(block, dict):
            continue
        for dep_name, dep_spec in block.items():
            if isinstance(dep_spec, dict):
                real_name = dep_spec.get("package", dep_name)
            else:
                real_name = dep_name
            names.add(real_name)
    return names


def _read_test_repo(package: str, path: str) -> list:
    """Читает тестовый файл графа (формат 'A -> B, C')."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Тестовый файл не найден: {path}")
    with open(path, encoding="utf-8") as handle:
        lines = [ln.strip() for ln in handle if ln.strip()]
    for line in lines:
        if line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("->")]
        if len(parts) == 2 and parts[0] == package:
            return sorted(p for p in parts[1].split(",") if p)
    raise ValueError(f"Пакет {package} отсутствует в тестовом файле")


def get_direct_dependencies(name: str, version: str,
                            repo_url: str, test_mode: bool) -> list:
    """Возвращает отсортированный список прямых зависимостей."""
    if test_mode:
        return _read_test_repo(name, repo_url)

    raw = _download_crate(name, version)
    toml_bytes = _extract_cargo_toml(raw)
    data = tomllib.loads(toml_bytes.decode("utf-8"))
    names = _dependency_names(data)
    return sorted(names)