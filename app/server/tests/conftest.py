import os
import pytest
from init_db.load_db import main as load_db
from server.wsgi import create_app


@pytest.fixture()
def app():
    """
    Database Connection Settings
    """
    SERVER_IP = '192.168.1.133'
    # SERVER_IP = '127.0.0.1'
    os.environ["DB_HOST"] = SERVER_IP
    os.environ["DB_PORT"] = '3306'
    os.environ["DB_USER"] = 'client'
    os.environ["DB_PASSWORD"] = "ClientPassword!5"

    os.environ["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), 'files')

    """
    Setup Database
    """
    os.chdir('app')
    os.chdir('init_db')
    load_db(force=True, drop_databases=False)
    os.chdir('..')
    os.chdir('..')

    """
    Redis Connection Settings
    """

    os.environ["REDIS_HOST"] = SERVER_IP
    os.environ["REDIS_PORT"] = '6379'
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
    os.chdir('app')
    os.chdir('init_db')
    load_db(force=True, drop_databases=True)
    os.chdir('..')
    os.chdir('..')

    # Delete all uploaded test files


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

if __name__ == '__main__':
    pytest.main()