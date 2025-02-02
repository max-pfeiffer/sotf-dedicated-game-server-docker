"""Tests if container works."""

import socket
from datetime import date

from python_on_whales import Builder, DockerClient
from requests.auth import HTTPBasicAuth
from testcontainers.registry import DockerRegistryContainer

from build.constants import PLATFORMS
from build.utils import get_image_reference
from tests.constants import CONTEXT, REGISTRY_PASSWORD, REGISTRY_USERNAME

BASIC_AUTH: HTTPBasicAuth = HTTPBasicAuth(REGISTRY_USERNAME, REGISTRY_PASSWORD)


def test_container_run(
    docker_client: DockerClient,
    buildx_builder: Builder,
    registry_container: DockerRegistryContainer,
) -> None:
    """Test the running container.

    :param docker_client:
    :param buildx_builder:
    :return:
    """
    registry: str = registry_container.get_registry()
    date_tag: str = date.today().isoformat()
    image_reference: str = get_image_reference(registry, date_tag)

    docker_client.login(
        server=registry,
        username=REGISTRY_USERNAME,
        password=REGISTRY_PASSWORD,
    )

    docker_client.buildx.build(
        context_path=CONTEXT,
        tags=[image_reference],
        platforms=PLATFORMS,
        builder=buildx_builder,
        push=True,
    )
    with docker_client.container.run(
        image_reference,
        detach=True,
        interactive=True,
        tty=True,
        publish=[(8766, 8766), (9700, 9700), (27016, 27016)],
        envs={"SKIPNETWORKACCESSIBILITYTEST": "true"},
    ):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b"test", ("localhost", 8766))
        sock.sendto(b"test", ("localhost", 9700))
        sock.sendto(b"test", ("localhost", 27016))
