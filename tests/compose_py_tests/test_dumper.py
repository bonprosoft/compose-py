import pathlib
import tempfile

from compose_py import _yaml, models_pydantic
from compose_py.dumper import dump_dict, dump_yaml, replace_enum_with_values
from compose_py.loader import load_yaml
from compose_py.model_type import ModelType


def assert_yaml_files(expected: pathlib.Path, actual: pathlib.Path) -> None:
    expected_content = _yaml.load(expected)
    actual_content = _yaml.load(actual)

    assert expected_content == actual_content


def test_load_and_dump_yaml_pydantic(simple_yml: pathlib.Path) -> None:
    with tempfile.TemporaryDirectory() as td:
        tempdir = pathlib.Path(td)

        data_pydantic = load_yaml(simple_yml, model=ModelType.PYDANTIC)
        saved_path = tempdir / "pydantic.yml"
        dump_yaml(data_pydantic, saved_path, model=ModelType.PYDANTIC)

        assert_yaml_files(simple_yml, saved_path)

        # Check if enum is represented with its value
        data = _yaml.load(saved_path)
        assert data["services"]["redis"]["cgroup"] == "host"


def test_load_and_dump_yaml_dataclasses(simple_yml: pathlib.Path) -> None:
    with tempfile.TemporaryDirectory() as td:
        tempdir = pathlib.Path(td)
        saved_path = tempdir / "dataclasses.yml"

        data_dataclasses = load_yaml(simple_yml, model=ModelType.DATACLASSES)
        dump_yaml(data_dataclasses, saved_path, model=ModelType.DATACLASSES)

        saved_dataclasses = load_yaml(saved_path, model=ModelType.DATACLASSES)
        assert data_dataclasses == saved_dataclasses

        # Check if enum is represented with its value
        data = _yaml.load(saved_path)
        assert data["services"]["redis"]["cgroup"] == "host"


def test_replace_enum_with_values(simple_yml: pathlib.Path) -> None:
    pydantic_model = load_yaml(simple_yml, model=ModelType.PYDANTIC)
    pydantic_dict = dump_dict(pydantic_model, model=ModelType.PYDANTIC)
    assert pydantic_dict["services"]["redis"]["cgroup"] is models_pydantic.Cgroup.HOST

    converted_dict = replace_enum_with_values(pydantic_dict)
    assert converted_dict["services"]["redis"]["cgroup"] == "host"
