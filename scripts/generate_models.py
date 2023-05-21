#!/usr/bin/env python3

import pathlib
import subprocess

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]


def convert_json_schema(
    schema_path: pathlib.Path,
    output_path: pathlib.Path,
    model_type: str = "pydantic.BaseModel",
) -> None:
    # NOTE: Don't use '--enum-field-as-literal all' to support py36,37 environments.
    subprocess.check_call(
        [
            "datamodel-codegen",
            "--input-file-type",
            "jsonschema",
            "--use-subclass-enum",
            "--capitalise-enum-members",
            "--output-model-type",
            model_type,
            "--input",
            str(schema_path),
            "--output",
            str(output_path),
        ]
    )


def main() -> None:
    convert_json_schema(
        REPOSITORY_ROOT / "third_party/compose-spec/schema/compose-spec.json",
        REPOSITORY_ROOT / "compose_py/models_pydantic/_generated.py",
    )
    convert_json_schema(
        REPOSITORY_ROOT / "third_party/compose-spec/schema/compose-spec.json",
        REPOSITORY_ROOT / "compose_py/models_dataclasses/_generated.py",
        "dataclasses.dataclass",
    )


if __name__ == "__main__":
    main()
