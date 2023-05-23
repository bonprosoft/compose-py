import pathlib

from compose_py import models_dataclasses, models_pydantic
from compose_py.loader import load_yaml, load_yaml_str
from compose_py.model_type import ModelType


def test_load_yaml_pydantic(simple_yml: pathlib.Path) -> None:
    with simple_yml.open("r") as f:
        data_pydantic = load_yaml(f, model=ModelType.PYDANTIC)
    assert isinstance(data_pydantic, models_pydantic.ComposeSpecification)
    services = data_pydantic.services
    assert services is not None
    assert len(services) == 2
    # Check if enum class is used
    redis: models_pydantic.Service = next(
        s for k, s in services.items() if k == "redis"
    )
    assert redis.cgroup is models_pydantic.Cgroup.HOST


def test_load_yaml_dataclasses(simple_yml: pathlib.Path) -> None:
    with simple_yml.open("r") as f:
        data_dataclasses = load_yaml(f, model=ModelType.DATACLASSES)
    assert isinstance(data_dataclasses, models_dataclasses.ComposeSpecification)
    services = data_dataclasses.services
    assert services is not None
    assert len(services) == 2
    # Check if enum class is used
    redis: models_dataclasses.Service = next(
        s for k, s in services.items() if k == "redis"
    )
    assert redis.cgroup is models_dataclasses.Cgroup.HOST


def test_load_yaml_str(simple_yml: pathlib.Path) -> None:
    content = simple_yml.read_text()
    data_from_str = load_yaml_str(content, model=ModelType.PYDANTIC)
    assert isinstance(data_from_str, models_pydantic.ComposeSpecification)
    services = data_from_str.services
    assert services is not None
    assert len(services) == 2

    with simple_yml.open("r") as f:
        data_from_fs = load_yaml(f, model=ModelType.PYDANTIC)
    assert data_from_str == data_from_fs
