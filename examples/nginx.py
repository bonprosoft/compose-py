#!/usr/bin/env python3

"""
An example that shows
- Basic usage of compose_py
- How to increase the number of services programatically

"""

import argparse
import subprocess

import compose_py
from compose_py.models_pydantic import ComposeSpecification, Service


def create_compose(
    num_services: int,
    port_begin: int,
) -> ComposeSpecification:
    services = []
    for i in range(num_services):
        service_port = port_begin + i
        services.append(
            Service(
                image="nginx",
                container_name=f"nginx-{i}",
                ports=[f"{service_port}:80"],
            )
        )

    return ComposeSpecification(
        services={s.container_name: s for s in services},
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print", action="store_true")
    parser.add_argument("-s", "--port-begin", type=int, default=20080)
    parser.add_argument("-n", "--num-services", type=int, default=3)
    parser.add_argument("commands", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    port_begin: int = args.port_begin
    num_services: int = args.num_services

    compose = create_compose(
        num_services=num_services,
        port_begin=port_begin,
    )
    compose_content = compose_py.dump_yaml_str(compose)
    if args.print:
        print(compose_content)
        return

    subprocess.run(
        ["docker", "compose", "-f", "-"] + args.commands,
        input=compose_content.encode("utf-8"),
        check=True,
    )


if __name__ == "__main__":
    main()
