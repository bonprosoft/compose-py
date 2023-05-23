import typing
from typing import Any, Dict, Optional, TextIO, Type, Union

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
    stream: TextIO,
    *,
    loader: Optional[LoaderType] = None,
) -> Dict[str, Any]:
    loader = loader or yaml.SafeLoader
    data: Dict[str, Any] = yaml.load(stream, Loader=loader)
    return data


def dump(
    obj: Any,
    stream: TextIO,
    *,
    dumper: Optional[DumperType] = None,
) -> None:
    dumper = dumper or yaml.SafeDumper
    yaml.dump(obj, stream, Dumper=dumper)
