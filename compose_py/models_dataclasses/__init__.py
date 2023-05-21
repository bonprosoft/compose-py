import dataclasses
import enum
from typing import Any, Dict, Optional, Type, TypeVar, overload

import dacite

from ._generated import *  # NOQA
from ._generated import ComposeSpecification

TModel = TypeVar("TModel")


@overload
def load_dict(
    data: Dict[str, Any],
    *,
    config: Optional[dacite.Config] = ...,
) -> ComposeSpecification:
    ...


@overload
def load_dict(
    data: Dict[str, Any],
    data_class: Type[TModel],
    *,
    config: Optional[dacite.Config] = ...,
) -> TModel:
    ...


# NOTE: Use Any for data_class and return type to avoid the following issue:
# https://github.com/python/mypy/issues/3737
def load_dict(
    data: Dict[str, Any],
    data_class: Any = None,
    *,
    config: Optional[dacite.Config] = None,
) -> Any:
    data_class = data_class or ComposeSpecification
    config = config or dacite.Config(cast=[enum.Enum])
    return dacite.from_dict(data_class=data_class, data=data, config=config)


def dump_dict(
    obj: Any,
    **kwargs: Any,
) -> Dict[str, Any]:
    return dataclasses.asdict(obj)
