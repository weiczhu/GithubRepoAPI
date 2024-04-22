import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock
from app.main import app as FastAPIApp

# Constants for repeated use
REPO_ENDPOINT = "/repositories/octocat/Hello-World"
EXPECTED_FULL_NAME = "octocat/Hello-World"
EXPECTED_DESCRIPTION = "My first repository on GitHub!"
EXPECTED_CLONE_URL = "https://github.com/octocat/Hello-World.git"
EXPECTED_STARS = 2516
EXPECTED_CREATION_DATE = "2011-01-26T19:01:12"


@pytest.fixture
async def client():
    async with AsyncClient(app=FastAPIApp, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture
async def setup_mocks(mocker):
    mock_startup_event = mocker.patch("app.main.startup_event", new_callable=AsyncMock)
    mock_get_repository = mocker.patch("app.crud.RepositoryCRUD.get_repository", new_callable=AsyncMock)
    mock_add_repository = mocker.patch("app.crud.RepositoryCRUD.add_repository", new_callable=AsyncMock)
    return {
        "startup_event": mock_startup_event,
        "get_repository": mock_get_repository,
        "add_repository": mock_add_repository
    }


@pytest.mark.integration
async def test_get_repository_returns_none(setup_mocks, client):
    setup_mocks["get_repository"].return_value = None
    response = await client.get("/repositories/octocat/Hello-World")

    assert response.status_code == 200


@pytest.mark.integration
async def test_get_repository_has_cached_result(setup_mocks, client):
    setup_mocks["get_repository"].return_value = {
        "full_name": EXPECTED_FULL_NAME,
        "description": EXPECTED_DESCRIPTION,
        "clone_url": EXPECTED_CLONE_URL,
        "stars": EXPECTED_STARS,
        "created_at": EXPECTED_CREATION_DATE,
    }
    response = await client.get("/repositories/octocat/Hello-World")

    assert response.status_code == 200
    data = response.json()
    assert data["fullName"] == EXPECTED_FULL_NAME
    assert data["description"] == EXPECTED_DESCRIPTION
    assert data["cloneUrl"] == EXPECTED_CLONE_URL
    assert data["stars"] == EXPECTED_STARS
    assert data["createdAt"] == EXPECTED_CREATION_DATE
