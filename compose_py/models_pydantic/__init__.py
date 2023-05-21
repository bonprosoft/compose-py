from typing import Any, Dict, Type, TypeVar, overload

import pydantic

from ._generated import *  # NOQA
from ._generated import ComposeSpecification

TModel = TypeVar("TModel", bound=pydantic.BaseModel)


@overload
def load_dict(data: Dict[str, Any]) -> ComposeSpecification:
    ...


@overload
def load_dict(data: Dict[str, Any], data_class: Type[TModel]) -> TModel:
    ...


# NOTE: Use Any for data_class and return type to avoid the following issue:
# https://github.com/python/mypy/issues/3737
def load_dict(
    data: Dict[str, Any],
    data_class: Any = None,
) -> Any:
    data_class = data_class or ComposeSpecification
    return data_class(**data)


def dump_dict(
    obj: pydantic.BaseModel,
    *,
    simplify: bool = True,
    **kwargs: Any,
) -> Dict[str, Any]:
    options: Dict[str, Any] = {}
    if simplify:
        options["exclude_unset"] = True
        options["exclude_none"] = True

    options.update(kwargs)
    return obj.dict(**options)
