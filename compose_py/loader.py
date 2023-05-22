import typing
from typing import Any, Dict, Optional, overload

from . import _yaml
from ._types import Path
from .model_type import ModelType

ComposeSpecification = Any

if typing.TYPE_CHECKING:
    from typing import Literal

    from . import models_dataclasses, models_pydantic


@overload
def load_dict(
    data: Dict[str, Any],
    *,
    model: "Literal[ModelType.PYDANTIC]" = ...,
) -> "models_pydantic.ComposeSpecification":
    ...


@overload
def load_dict(
    data: Dict[str, Any],
    *,
    model: "Literal[ModelType.DATACLASSES]",
) -> "models_dataclasses.ComposeSpecification":
    ...


@overload
def load_dict(data: Dict[str, Any], *, model: ModelType) -> ComposeSpecification:
    ...


def load_dict(
    data: Dict[str, Any],
    *,
    model: ModelType = ModelType.PYDANTIC,
) -> ComposeSpecification:
    if model is ModelType.PYDANTIC:
        from . import models_pydantic

        return models_pydantic.load_dict(data)
    elif model is ModelType.DATACLASSES:
        from . import models_dataclasses

        return models_dataclasses.load_dict(data)


@overload
def load_yaml(
    path: Path,
    *,
    model: "Literal[ModelType.PYDANTIC]" = ...,
    loader: Optional[_yaml.LoaderType] = ...,
) -> "models_pydantic.ComposeSpecification":
    ...


@overload
def load_yaml(
    path: Path,
    *,
    model: "Literal[ModelType.DATACLASSES]",
    loader: Optional[_yaml.LoaderType] = ...,
) -> "models_dataclasses.ComposeSpecification":
    ...


@overload
def load_yaml(
    path: Path,
    *,
    model: ModelType,
    loader: Optional[_yaml.LoaderType] = ...,
) -> ComposeSpecification:
    ...


def load_yaml(
    path: Path,
    *,
    model: ModelType = ModelType.PYDANTIC,
    loader: Optional[_yaml.LoaderType] = None,
) -> ComposeSpecification:
    data = _yaml.load(path, loader=loader)
    return load_dict(data, model=model)
