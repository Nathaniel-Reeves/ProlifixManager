import pytest

from server.controler import organizations as org
from server.wsgi import create_app
from server import view

app = create_app()

def describe_Organizations_Enpoints():
    
    def describe_Unit_Tests():
        
        @pytest.fixture
        def mock_controler_get_organizations(mocker):
            responce = view.CustomResponse()
            responce.set_status_code(200)
            return mocker.patch(
                    "org.get_organizations()", 
                    return_value=responce
                )
        
        # @pytest.fixture
        # def when_logged_in(mocker):
        #     mocker.patch.object(
        #             "Redis", 
        #             return_value="fake_connection"
        #         )
        #     mocker.patch.object(
        #             "redis_connection.ping()",
        #             return_value=True
        #         )
        #     mocker.patch.object(
        #             "request.cookies.get()",
        #             return_value=True
        #         )
        #     mocker.patch.object(
        #             "session_token",
        #             return_value=True
        #         )
        #     mocker.patch.object(
        #             "redis_connection.exists()",
        #             return_value=True
        #         )
        #     mocker.patch.object(
        #             "create_session()",
        #             return_value="fake_session"
        #         )

        def describe_api_orgnaizations():
            
            def it_exists(mocker, mock_controler_get_organizations):
                url = '/api/organizations'
                response = app.test_client().get(url)
                
                assert response.status_code == 200