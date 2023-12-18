import json
import pytest
import sqlalchemy

from main.wsgi import create_app
from main.view.response import CustomResponse
from main.controller import organizations as org

todo = pytest.mark.skip("todo")

def describe_get_organizations():
    
    def describe_required_args():
        
        @todo
        def it_throws_a_type_err_with_no_args(mocker):
            mock_select = mocker.patch('sqlalchemy.sql.selectable.Select', return_value = "")
            mock_join = mocker.patch('sqlalchemy.sql.selectable.Select.join', return_value = "")
            mock_where = mocker.patch('sqlalchemy.sql.selectable.Select.where', return_value = "")
            mock_get_session = mocker.patch('main.model.connector.get_session', return_value = '')
            
            try:
                org.get_organizations()
            except Exception as e:
                assert isinstance(e, TypeError)
                
            mock_select.assert_called_once()
            mock_join.assert_called_once()
            # mock_where.assert_called_once()
            mock_get_session.assert_called_once()
        
        @todo
        def it_works_with_correct_args(mocker):
            mock_select = mocker.patch("sqlalchemy.sql.expression.select", return_value = sqlalchemy.sql.selectable.Select)
            mock_join = mocker.patch.object(sqlalchemy.sql.selectable.Select, "join", return_value = sqlalchemy.sql.selectable.Select)
            mock_where = mocker.patch.object(sqlalchemy.sql.selectable.Select, "where", return_value = sqlalchemy.sql.selectable.Select)
            mock_get_session = mocker.patch('main.model.connector.get_session', return_value = '')
            
            org.get_organizations(CustomResponse(), [], [], [], False)
                
            mock_select.assert_called_once()
            mock_join.assert_called_once()
            # mock_where.assert_called_once()
            mock_get_session.assert_called_once()
        