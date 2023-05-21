import enum
import os
import typing
from typing import Any, Dict, Literal, Optional, TypeVar, cast, overload

from . import _yaml
from .model_type import ModelType

ComposeSpecification = Any
TObj = TypeVar("TObj")

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
    path: os.PathLike,
    *,
    model: Literal[ModelType.PYDANTIC],
    simplify: bool = ...,
    dumper: Optional[_yaml.DumperType] = ...,
) -> None:
    ...


@overload
def dump_yaml(
    obj: "models_dataclasses.ComposeSpecification",
    path: os.PathLike,
    *,
    model: Literal[ModelType.DATACLASSES],
    simplify: bool = ...,
    dumper: Optional[_yaml.DumperType] = ...,
) -> None:
    ...


@overload
def dump_yaml(
    obj: ComposeSpecification,
    path: os.PathLike,
    *,
    model: ModelType,
    simplify: bool = ...,
    dumper: Optional[_yaml.DumperType] = ...,
) -> None:
    ...


def dump_yaml(
    obj: ComposeSpecification,
    path: os.PathLike,
    *,
    model: ModelType = ModelType.PYDANTIC,
    simplify: bool = True,
    dumper: Optional[_yaml.DumperType] = None,
) -> None:
    data = dump_dict(obj, model=model, simplify=simplify)
    data = replace_enum_with_values(data)
    _yaml.dump(data, path, dumper=dumper)


def replace_enum_with_values(obj: TObj) -> TObj:
    if isinstance(obj, enum.Enum):
        ret = obj.value
    elif isinstance(obj, dict):
        ret = {
            replace_enum_with_values(k): replace_enum_with_values(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        ret = [replace_enum_with_values(v) for v in obj]
    else:
        ret = obj

    return cast(TObj, ret)
