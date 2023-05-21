import pathlib

import pytest

BASE_DIR = pathlib.Path(__file__).resolve().parent


@pytest.fixture
def data_dir() -> pathlib.Path:
    return BASE_DIR / "data"


@pytest.fixture
def simple_yml(data_dir: pathlib.Path) -> pathlib.Path:
    return data_dir / "simple.yml"


@pytest.fixture
def anchor_yml(data_dir: pathlib.Path) -> pathlib.Path:
    return data_dir / "anchor.yml"
