import pytest
from main import model as db

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

            def describe_get_id():

                def it_returns_id_type_int():
                    org = db.Organization_Names()

                    assert org.get_id() == org.name_id

            def describe_get_id_name():

                def it_returns_id_name():
                    org = db.Organization_Names()

                    assert org.get_id_name() == "name_id"

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

    def describe_Users():

        def describe_Unit_Tests():

            def describe_init_Users():

                def it_is_in_the_correct_schema():
                    users = db.Users()

                    schema = users.__table_args__['schema']

                    assert schema == 'Organizations'

                def it_has_the_correct_table_name():
                    users = db.Users()

                    table_name = users.__tablename__

                    assert table_name == 'Users'

                def it_has_all_data_members():
                    users = db.Users()

                    assert hasattr(users, 'user_id')
                    assert hasattr(users, 'person_id')
                    assert hasattr(users, 'username')
                    assert hasattr(users, 'encrypted_password')
                    assert hasattr(users, 'profile_picture')
                    assert hasattr(users, 'color_theme')
                    assert hasattr(users, 'doc')

                def it_has_all_common_methods():
                    users = db.Users()

                    assert hasattr(users, 'to_dict')
                    assert hasattr(users, 'get_id')
                    assert hasattr(users, 'get_id_name')

            def describe_get_id():

                def it_returns_id_type_int():
                    user = db.Users()

                    assert user.get_id() == user.user_id

            def describe_get_id_name():

                def it_returns_id_name():
                    user = db.Users()

                    assert user.get_id_name() == "user_id"

            def describe_to_dict():

                def it_returns_correct_number_of_data_members():
                    user = db.Users()

                    data = user.to_dict()

                    assert len(list(data.keys())) == 7

                def it_returns_correct_data_keys():
                    user = db.Users()

                    data = user.to_dict()

                    assert data['user_id'] == user.user_id
                    assert data['person_id'] == user.person_id
                    assert data['username'] == user.username
                    assert data['encrypted_password'] == user.encrypted_password
                    assert data['profile_picture'] == user.profile_picture
                    assert data['color_theme'] == user.color_theme
                    assert data['doc'] == user.doc

    def describe_Facilities():

        def describe_Unit_Tests():

            def describe_init_Facilities():

                def it_is_in_the_correct_schema():
                    facilities = db.Facilities()

                    schema = facilities.__table_args__['schema']

                    assert schema == 'Organizations'

                def it_has_the_correct_table_name():
                    facilities = db.Facilities()

                    table_name = facilities.__tablename__

                    assert table_name == 'Facilities'

                def it_has_all_data_members():
                    facilities = db.Facilities()

                    assert hasattr(facilities, 'facility_id')
                    assert hasattr(facilities, 'organization_id')
                    assert hasattr(facilities, 'building_type')
                    assert hasattr(facilities, 'building_name')
                    assert hasattr(facilities,'street_1_number')
                    assert hasattr(facilities,'street_1_number_suffix')
                    assert hasattr(facilities,'street_1_name')
                    assert hasattr(facilities,'street_1_type')
                    assert hasattr(facilities,'street_1_direction')
                    assert hasattr(facilities,'street_2_number')
                    assert hasattr(facilities,'street_2_number_suffix')
                    assert hasattr(facilities,'street_2_name')
                    assert hasattr(facilities,'street_2_type')
                    assert hasattr(facilities,'street_2_direction')
                    assert hasattr(facilities, 'address_type')
                    assert hasattr(facilities, 'address_type_identifier')
                    assert hasattr(facilities, 'local_municipality')
                    assert hasattr(facilities, 'city_town')
                    assert hasattr(facilities, 'governing_district')
                    assert hasattr(facilities, 'postal_area')
                    assert hasattr(facilities, 'country')
                    assert hasattr(facilities,'ship_time')
                    assert hasattr(facilities,'ship_time_units')
                    assert hasattr(facilities,'ship_time_in_days')
                    assert hasattr(facilities, 'notes')

            def describe_get_id():

                def it_returns_id_type_int():
                    facility = db.Facilities()

                    assert facility.get_id() == facility.facility_id

            def describe_get_id_name():

                def it_returns_id_name():
                    facility = db.Facilities()

                    assert facility.get_id_name() == "facility_id"

            def describe_to_dict():

                def it_returns_correct_number_of_data_members():
                    facility = db.Facilities()

                    data = facility.to_dict()

                    assert len(list(data.keys())) == 25

                def it_returns_correct_data_keys():
                    facility = db.Facilities()

                    data = facility.to_dict()

                    assert data['facility_id'] == facility.facility_id
                    assert data['organization_id'] == facility.organization_id
                    assert data['building_type'] == facility.building_type
                    assert data['building_name'] == facility.building_name
                    assert data['street_1_number'] == facility.street_1_number
                    assert data['street_1_number_suffix'] == facility.street_1_number_suffix
                    assert data['street_1_name'] == facility.street_1_name
                    assert data['street_1_type'] == facility.street_1_type
                    assert data['street_1_direction'] == facility.street_1_direction
                    assert data['street_2_number'] == facility.street_2_number
                    assert data['street_2_number_suffix'] == facility.street_2_number_suffix
                    assert data['street_2_name'] == facility.street_2_name
                    assert data['street_2_type'] == facility.street_2_type
                    assert data['street_2_direction'] == facility.street_2_direction
                    assert data['address_type'] == facility.address_type
                    assert data['address_type_identifier'] == facility.address_type_identifier
                    assert data['local_municipality'] == facility.local_municipality
                    assert data['city_town'] == facility.city_town
                    assert data['governing_district'] == facility.governing_district
                    assert data['postal_area'] == facility.postal_area
                    assert data['country'] == facility.country
                    assert data['ship_time'] == facility.ship_time
                    assert data['ship_time_units'] == facility.ship_time_units
                    assert data['ship_time_in_days'] == facility.ship_time_in_days


