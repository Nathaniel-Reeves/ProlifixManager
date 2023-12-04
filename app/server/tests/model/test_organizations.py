import pytest
from server import model as db

notImplemented = pytest.mark.skip(reason="Not yet implemented")
def describe_Organizations_Schema():
    
    def describe_oranizations():
        
        def describe_Unit_Tests():
        
            def describe_init_Organizations():
                
                def it_is_in_the_correct_schema():
                    org = db.Organizations()
                    
                    schema = org.__table_args__['schema']
                    
                    assert schema == 'Organizations'
                
                def it_has_the_correct_table_name():
                    org = db.Organizations()
                    
                    table_name = org.__tablename__
                    
                    assert table_name == 'Organizations'
                
                def it_has_all_data_members():
                    org = db.Organizations()
                    
                    assert hasattr(org, 'organization_id')
                    assert hasattr(org, 'date_entered')
                    assert hasattr(org, 'website_url')
                    assert hasattr(org, 'vetted')
                    assert hasattr(org, 'risk_level')
                    assert hasattr(org, 'supplier')
                    assert hasattr(org, 'lab')
                    assert hasattr(org, 'courier')
                    assert hasattr(org, 'other')
                    assert hasattr(org, 'doc')
                    
                def it_has_all_common_methods():
                    org = db.Organizations()
                    
                    assert hasattr(org, 'to_dict')
                    assert hasattr(org, 'get_id')
                    assert hasattr(org, 'get_id_name')
                
                def it_has_all_relationships_members():
                    org = db.Organizations()
                    
                    assert hasattr(org, 'organization_names')
                    assert hasattr(org, 'people')
                    assert hasattr(org, 'facilities')
            
            def describe_to_dict():
                
                def it_returns_correct_number_of_data_members():
                    org = db.Organizations()
                    
                    data = org.to_dict()
                    
                    assert len(list(data.keys())) == 12
                
                def it_returns_correct_data_keys():
                    org = db.Organizations()
                    
                    data = org.to_dict()
                    
                    assert data['organization_id'] == org.organization_id
                    assert data['website_url'] == org.website_url
                    assert data['vetted'] == org.vetted
                    assert data['date_vetted'] == org.date_vetted
                    assert data['date_entered'] == org.date_entered
                    assert data['risk_level'] == org.risk_level
                    assert data['supplier'] == org.supplier
                    assert data['client'] == org.client
                    assert data['lab'] == org.lab
                    assert data['courier'] == org.courier
                    assert data['other'] == org.other
                    assert data['doc'] == org.doc
            
            def describe_get_id():
                
                def it_returns_id_type_int():
                    org = db.Organizations()
                    
                    assert org.get_id() == org.organization_id
            
            def describe_get_id_name():
                
                def it_returns_id_name():
                    org = db.Organizations()
                    
                    assert org.get_id_name() == "organization_id"
                
    def describe_Organization_Names():
        
        def describe_init_Organization_Names():
            
            def describe_Unit_Tests():
            
                def it_is_in_the_correct_schema():
                    org_name = db.Organization_Names()
                    
                    schema = org_name.__table_args__['schema']
                    
                    assert schema == 'Organizations'
                
                def it_has_the_correct_table_name():
                    org_name = db.Organization_Names()
                    
                    table_name = org_name.__tablename__
                    
                    assert table_name == 'Organization_Names'
                
                def it_has_all_data_members():
                    org_name = db.Organization_Names()
                    
                    assert hasattr(org_name, 'name_id')
                    assert hasattr(org_name, 'organization_id')
                    assert hasattr(org_name, 'organization_initial')
                    assert hasattr(org_name, 'organization_name')
                    assert hasattr(org_name, 'primary_name')
                
                def it_has_all_common_methods():
                    org_name = db.Organization_Names()
                    
                    assert hasattr(org_name, 'to_dict')
                    assert hasattr(org_name, 'get_id')
                    assert hasattr(org_name, 'get_id_name')
                
    def describe_People():
        
        def describe_Unit_Tests():
            
            def describe_init_People():
                
                def it_is_in_the_correct_schema():
                    people = db.People()
                    
                    schema = people.__table_args__['schema']
                    
                    assert schema == 'Organizations'
                
                def it_has_the_correct_table_name():
                    people = db.People()
                    
                    table_name = people.__tablename__
                    
                    assert table_name == 'People'
                
                def it_has_all_data_members():
                    people = db.People()
                    
                    assert hasattr(people, 'person_id')
                    assert hasattr(people, 'organization_id')
                    assert hasattr(people, 'first_name')
                    assert hasattr(people, 'last_name')
                    assert hasattr(people, 'date_entered')
                    assert hasattr(people, 'job_description')
                    assert hasattr(people, 'department')
                    assert hasattr(people, 'phone_number_primary')
                    assert hasattr(people, 'phone_number_secondary')
                
                def it_has_all_common_methods():
                    people = db.People()
                    
                    assert hasattr(people, 'to_dict')
                    assert hasattr(people, 'get_id')
                    assert hasattr(people, 'get_id_name')

    @notImplemented
    def describe_Users():
        pass

    @notImplemented
    def describe_Facilities():
        pass
