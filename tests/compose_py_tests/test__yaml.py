import pathlib

from compose_py import _yaml


def test_load(simple_yml: pathlib.Path, anchor_yml: pathlib.Path) -> None:
    with simple_yml.open("r") as f:
        simple = _yaml.load(f)
    assert simple["services"]["web"]["ports"] == ["8000:5000"]

    with anchor_yml.open("r") as f:
        anchor = _yaml.load(f)
    assert anchor["services"]["web"]["ports"] == ["8000:5000"]

    # Check anchor references are resolved at `load`
    assert anchor["services"]["web"]["network"] == "hosts"
    assert anchor["services"]["redis"]["network"] == "hosts"

    # NOTE: web.command is overwritten
    assert anchor["services"]["web"]["command"] == 'echo "web"'
    assert anchor["services"]["redis"]["command"] == 'echo "common"'
