"""Basic test fixtures."""

import pytest
from python_on_whales import Builder, DockerClient
from testcontainers.registry import DockerRegistryContainer

from tests.constants import REGISTRY_PASSWORD, REGISTRY_USERNAME


@pytest.fixture(scope="session")
def docker_client() -> DockerClient:
    """Provide the Python on Whales docker client.

    :return:
    """
    return DockerClient(debug=True)


@pytest.fixture(scope="session")
def buildx_builder(docker_client: DockerClient) -> Builder:
    """Provide a Pyhton on Whales BuildX builder instance.

    :param docker_client:
    :return:
    """
    builder: Builder = docker_client.buildx.create(
        driver="docker-container", driver_options=dict(network="host")
    )
    yield builder
    docker_client.buildx.stop(builder)
    docker_client.buildx.remove(builder)


@pytest.fixture(scope="session")
def registry_container(docker_client: DockerClient) -> DockerRegistryContainer:
    """Fixture providing a Docker registry container instance.

    :param docker_client:
    :return:
    """
    with DockerRegistryContainer(
        username=REGISTRY_USERNAME, password=REGISTRY_PASSWORD
    ).with_bind_ports(5000, 5000) as registry_container:
        yield registry_container
