"""Тесты загрузки конфигурации."""
import os
import tempfile
import pytest
from src.config import load_config

VALID_INI = """[main]
package_name = serde
repo_url = https://crates.io
test_mode = false
package_version = 1.0.0
output_image = out.png
ascii_tree = false
max_depth = 3
"""

def _write_tmp(content: str) -> str:
    """Пишет контент во временный файл и возвращает путь."""
    handle = tempfile.NamedTemporaryFile("w", suffix=".ini", delete=False, encoding="utf-8")
    handle.write(content)
    handle.close()
    return handle.name

def test_valid_config():
    """Валидный INI загружается без ошибок."""
    path = _write_tmp(VALID_INI)
    try:
        cfg = load_config(path)
        assert cfg.package_name == "serde"
        assert cfg.max_depth == 3
    finally:
        os.unlink(path)