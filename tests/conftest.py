"""Спільні фікстури: завантажують `task_N/main.py` як модулі за шляхом.

Теки `task_N` — це скрипти-демо без `__init__.py`, тож імпортуємо їх явно за
файлом. Пакет `viz`, від якого залежать деякі задачі, доступний завдяки
editable-встановленню (`pip install -e ".[dev]"`, див. README). Фікстури —
session-scoped: кожен модуль вантажиться один раз.
"""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(task: str):
    path = ROOT / task / "main.py"
    spec = importlib.util.spec_from_file_location(f"{task}_main", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def t1():
    return _load("task_1")


@pytest.fixture(scope="session")
def t2():
    return _load("task_2")


@pytest.fixture(scope="session")
def t3():
    return _load("task_3")


@pytest.fixture(scope="session")
def t4():
    return _load("task_4")


@pytest.fixture(scope="session")
def t5():
    return _load("task_5")


@pytest.fixture(scope="session")
def t6():
    return _load("task_6")


@pytest.fixture(scope="session")
def t7():
    return _load("task_7")
