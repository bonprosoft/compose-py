# compose-py

A Python library for parsing and loading [Compose](https://github.com/compose-spec/compose-spec) files

## Installation

```sh
pip install compose-py
```

By default, the library doesn't have any dependencies for dataclass libraries.
Choose 'pydantic' or 'dataclasses' and install the library.
We also provide `extras` for the libraries:
```sh
# If you prefer Pydantic models
pip install "compose-py[pydantic]"

# If you prefer dataclasses models
pip install "compose-py[dataclasses]"
```

## Tutorial: Load, modify, and save docker-compose.yml

### Pydantic.BaseModel (default)

```py
import compose_py

obj = compose_py.load_yaml("docker-compose.yml")
print(obj)  # Prints 'compose_py.models_pydantic.ComposeSpecification(...)'
print(obj.services["web"])  # Prints 'compose_py.models_pydantic.Service(...)'

# Copy and modify the existing service, then add it to the specification
web2 = obj.services["web"].copy()
web2.command = '--port 8081'
obj.services["web2"] = web2

compose_py.dump_yaml(obj, "docker-compose-modified.yml")
```

You can find more APIs under `compose_py.models_pydantic` package.

### dataclasses.dataclass

```py
import compose_py

obj = compose_py.load_yaml("docker-compose.yml", model=compose_py.ModelType.DATACLASSES)
print(obj)  # Prints 'compose_py.models_dataclasses.ComposeSpecification(...)'
print(obj.services["web"])  # Prints 'compose_py.models_dataclasses.Service(...)'

# Copy and modify the existing service, then add it to the specification
web2 = obj.services["web"].copy()
web2.command = '--port 8081'
obj.services["web2"] = web2

compose_py.dump_yaml(obj, "docker-compose-modified.yml", model=compose_py.ModelType.DATACLASSES)
```

You can find more APIs under `compose_py.models_dataclasses` package.

