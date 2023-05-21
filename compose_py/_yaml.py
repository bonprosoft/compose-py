import pathlib
import typing
from typing import Any, Dict, Optional, Type, Union

import yaml

DumperType = Any

if typing.TYPE_CHECKING:
    from yaml.cyaml import _CLoader
    from yaml.loader import _Loader

    LoaderClass = Union[_Loader, _CLoader]
    LoaderType = Type[LoaderClass]
else:
    LoaderClass = Any
    LoaderType = Any


def load(
    path: pathlib.Path,
    *,
    loader: Optional[LoaderType] = None,
) -> Dict[str, Any]:
    loader = loader or yaml.SafeLoader
    with path.open("r") as f:
        data: Dict[str, Any] = yaml.load(f, Loader=loader)
        return data


def dump(
    obj: Any,
    path: pathlib.Path,
    *,
    dumper: Optional[DumperType] = None,
) -> None:
    dumper = dumper or yaml.Dumper
    with path.open("w") as f:
        yaml.dump(obj, f, Dumper=dumper)
