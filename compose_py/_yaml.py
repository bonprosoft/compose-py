import pathlib
import typing
from typing import Any, Dict, Optional, Type, Union

import yaml

from ._types import Path

DumperType = Any

if typing.TYPE_CHECKING:
    from yaml.cyaml import _CLoader
    from yaml.loader import _Loader

    LoaderClass = Union[_Loader, _CLoader]
    LoaderType = Type[LoaderClass]
else:
    LoaderClass = Any
    LoaderType = Any


def ensure_pathlib_obj(p: Path) -> pathlib.Path:
    return pathlib.Path(p)


def load(
    path: Path,
    *,
    loader: Optional[LoaderType] = None,
) -> Dict[str, Any]:
    path = ensure_pathlib_obj(path)
    loader = loader or yaml.SafeLoader
    with path.open("r") as f:
        data: Dict[str, Any] = yaml.load(f, Loader=loader)
        return data


def dump(
    obj: Any,
    path: Path,
    *,
    dumper: Optional[DumperType] = None,
) -> None:
    path = ensure_pathlib_obj(path)
    dumper = dumper or yaml.SafeDumper
    with path.open("w") as f:
        yaml.dump(obj, f, Dumper=dumper)
