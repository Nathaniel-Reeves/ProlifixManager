import pytest

from main.wsgi import create_app
from main.controler import organizations as org
from main.view.response import CustomResponse

app = create_app()

def describe_Organizations_Enpoints():
    
    def describe_Unit_Tests():
        
        @pytest.fixture
        def mock_controler_get_organizations(mocker):
            response = CustomResponse()
            response.set_status_code(200)
            return mocker.patch.object(org,
                    "get_organizations", 
                    return_value=response
                )
        
        @pytest.fixture
        def when_logged_in(mocker):
            mocker.patch(
                    "redis.Redis", 
                    return_value="fake_connection"
                )
            mocker.patch(
                    "redis.Redis.ping",
                    return_value=True
                )
            mocker.patch(
                    "flask.request.cookies.get",
                    return_value=True
                )
            mocker.patch.object(
                    "session_token",
                    return_value=True
                )
            mocker.patch.object(
                    "redis_connection.exists()",
                    return_value=True
                )
            mocker.patch.object(
                    "create_session()",
                    return_value="fake_session"
                )

        def describe_api_orgnaizations():
            
            def it_exists(when_logged_in, mock_controler_get_organizations):
                url = '/api/organizations'
                response = app.test_client().get(url)
                
                assert response.status_code == 200