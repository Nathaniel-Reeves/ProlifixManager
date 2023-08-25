import os
import pytest
# from ...init_db.load_db import main as load_db
from .wsgi import create_app


@pytest.fixture()
def app():

    """
    Database Connection Settings
    """
    os.environ["DB_HOST"] = '127.0.0.1'
    os.environ["DB_PORT"] = '3306'
    os.environ["DB_USER"] = 'client'
    os.environ["DB_PASSWORD"] = "ClientPassword!5"

    os.environ["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), 'files')

    """
    Setup Database
    """

    """
    Redis Connection Settings
    """

    os.environ["REDIS_HOST"] = "127.0.0.1"
    os.environ["REDIS_PORT"] = 6379
    os.environ["REDIS_PASSWORD"] = "Am ^ 7qq?% QgedcLn"

    os.environ["API_PREFIX"] = '/api'


    """
    Create App
    """
    app = create_app()
    app.config['TESTING'] = True

    # Yield the app for testing
    yield app

    """
    Clean up testing environment
    """

    # Drop all databases

    # Delete all uploaded test files



@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_request_example(client):
    response = client.get("/ping")
    print(response)
    assert 'pong!' in response.json()

if __name__ == "__main__":
    test_request_example(client(app()))
