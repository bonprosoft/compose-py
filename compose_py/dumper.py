import pathlib
import typing
from typing import Any, Dict, Literal, Optional, overload

from . import _yaml
from .model_type import ModelType

ComposeSpecification = Any

if typing.TYPE_CHECKING:
    from . import models_dataclasses, models_pydantic


@overload
def dump_dict(
    obj: "models_pydantic.ComposeSpecification",
    *,
    model: Literal[ModelType.PYDANTIC],
    simplify: bool = ...,
) -> Dict[str, Any]:
    ...


@overload
def dump_dict(
    obj: "models_dataclasses.ComposeSpecification",
    *,
    model: Literal[ModelType.DATACLASSES],
    simplify: bool = ...,
) -> Dict[str, Any]:
    ...


@overload
def dump_dict(obj: Any, *, model: ModelType, simplify: bool) -> Dict[str, Any]:
    ...


def dump_dict(
    obj: ComposeSpecification,
    *,
    model: ModelType = ModelType.PYDANTIC,
    simplify: bool = True,
) -> Dict[str, Any]:
    if model is ModelType.PYDANTIC:
        from . import models_pydantic

        return models_pydantic.dump_dict(obj, simplify=simplify)
    elif model is ModelType.DATACLASSES:
        from . import models_dataclasses

        return models_dataclasses.dump_dict(obj, simplify=simplify)


@overload
def dump_yaml(
    obj: "models_pydantic.ComposeSpecification",
    path: pathlib.Path,
    *,
    model: Literal[ModelType.PYDANTIC],
    simplify: bool = ...,
    dumper: Optional[_yaml.DumperType] = ...,
) -> None:
    ...


@overload
def dump_yaml(
    obj: "models_dataclasses.ComposeSpecification",
    path: pathlib.Path,
    *,
    model: Literal[ModelType.DATACLASSES],
    simplify: bool = ...,
    dumper: Optional[_yaml.DumperType] = ...,
) -> None:
    ...


@overload
def dump_yaml(
    obj: ComposeSpecification,
    path: pathlib.Path,
    *,
    model: ModelType,
    simplify: bool = ...,
    dumper: Optional[_yaml.DumperType] = ...,
) -> None:
    ...


def dump_yaml(
    obj: ComposeSpecification,
    path: pathlib.Path,
    *,
    model: ModelType = ModelType.PYDANTIC,
    simplify: bool = True,
    dumper: Optional[_yaml.DumperType] = None,
) -> None:
    data = dump_dict(obj, model=model, simplify=simplify)
    _yaml.dump(data, path, dumper=dumper)