import pathlib
import tempfile

from compose_py import _yaml, models_pydantic
from compose_py.dumper import (
    dump_dict,
    dump_yaml,
    dump_yaml_str,
    replace_enum_with_values,
)
from compose_py.loader import load_yaml
from compose_py.model_type import ModelType


def assert_yaml_files(expected: pathlib.Path, actual: pathlib.Path) -> None:
    with expected.open("r") as f:
        expected_content = _yaml.load(f)
    with actual.open("r") as f:
        actual_content = _yaml.load(f)

    assert expected_content == actual_content


def test_load_and_dump_yaml_pydantic(simple_yml: pathlib.Path) -> None:
    with tempfile.TemporaryDirectory() as td:
        tempdir = pathlib.Path(td)
        saved_path = tempdir / "pydantic.yml"

        with simple_yml.open("r") as f:
            data_pydantic = load_yaml(f, model=ModelType.PYDANTIC)
        with saved_path.open("w") as f:
            dump_yaml(data_pydantic, f, model=ModelType.PYDANTIC)

        assert_yaml_files(simple_yml, saved_path)

        # Check if enum is represented with its value
        with saved_path.open("r") as f:
            data = _yaml.load(f)
        assert data["services"]["redis"]["cgroup"] == "host"


def test_load_and_dump_yaml_dataclasses(simple_yml: pathlib.Path) -> None:
    with tempfile.TemporaryDirectory() as td:
        tempdir = pathlib.Path(td)
        saved_path = tempdir / "dataclasses.yml"

        with simple_yml.open("r") as f:
            data_dataclasses = load_yaml(f, model=ModelType.DATACLASSES)
        with saved_path.open("w") as f:
            dump_yaml(data_dataclasses, f, model=ModelType.DATACLASSES)
        with saved_path.open("r") as f:
            saved_dataclasses = load_yaml(f, model=ModelType.DATACLASSES)
        assert data_dataclasses == saved_dataclasses

        # Check if enum is represented with its value
        with saved_path.open("r") as f:
            data = _yaml.load(f)
        assert data["services"]["redis"]["cgroup"] == "host"


def test_dump_yaml_str(simple_yml: pathlib.Path) -> None:
    with simple_yml.open("r") as f:
        data_pydantic = load_yaml(f, model=ModelType.PYDANTIC)

    content = dump_yaml_str(data_pydantic, model=ModelType.PYDANTIC)
    with tempfile.TemporaryDirectory() as td:
        tempdir = pathlib.Path(td)
        saved_path = tempdir / "pydantic.yml"

        saved_path.write_text(content)
        assert_yaml_files(simple_yml, saved_path)


def test_replace_enum_with_values(simple_yml: pathlib.Path) -> None:
    with simple_yml.open("r") as f:
        pydantic_model = load_yaml(f, model=ModelType.PYDANTIC)
    pydantic_dict = dump_dict(pydantic_model, model=ModelType.PYDANTIC)
    assert pydantic_dict["services"]["redis"]["cgroup"] is models_pydantic.Cgroup.HOST

    converted_dict = replace_enum_with_values(pydantic_dict)
    assert converted_dict["services"]["redis"]["cgroup"] == "host"
