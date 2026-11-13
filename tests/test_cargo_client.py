"""Тесты парсинга зависимостей Cargo."""
import io
import tarfile

from src.cargo_client import (_dependency_names,
                              _extract_cargo_toml)


def _make_crate(toml_text: str) -> bytes:
    """Создаёт .crate-архив в памяти."""
    data = toml_text.encode("utf-8")
    info = tarfile.TarInfo("demo-1.0.0/Cargo.toml")
    info.size = len(data)
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        archive.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


def test_dependency_names():
    """Собирает имена из [dependencies] и [build-dependencies]."""
    names = _dependency_names(
        {"dependencies": {"serde": "1.0",
                          "renamed": {"package": "real-crate",
                                      "version": "0.2"}},
         "build-dependencies": {"cc": "1.0"}})
    assert names == {"serde", "real-crate", "cc"}


def test_extract_cargo_toml():
    """Извлекает Cargo.toml из корректного архива."""
    crate = _make_crate("[package]\nname = \"demo\"\n")
    toml_bytes = _extract_cargo_toml(crate)
    assert b"[package]" in toml_bytes