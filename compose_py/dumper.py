import enum
import io
import typing
from typing import Any, Dict, Optional, TextIO, TypeVar, cast, overload

from . import _yaml
from .model_type import ModelType

ComposeSpecification = Any
TObj = TypeVar("TObj")

if typing.TYPE_CHECKING:
    from typing import Literal

    from . import models_dataclasses, models_pydantic


@overload
def dump_dict(
    obj: "models_pydantic.ComposeSpecification",
    *,
    model: "Literal[ModelType.PYDANTIC]" = ...,
    simplify: bool = ...,
) -> Dict[str, Any]:
    ...


@overload
def dump_dict(
    obj: "models_dataclasses.ComposeSpecification",
    *,
    model: "Literal[ModelType.DATACLASSES]",
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
    stream: TextIO,
    *,
    model: "Literal[ModelType.PYDANTIC]" = ...,
    simplify: bool = ...,
    dumper: Optional[_yaml.DumperType] = ...,
) -> None:
    ...


@overload
def dump_yaml(
    obj: "models_dataclasses.ComposeSpecification",
    stream: TextIO,
    *,
    model: "Literal[ModelType.DATACLASSES]",
    simplify: bool = ...,
    dumper: Optional[_yaml.DumperType] = ...,
) -> None:
    ...


@overload
def dump_yaml(
    obj: ComposeSpecification,
    stream: TextIO,
    *,
    model: ModelType,
    simplify: bool = ...,
    dumper: Optional[_yaml.DumperType] = ...,
) -> None:
    ...


def dump_yaml(
    obj: ComposeSpecification,
    stream: TextIO,
    *,
    model: ModelType = ModelType.PYDANTIC,
    simplify: bool = True,
    dumper: Optional[_yaml.DumperType] = None,
) -> None:
    data = dump_dict(obj, model=model, simplify=simplify)
    data = replace_enum_with_values(data)
    _yaml.dump(data, stream, dumper=dumper)


@overload
def dump_yaml_str(
    obj: "models_pydantic.ComposeSpecification",
    *,
    model: "Literal[ModelType.PYDANTIC]" = ...,
    simplify: bool = ...,
    dumper: Optional[_yaml.DumperType] = ...,
) -> str:
    ...


@overload
def dump_yaml_str(
    obj: "models_dataclasses.ComposeSpecification",
    *,
    model: "Literal[ModelType.DATACLASSES]",
    simplify: bool = ...,
    dumper: Optional[_yaml.DumperType] = ...,
) -> str:
    ...


@overload
def dump_yaml_str(
    obj: ComposeSpecification,
    *,
    model: ModelType,
    simplify: bool = ...,
    dumper: Optional[_yaml.DumperType] = ...,
) -> str:
    ...


def dump_yaml_str(
    obj: ComposeSpecification,
    *,
    model: ModelType = ModelType.PYDANTIC,
    simplify: bool = True,
    dumper: Optional[_yaml.DumperType] = None,
) -> str:
    with io.StringIO() as buf:
        dump_yaml(
            obj,
            stream=buf,
            model=model,
            simplify=simplify,
            dumper=dumper,
        )
        return buf.getvalue()


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
