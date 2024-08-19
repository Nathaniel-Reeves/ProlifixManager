from view.response import CustomResponse, FlashMessage, error_message
import json
import model as db
import sqlalchemy as sa
from flask import current_app as app
import datetime

from sqlalchemy import select, update

def get_session():
    """
    Define the MariaDb engine using MariaDB Connector/Python.
    """
    host = app.config['DB_HOST']
    port = app.config['DB_PORT']
    user = app.config['DB_USER']
    password = app.config['DB_PASSWORD']

    engine = sa.create_engine(
            f'mariadb+mariadbconnector://{user}:{password}@{host}:{port}',connect_args={'connect_timeout': 3}
        )

    Session = sa.orm.sessionmaker()
    Session.configure(bind=engine)
    Session.configure(autocommit=False)
    Session = Session()
    return Session

def execute_query(custom_response, stm):
    raw_data = []

    # Connect to the database
    try:
        session = get_session()
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(500)
        return custom_response, raw_data, False

    # Execute the query
    try:
        stream = session.execute(stm)
        if isinstance(stm, sa.sql.selectable.Select):
            raw_data = stream.all()
        else:
            session.commit()
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(400)
        session.close()
        return custom_response, raw_data, False

    session.close()
    return custom_response, raw_data, True

def order_66(request):
    custom_response = CustomResponse()

    # custom_response = fix_primary_name_id_column_organizations(custom_response)
    # custom_response = fix_primary_name_id_column_components(custom_response)
    # custom_response = fix_product_master(custom_response)
    # custom_response = fix_old_components_template(custom_response)
    # custom_response = fix_org_doc(custom_response)

    if custom_response.status_code == 200:
        fm = FlashMessage(
            message='Success',
            title='Order 66'
        )
        print('SUCCESS')
        custom_response.insert_flash_message(fm)

    return custom_response

def fix_primary_name_id_column_components(custom_response):
    stm = select(db.Components)
    stm = stm.where(db.Components.primary_name_id == None)
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    for row in raw_data:
        stm = select(db.Component_Names)
        stm = stm.where(db.Component_Names.component_id == row[0].get_id())
        stm = stm.where(db.Component_Names.primary_name == True)
        custom_response, raw_data, success = execute_query(custom_response, stm)
        if not success:
            return custom_response

        if raw_data:
            primary_name_id = raw_data[0][0].get_id()
        else:
            print("No primary name found for component_id: ", row[0].get_id())
            continue

        stm = update(db.Components) \
            .values(primary_name_id=primary_name_id) \
            .where(db.Components.component_id == row[0].get_id())

        custom_response, raw_data, success = execute_query(custom_response, stm)
        if not success:
            return custom_response

    return custom_response

def fix_primary_name_id_column_organizations(custom_response):
    stm = select(db.Organizations)
    stm = stm.where(db.Organizations.primary_name_id == None)
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    for row in raw_data:
        stm = select(db.Organization_Names)
        stm = stm.where(db.Organization_Names.organization_id == row[0].get_id())
        stm = stm.where(db.Organization_Names.primary_name == True)
        custom_response, raw_data, success = execute_query(custom_response, stm)
        if not success:
            return custom_response

        if raw_data:
            primary_name_id = raw_data[0][0].get_id()
        else:
            print("No primary name found for organization_id: ", row[0].get_id())
            continue

        stm = update(db.Organizations) \
            .values(primary_name_id=primary_name_id) \
            .where(db.Organizations.organization_id == row[0].get_id())

        custom_response, raw_data, success = execute_query(custom_response, stm)
        if not success:
            return custom_response

    return custom_response

PRODUCT_DOC = {
  "labels": {
    "date_issued": None,
    "date_revised": None,
    "notes": None,
    "num_label_versions": 0,
    "num_pouch_versions": 0,
    "num_carton_versions": 0,
    "num_promotional_versions": 0,
    "all_labels": []
  },
  "formula_files": [],
  "manufacturing_files": [],
  "specifications": {
    "date_issued": '',
    "date_revised": '',
    "file_pointer": '',
    "revision_number": 0,
    "id_code": '',
    "description_statement": '',
    "identity_statement": 'This ingredient is identified by in house organoleptic specs and microscopy specs.',
    "purity_statement": 'This finished product is verified for purity via Certificate of Analysis and microscopy observation (checking for contaminating particles.) Both the raw powders and finished blended powder are tested in this way. We verify the supplier of every raw ingredient through a reviewed questionnaire and test the supplier\'s certificate of analysis on a random/skip lot basis.',
    "strength_statement": 'Strength is not relevant to this ingredient.',
    "origin": '',
    "parts_used": '',
    "specs": {
      "example_cofas": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "id_code": '',
        "locations": {
          "in_house": True,
          "primary": 'in_house',
          "supplier": True,
          "third_party_lab": False
        },
        "required_spec": True,
        "revision_number": 0,
        "test_name": 'Reference CofA\'s',
        "tests": []
      },
      "mesh_size": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "id_code": '',
        "locations": {
          "in_house": True,
          "primary": 'in_house',
          "supplier": True,
          "third_party_lab": True
        },
        "required_spec": False,
        "revision_number": 0,
        "statement": 'While mesh size testing can vary across supplier C of A\'s, the coarsest powder in this finished product is tested using a _____ mesh, with ____ % passing through. This is reflected in our in house microscopy testing. There should be no extraneous foreign objects (microscopically or visible to the naked eye), granulating agents, fillers or excipients in this finished product without express disclosure on the label.',
        "test_name": 'Mesh Size',
        "tests": []
      },
      "ftir": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "locations": {
          "in_house": False,
          "primary": 'supplier',
          "supplier": True,
          "third_party_lab": True
        },
        "required_spec": False,
        "revision_number": 0,
        "id_code": '',
        "statement": 'FTIR testing is not required for this finished product. The individual powders that compose this product may have been identity tested using FTIR and this will be specified on the supplier\'s C of A.',
        "test_name": 'FTIR',
        "methods": [
          'FTIR'
        ],
        "tests": []
      },
      "gluten": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "locations": {
          "in_house": False,
          "primary": 'supplier',
          "supplier": True,
          "third_party_lab": True
        },
        "required_spec": False,
        "revision_number": 0,
        "id_code": '',
        "statement": 'While a gluten spec is not required for this finished product, if the suppliers provides a C of A with gluten testing, we\'ll accept the specs below.',
        "test_name": 'Gluten',
        "tests": []
      },
      "heavy_metals": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "locations": {
          "in_house": False,
          "primary": 'supplier',
          "supplier": True,
          "third_party_lab": True
        },
        "required_spec": False,
        "revision_number": 0,
        "id_code": '',
        "statement": 'While heavy metals specs are not required, if there are suspicions regarding powder/the supplier, we will test this finished product (and/or its composite ingredients) to verify quality. On these occasions we will accept the specs below.',
        "test_name": 'Heavy Metals',
        "tests": [
          {
            "test_name": 'Arsenic (As)',
            "statement": '',
            "magnification": '',
            "required_spec": False,
            "method": '',
            "methods": [],
            "unit_of_measure": 'ppm',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          },
          {
            "test_name": 'Cadmium (Cd)',
            "statement": '',
            "magnification": '',
            "required_spec": False,
            "method": '',
            "methods": [],
            "unit_of_measure": 'ppm',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          },
          {
            "test_name": 'Lead (Pb)',
            "statement": '',
            "magnification": '',
            "required_spec": False,
            "method": '',
            "methods": [],
            "unit_of_measure": 'ppm',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          },
          {
            "test_name": 'Mercury (Hg)',
            "statement": '',
            "magnification": '',
            "required_spec": False,
            "method": '',
            "methods": [],
            "unit_of_measure": 'ppm',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          },
          {
            "test_name": 'Total Heavy Metals',
            "statement": '',
            "magnification": '',
            "required_spec": False,
            "method": '',
            "methods": [],
            "unit_of_measure": 'ppm',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          }
        ]
      },
      "hplc": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "locations": {
          "in_house": False,
          "primary": 'supplier',
          "supplier": True,
          "third_party_lab": True
        },
        "required_spec": False,
        "revision_number": 0,
        "id_code": '',
        "statement": 'HPLC testing is not required for this finished product. The individual powders that compose this product may have been identity tested using HPLC and this will be specified on the supplier\'s C of A.',
        "test_name": 'HPLC',
        "methods": [
          'HPLC'
        ],
        "tests": []
      },
      "hptlc": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "locations": {
          "in_house": False,
          "primary": 'supplier',
          "supplier": True,
          "third_party_lab": True
        },
        "required_spec": False,
        "revision_number": 0,
        "id_code": '',
        "statement": 'HPTLC testing is not required for this finished product. The individual powders that compose this product may have been identity tested using HPTLC and this will be specified on the supplier\'s C of A.',
        "test_name": 'HPTLC',
        "tests": []
      },
      "microbiological": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "locations": {
          "in_house": False,
          "primary": 'supplier',
          "supplier": True,
          "third_party_lab": True
        },
        "required_spec": True,
        "revision_number": 0,
        "id_code": '',
        "statement": '',
        "test_name": 'Microbiological',
        "tests": [
          {
            "test_name": 'Aerobic Plate Count',
            "statement": '',
            "magnification": '',
            "required_spec": True,
            "method": '',
            "methods": [],
            "unit_of_measure": 'cfu/g',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          },
          {
            "test_name": 'Total Plate Count',
            "statement": '',
            "magnification": '',
            "required_spec": True,
            "method": '',
            "methods": [],
            "unit_of_measure": 'cfu/g',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          },
          {
            "test_name": 'Coliforms Count',
            "statement": '',
            "magnification": '',
            "required_spec": True,
            "method": '',
            "methods": [],
            "unit_of_measure": 'cfu/g',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          },
          {
            "test_name": 'Escherichia Coli Count (E.Coli)',
            "statement": '',
            "magnification": '',
            "required_spec": True,
            "method": '',
            "methods": [],
            "unit_of_measure": 'cfu/g',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          },
          {
            "test_name": 'Staphylococcus Count (Staph)',
            "statement": '',
            "magnification": '',
            "required_spec": True,
            "method": '',
            "methods": [],
            "unit_of_measure": 'cfu/g',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          },
          {
            "test_name": 'Salmonella Count',
            "statement": '',
            "magnification": '',
            "required_spec": True,
            "method": '',
            "methods": [],
            "unit_of_measure": 'cfu/g',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          },
          {
            "test_name": 'Mold Count',
            "statement": '',
            "magnification": '',
            "required_spec": True,
            "method": '',
            "methods": [],
            "unit_of_measure": 'cfu/g',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          },
          {
            "test_name": 'Yeast Count',
            "statement": '',
            "magnification": '',
            "required_spec": True,
            "method": '',
            "methods": [],
            "unit_of_measure": 'cfu/g',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          },
          {
            "test_name": 'Moisture/Loss on Drying',
            "statement": '',
            "magnification": '',
            "required_spec": False,
            "method": '',
            "methods": [],
            "unit_of_measure": '%',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          }
        ]
      },
      "microscopic": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "locations": {
          "in_house": True,
          "primary": 'in_house',
          "supplier": False,
          "third_party_lab": False
        },
        "required_spec": True,
        "revision_number": 0,
        "id_code": '',
        "statement": 'Overall, the visual profile of this finished product under the microscope is a _______ powder. Typically, it has __________ with __________ . We expect this kind of visual profile for __________.',
        "test_name": 'Microscopic',
        "tests": []
      },
      "nutritional_facts": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "locations": {
          "in_house": False,
          "primary": 'third_party_lab',
          "supplier": True,
          "third_party_lab": True
        },
        "required_spec": False,
        "revision_number": 0,
        "id_code": '',
        "statement": '',
        "test_name": 'Nutritional Assay',
        "tests": []
      },
      "organochlorines": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "locations": {
          "in_house": False,
          "primary": 'supplier',
          "supplier": True,
          "third_party_lab": True
        },
        "required_spec": False,
        "revision_number": 0,
        "id_code": '',
        "statement": '',
        "test_name": 'Organochlorines',
        "tests": []
      },
      "organoleptic": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "locations": {
          "in_house": True,
          "primary": 'in_house',
          "supplier": True,
          "third_party_lab": False
        },
        "required_spec": True,
        "revision_number": 0,
        "id_code": '',
        "test_name": 'Organoleptic',
        "tests": [
          {
            "test_name": 'Organoleptic',
            "statement": 'Overall, the visual organoleptic profile of this finished product is a ________ powder. It typically has a _______ odor and a ________ taste. We expect this kind of organoleptic profile for _________.',
            "magnification": '',
            "required_spec": False,
            "method": '',
            "methods": [],
            "unit_of_measure": 'ppm',
            "count": 0,
            "inequality": '<',
            "sources": [],
            "odor": '',
            "taste_dissolved": '',
            "taste_dry": '',
            "visual": '',
            "id_code": '',
            "file_pointer": '',
            "file_preview_pointer": '',
            "date_issued": '',
            "date_revised": ''
          }
        ]
      },
      "pesticides": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "locations": {
          "in_house": False,
          "primary": 'supplier',
          "supplier": True,
          "third_party_lab": True
        },
        "required_spec": False,
        "revision_number": 0,
        "id_code": '',
        "statement": '[TEMPLATE]      However, to ensure this is the case, we test for pesticide residue on a skip lot basis (for each supplier company.) Ultimately, while pesticide specs are not required, if the supplier provides a C of A with pesticide testing, we\'ll accept the individual spec below.',
        "test_name": 'Pesticides',
        "tests": []
      },
      "residual_solvents": {
        "date_issued": '',
        "date_revised": '',
        "file_pointer": '',
        "locations": {
          "in_house": False,
          "primary": 'supplier',
          "supplier": True,
          "third_party_lab": True
        },
        "required_spec": False,
        "revision_number": 0,
        "id_code": '',
        "statement": 'Since this finished product is made from whole ingredients it\'s highly unlikely solvents were used at any point during production. Solvents are most often used in an extraction process that separates the natural constituents from a raw material (in an extract or concentrate.) This wouldn\'t be relevant for this product, which doesn\'t use extracts or concentrated powders; the typical way a powder is processed is through dehydration and grinding and therefore there should be no residual solvents.',
        "test_name": 'Residual Solvents',
        "tests": []
      }
    }
  }
}

def fix_product_master(custom_response):
    stm = update(db.Product_Master) \
            .values(
                doc=PRODUCT_DOC,
                date_entered=datetime.datetime.now(),
                spec_revise_date=datetime.datetime.now(),
                default_formula_version=None,
                num_formula_versions=0,
                default_manufacturing_version=None,
                num_manufacturing_versions=0
            ) \
            .where(db.Product_Master.product_id > 0)
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        print('FAILURE')
    return custom_response

def fix_old_components_template(custom_response):

    stm = select(db.Components).where(db.Components.component_type == "powder")
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    for row in raw_data:

        component = row[0].to_dict()
        doc = component['doc']
        # print(json.dumps(doc, indent=5))

        # Hi Nate, These are the things I need to be BULK changed
        # for Prolifix Manager specs:
        #
        # Purity statement: "This ingredient is verified
        # for purity via the supplier's Certificate of Analysis
        # and through microscopy observation (checking for contaminating
        # particles.) We verify this supplier through a reviewed
        # questionnaire and verify the supplier's certificate of
        # analysis on a random/skip lot basis."
        # NOTE: Effect Every Component with this change)
        doc['specifications']['purity_statement'] = "This ingredient is verified for purity via the supplier's Certificate of Analysis and through microscopy observation (checking for contaminating particles.) We verify this supplier through a reviewed questionnaire and verify the supplier's certificate of analysis on a random/skip lot basis."

        # Change heavy metals spec from required YES to required NO.
        # NOTE: Effect Every Component with this change)
        for hm in doc['specifications']['specs']['heavy_metals']['tests']:
            hm['required_spec'] = False

        # Pesticides:
        # Add statement (after first sentence)
        # "However, to ensure this is the case, we test for
        # pesticide residue on a skip lot basis (for each supplier company.)
        # While pesticide specs are not required, if the supplier
        # provides a C of A with pesticide testing, we'll accept
        # the individual spec below."
        # NOTE: Use input and print to check if a statement needs this appended or not.
        current_statement = doc['specifications']['specs']['pesticides']['statement']
        appending_statement = "However, to ensure this is the case, we test for pesticide residue on a skip lot basis (for each supplier company.) Ultimately, while pesticide specs are not required, if the supplier provides a C of A with pesticide testing, we'll accept the individual spec below."
        # check if appending statement already exists in current statement
        if appending_statement not in current_statement:
            doc['specifications']['specs']['pesticides']['statement'] = current_statement + "  " + appending_statement

        # Join aerobic and TPC together as one spec as well.
        # (and be able to select which one is relevant for a
        # particular ingredient--steve's suggestion.)
        # NOTE: Pick the max between TPC and Aerobic
        tpc = {}
        aerobic = {}
        coliforms = {}
        ecoli = {}
        staph = {}
        salmonella = {}
        mold = {}
        yeast = {}
        moisture = {}

        unknown_test = False
        tests = doc['specifications']['specs']['microbiological']['tests'].copy()
        for index, test in enumerate(tests):
            remove_test = False
            if 'Total Plate Count'.lower() in test['test_name'].lower():
                tpc = test.copy()
                tpc['test_name'] = 'Total Plate Count (Anaerobic)'
                remove_test = True
            elif 'Aerobic Plate Count'.lower() in test['test_name'].lower():
                aerobic = test.copy()
                if not aerobic['count']:
                    aerobic['required_spec'] = False
                remove_test = True
            elif 'Coliforms Count'.lower() in test['test_name'].lower():
                coliforms = test.copy()
                remove_test = True
            elif 'Escherichia Coli Count (E.Coli)'.lower() in test['test_name'].lower():
                ecoli = test.copy()
                remove_test = True
            elif 'Staphylococcus Count (Staph)'.lower() in test['test_name'].lower():
                staph = test.copy()
                remove_test = True
            elif 'Salmonella Count'.lower() in test['test_name'].lower():
                salmonella = test.copy()
                remove_test = True
            elif 'Mold Count'.lower() in test['test_name'].lower():
                mold = test.copy()
                remove_test = True
            elif 'Yeast Count'.lower() in test['test_name'].lower():
                yeast = test.copy()
                remove_test = True
            elif 'Moisture/Loss on Drying'.lower() in test['test_name'].lower():
                moisture = test.copy()
                remove_test = True
            else:
                print('Unknown test: ', test['test_name'])
                unknown_test = True
            if remove_test:
                doc['specifications']['specs']['microbiological']['tests'].remove(test)

        # Rearrange the microbiological specs so they follow the
        # same order as C of A's. (E.g.
        # Total plate count/aerobic plate count
        # Coliforms
        # E. Coli
        # Staphylococcus
        # Salmonella
        # Yeast
        # Mold
        # Moisture/Loss on Drying
        new_tests = []
        if tpc:
            new_tests.append(tpc)
        else:
            print("No TPC test found")
            print(component['component_id'])

        if coliforms:
            new_tests.append(coliforms)
        else:
            print("No Coliforms test found")

        if ecoli:
            new_tests.append(ecoli)
        else:
            print("No E.Coli test found")

        if staph:
            new_tests.append(staph)
        else:
            print("No Staph test found")

        if salmonella:
            new_tests.append(salmonella)
        else:
            print("No Salmonella test found")

        if mold:
            new_tests.append(mold)
        else:
            print("No Mold test found")

        if yeast:
            new_tests.append(yeast)
        else:
            print("No Yeast test found")

        if moisture:
            new_tests.append(moisture)
        else:
            print("No Moisture test found")

        # if aerobic:
        #     new_tests.append(aerobic)
        # else:
        #     print("No Aerobic test found")

        for remaining_test in doc['specifications']['specs']['microbiological']['tests']:
            new_tests.append(remaining_test)
        doc['specifications']['specs']['microbiological']['tests'] = new_tests

        # if unknown_test:
        #     print(json.dumps(new_tests, indent=3))

        # Change default template (it has no CofA,
        # and shouldn't have herbicides/insecticides...)

        test_catagories = doc['specifications']['specs'].keys()
        if 'herbicides' in test_catagories:
            del doc['specifications']['specs']['herbicides']
        if 'insecticides' in test_catagories:
            del doc['specifications']['specs']['insecticides']
        if 'organochlorines' in test_catagories:
            del doc['specifications']['specs']['organochlorines']
        if 'example_cofas' not in test_catagories:
            example_cofa = {
                    "date_issued": "",
                    "date_revised": "",
                    "file_pointer": "",
                    "id_code": "",
                    "locations": {
                        "in_house": True,
                        "primary": "in_house",
                        "supplier": True,
                        "third_party_lab": True
                    },
                    "required_spec": True,
                    "revision_number": 0,
                    "test_name": "Reference CofA's",
                    "tests": []
                }
            doc['specifications']['specs']['example_cofas'] = example_cofa
        myKeys = list(doc['specifications']['specs'].keys())
        myKeys.sort()
        sorted_dict = {i: doc['specifications']['specs'][i] for i in myKeys}
        doc['specifications']['specs'] = sorted_dict

        # Heavy Metals:
        # Add to the statement box,
        # "While heavy metal specs are not required, if the supplier
        # provides a test for heavy metals these are the specs we'll accept."
        doc['specifications']['specs']['heavy_metals']['statement'] = "While heavy metal specs are not required, if the supplier provides a test for heavy metals these are the specs we'll accept."

        # print(json.dumps(doc, indent=5))

        stm = update(db.Components).values(doc=doc).where(db.Components.component_id == component['component_id'])
        custom_response, raw_data, success = execute_query(custom_response, stm)

    return custom_response

def fix_org_doc(custom_response):
    org_doc = {
        "documents": [],
        "current_supplier_risk_assesment_id": None,
        "current_lab_risk_assessment_id": None,
        "current_client_risk_assessment_id": None,
        "current_courier_risk_assessment_id": None,
        "current_other_risk_assessment_id": None,
        "supplier_risk_assessments": [],
        "lab_risk_assessments": [],
        "client_risk_assessments": [],
        "courier_risk_assessments": [],
        "other_risk_assessments": []
    }

    stm = update(db.Organizations).values(doc=org_doc)

    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    return custom_response













