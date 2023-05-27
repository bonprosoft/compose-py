#!/usr/bin/env python3

import argparse
import subprocess

import compose_py
from compose_py.models_pydantic import ComposeSpecification, Service


def create_compose(
    num_services: int,
    port_starts: int,
) -> ComposeSpecification:
    services = []
    for i in range(num_services):
        listen_port = port_starts + i
        services.append(
            Service(
                image="nginx",
                container_name=f"nginx-{i}",
                ports=[f"{listen_port}:80"],
            )
        )

    return ComposeSpecification(
        services={s.container_name: s for s in services},
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print", action="store_true")
    parser.add_argument("-s", "--port-starts", type=int, default=20080)
    parser.add_argument("-n", "--num-services", type=int, default=3)
    parser.add_argument("commands", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    port_starts: int = args.port_starts
    num_services: int = args.num_services

    compose = create_compose(
        num_services=num_services,
        port_starts=port_starts,
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
