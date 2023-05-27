#!/usr/bin/env python3

"""
An example that shows
- Usage of the builder pattern to construct service definitions
- The advantages of putting initialization logic along with a composite
  specification into a single script (See: `initialize()` method)

"""

from __future__ import annotations

import argparse
import subprocess
from typing import List, Union

import compose_py
from compose_py.models_pydantic import ComposeSpecification, Network, Service, Volume1

ROS_MASTER_URI = "http://ros-master:11311"


class ServiceBuilder:
    def __init__(self, name: str, image: str, network: Network):
        self._environment: List[str] = []
        self._volumes: List[Union[str, Volume1]] = []
        self._service = Service(
            container_name=name,
            image=image,
            networks=[network.name],
            restart="always",
        )

    def with_x(self) -> ServiceBuilder:
        self._environment.append("DISPLAY")
        self._environment.append("QT_X11_NO_MITSHM=1")
        self._volumes.append(
            Volume1(type="bind", source="/tmp/.X11-unix", target="/tmp/.X11-unix")
        )
        return self

    def with_command(self, command: str) -> ServiceBuilder:
        self._service.command = command
        return self

    def with_ros(self) -> ServiceBuilder:
        self._environment.append(f"ROS_MASTER_URI={ROS_MASTER_URI}")
        return self

    def depends_on(self, *services: Service) -> ServiceBuilder:
        container_names: List[str] = []
        for s in services:
            name = s.container_name
            assert name is not None
            container_names.append(name)
        self._service.depends_on = container_names
        return self

    def build(self) -> Service:
        service = self._service.copy()
        service.environment = self._environment.copy()
        service.volumes = self._volumes.copy()
        return service


def create_compose() -> ComposeSpecification:
    network = Network(name="ros", driver="bridge")
    master = (
        ServiceBuilder("ros-master", "ros:noetic-ros-core", network)
        .with_command("roscore")
        .build()
    )
    publisher = (
        ServiceBuilder("publisher", "ros:noetic-ros-core", network)
        .with_ros()
        .depends_on(master)
        .with_command(
            "rostopic pub /my_point geometry_msgs/PointStamped "
            "'{header: {stamp: now, frame_id: \"map\"}, point: [1, 1, 1]}' -r 1 -s"
        )
        .build()
    )
    subscriber = (
        ServiceBuilder("subscriber", "ros:noetic-ros-core", network)
        .with_ros()
        .depends_on(master)
        .with_command("rostopic echo /my_point")
        .build()
    )
    rviz = (
        ServiceBuilder("rviz", "osrf/ros:noetic-desktop-full", network)
        .with_ros()
        .depends_on(master)
        .with_x()
        .with_command("rviz")
        .build()
    )
    networks = [network]
    services = [master, publisher, subscriber, rviz]
    return ComposeSpecification(
        networks={n.name: n for n in networks},
        services={s.container_name: s for s in services},
    )


def initialize() -> None:
    # Disable access control of X to host GUI applications in a container
    subprocess.check_call(["xhost", "+"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print", action="store_true")
    parser.add_argument("commands", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    compose = create_compose()
    compose_content = compose_py.dump_yaml_str(compose)
    if args.print:
        print(compose_content)
        return

    initialize()
    subprocess.run(
        ["docker", "compose", "-f", "-"] + args.commands,
        input=compose_content.encode("utf-8"),
        check=True,
    )


if __name__ == "__main__":
    main()
