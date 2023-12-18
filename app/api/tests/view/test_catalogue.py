import json
import pytest

from main.wsgi import create_app
from main.view.response import CustomResponse
from main.controller import catalogue as cat
from view import auth as auth
from .common_fixtures import *

todo = pytest.mark.skip("todo")

def describe_Components_Endpoints():
    
    def describe_Unit_Tests():
        
        @pytest.fixture
        def mock_controller__get_components(mocker):
            custom_response = CustomResponse()
            custom_response.status_code = 200
            fake_data = {
                "1": {
                    "component_id": "1",
                    "component_type": "powder"
                },
                "2": {
                    "component_id": "2",
                    "component_type": "liquid"
                }
            }
            custom_response.insert_data(fake_data)
            
            mock_get_components = mocker.patch.object(cat, 'get_components', return_value=custom_response)
            return mock_get_components
        
        def describe_api_components():
            
            def it_exists(mocker, api_url, when_logged_in,
                          mock_controller__get_components):
                mock_get_components = mock_controller__get_components
                
                # Stimulate Test
                app = create_app()
                client = app.test_client()
                url = api_url + '/catalogue/components/'
                response = client.get(url)
                
                # Assert Response
                assert response.status_code == 200