import json
import pytest

from main.wsgi import create_app
from main.view.response import CustomResponse
from controller import organizations as org
from view import auth as auth

todo = pytest.mark.skip("todo")

def describe_Organizations_Enpoints():
    
    def describe_Unit_Tests():
        
        @pytest.fixture
        def mock_controller__get_organizations(mocker):
            custom_response = CustomResponse()
            custom_response.set_status_code(200)
            fake_data = {
                "1": {
                    "organization_id": 1,
                    "organization_name": "Organization 1"
                },
                "2": {
                    "organization_id": 2,
                    "organization_name": "Organization 2"
                }
            }
            custom_response.insert_data(fake_data)
            
            mock_get_organizations = mocker.patch.object(org,"get_organizations", return_value=custom_response)
            return mock_get_organizations
        
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

        def describe_api_orgnaizations():
            
            def it_exists(mocker, when_logged_in, mock_controller__get_organizations):
                mock_get_organizations = mock_controller__get_organizations

                # Stimulate Test
                app = create_app()
                client = app.test_client()
                url = '/api/organizations/'
                response = client.get(url)
                
                # Assert Response
                mock_get_organizations.assert_called_once()
                assert response.status_code == 200
            
            def it_requires_authentication(mocker, when_not_logged_in, mock_controller__get_organizations):
                mock_get_organizations = mock_controller__get_organizations
                
                # Stimulate Test
                app = create_app()
                client = app.test_client()
                url = '/api/organizations/'
                response = client.get(url)
                
                # Assert Response
                assert response.status_code == 401
                mock_get_organizations.assert_not_called()
            
            def it_returns_json(mocker, when_logged_in, mock_controller__get_organizations):
                mock_get_organizations = mock_controller__get_organizations
                
                # Stimulate Test
                app = create_app()
                client = app.test_client()
                url = '/api/organizations/'
                response = client.get(url)
                
                # Assert Response
                assert response.status_code == 200
                assert response.content_type == 'application/json'
            
            def it_returns_custom_response_format(mocker, when_logged_in, mock_controller__get_organizations):
                # Setup
                mock_get_organizations = mock_controller__get_organizations
                app = create_app()
                client = app.test_client()
                
                # Stimulate Test
                url = '/api/organizations/'
                response = client.get(url)
                
                # Assert Response
                assert response.status_code == 200
                assert response.content_type == 'application/json'
                assert "data" in response.json.keys()
                assert "messages" in response.json.keys()
                assert "flash" in response.json["messages"]
                assert "form" in response.json["messages"]
            
            def describe_endpoint_handles_specific_organization_ids():
                
                def it_handles_a_single_organization(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()

                    # Stimulate Test
                    url = 'api/organizations/?org-id=1'
                    response = client.get(url)

                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [1],    # org_ids
                        [],     # org_types
                        [],     # populate
                        False    # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_handles_multiple_organizations(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?org-id=1&org-id=2'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [1,2],  # org_ids
                        [],     # org_types
                        [],     # populate
                        False    # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_cleans_queries(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?org-id=1&org-id=injection&org-id=3'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [1,3],  # org_ids
                        [],     # org_types
                        [],     # populate
                        False    # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
            
            def describe_endpoint_handles_specific_organization_types():
                
                def it_filters_by_client(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?org-type=client'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],                 # org_ids
                        ['client'],         # org_types
                        [],                 # populate
                        False                # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_filters_by_supplier(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?org-type=supplier'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],                 # org_ids
                        ['supplier'],       # org_types
                        [],                 # populate
                        False                # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_filters_by_lab(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?org-type=lab'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],                 # org_ids
                        ['lab'],           # org_types
                        [],                 # populate
                        False                # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_filters_by_courier(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?org-type=courier'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],                 # org_ids
                        ['courier'],       # org_types
                        [],                 # populate
                        False                # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_filters_by_more_than_one_organization_type(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?org-type=client&org-type=supplier'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],                     # org_ids
                        ['client','supplier'],  # org_types
                        [],                     # populate
                        False                    # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_filters_by_all(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?org-type=client&org-type=supplier&org-type=lab&org-type=courier&org-type=client'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],     # org_ids
                        [],     # org_types
                        [],     # populate
                        False    # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_cleans_queries(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?org-type=injection'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],                 # org_ids
                        [],                 # org_types
                        [],                 # populate
                        False                # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
            
            def describe_endpoint_handles_populating_organization_data():
                
                def it_handles_populating_organization_facilites_data(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?populate=facilities'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    print(args)
                    expected_args = [
                        CustomResponse(),
                        [],                 # org_ids
                        [],                 # org_types
                        ['facilities'],     # populate
                        False                # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_handles_populating_organization_sales_orders_data(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?populate=sales-orders'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],                 # org_ids
                        [],                 # org_types
                        ['sales-orders'],   # populate
                        False                # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_handles_populating_organization_purchase_orders_data(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?populate=purchase-orders'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],                     # org_ids
                        [],                     # org_types
                        ['purchase-orders'],    # populate
                        False                    # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_handles_populating_organization_people_data(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?populate=people'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],             # org_ids
                        [],             # org_types
                        ['people'],     # populate
                        False            # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_handles_populating_organization_components_data(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?populate=components'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],                 # org_ids
                        [],                 # org_types
                        ['components'],     # populate
                        False                # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_handles_populating_organization_products_data(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?populate=products'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],             # org_ids
                        [],             # org_types
                        ['products'],   # populate
                        False            # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_handles_populating_more_than_one_field(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_controller__get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?populate=facilities&populate=sales-orders'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_controller__get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],                 # org_ids
                        [],                 # org_types
                        ['facilities','sales-orders'],     # populate
                        False                # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_handles_populating_organization_all_data(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_controller__get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?populate=facilities&populate=sales-orders&populate=purchase-orders&populate=people&populate=components&populate=products'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_controller__get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],                 # org_ids
                        [],                 # org_types
                        ['facilities','sales-orders', 'purchase-orders', 'people', 'components', 'products'],     # populate
                        False                # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_cleans_queries(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?populate=facilities&populate=Injection&populate=purchase-orders'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],                 # org_ids
                        [],                 # org_types
                        ['facilities', 'purchase-orders'],     # populate
                        False                # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
            
            def describe_enpoint_handles_filtering_doc():
                
                def it_defaluts_to_excluding_doc(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],             # org_ids
                        [],             # org_types
                        [],             # populate
                        False            # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200
                
                def it_includes_doc_when_queried(mocker, when_logged_in, mock_controller__get_organizations):
                    # Setup
                    mock_get_organizations = mock_controller__get_organizations
                    app = create_app()
                    client = app.test_client()
                    
                    # Stimulate Test
                    url = 'api/organizations/?doc=true'
                    response = client.get(url)
                    
                    # Assert Response
                    args = mock_get_organizations.call_args_list[0][0]
                    expected_args = [
                        CustomResponse(),
                        [],             # org_ids
                        [],             # org_types
                        [],             # populate
                        True            # doc
                    ]
                    
                    assert args[1] == expected_args[1]
                    assert args[2] == expected_args[2]
                    assert args[3] == expected_args[3]
                    assert args[4] == expected_args[4]
                    assert response.status_code == 200