import pytest
from fastapi.testclient import TestClient

from app.main import get_application


@pytest.fixture(scope="module")
def app_client():
    # set up
    app = get_application()

    with TestClient(app) as test_client:
        yield test_client
    # tear down
