import pytest

from server import model as db
from server.controler import organizations as org
from server.wsgi import create_app
from server import view

app = create_app()

def describe_Organizations_Enpoints():
    
    def describe_Unit_Tests():
        
        @pytest.fixture
        def mock_controler_get_organizations(mocker):
            return mocker.patch.object(org.get_organizations, return_value=view.CustomResponse(status_code=200))
        
        def describe_api_orgnaizations():
            
            def it_exists():
                response = app.test_client().get('/api/organizations')
                
                assert response.status_code == 308