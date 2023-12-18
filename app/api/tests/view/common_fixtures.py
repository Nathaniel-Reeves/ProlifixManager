import json
import pytest

from main.wsgi import create_app
from main.view.response import CustomResponse
from controller import organizations as org
from view import auth as auth

todo = pytest.mark.skip("todo")

@pytest.fixture
def api_url():
    return "/api/v1"

@pytest.fixture
def when_logged_in(mocker):
    user_data_template = {
        "department": "",
        "doc": {},
        "first_name": "",
        "job_description": "",
        "last_name": "",
        "organization_id": 0,
        "person_id": 0,
        "profile_picture": "",
        "user_id": "1",
        "username": "username",
        "encrypted_password": "encrypted_password"
    }
    mocker.patch("redis.Redis")
    mocker.patch("redis.client.Redis.ping")
    mocker.patch.object(auth,"get_session_token", return_value="session_token")
    mocker.patch("redis.client.Redis.exists", return_value=True)
    mocker.patch("redis.client.Redis.get", return_value=json.dumps(user_data_template))
    mocker.patch("flask.Response.set_cookie")

@pytest.fixture
def when_not_logged_in(mocker):
    user_data_template = {
        "department": "",
        "doc": {},
        "first_name": "",
        "job_description": "",
        "last_name": "",
        "organization_id": 0,
        "person_id": 0,
        "profile_picture": "",
        "user_id": "",
        "username": "username",
        "encrypted_password": "encrypted_password"
    }
    mocker.patch("redis.Redis")
    mocker.patch("redis.client.Redis.ping")
    mocker.patch.object(auth,"get_session_token", return_value="session_token")
    mocker.patch("redis.client.Redis.exists", return_value=True)
    mocker.patch("redis.client.Redis.get", return_value=json.dumps(user_data_template))
    mocker.patch("flask.Response.set_cookie")