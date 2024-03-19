import os
import json
import datetime
import traceback
import sys

def get_filenames(directory):
    filenames = os.listdir(directory)
    return filenames

def read_json_file(directory, filename):
    path = os.path.join(directory, filename)
    data = json.load(open(path, 'rb'))
    return data

def format_title_string(string):
    # Define words to exclude from capitalization
    excluded_words = ["and", "or", "the", "of", "a", "an", "in", "on", "at", "for", "with"]
    words = string.split(" ")
    formatted_words = []
    for word in words:
        if word.lower() not in excluded_words:
            formatted_words.append(word.capitalize())
        else:
            formatted_words.append(word)
    return " ".join(formatted_words)

def format_key_string(string):
    words = string.split(" ")
    formatted_words = []
    for word in words:
        formatted_words.append(word.lower())
    return "_".join(formatted_words)

def translate_component_names(template, data):
    template_component_name = {
        "component_name": "",
        "primary_name": False,
        "botanical_name": False
    }
    
    primary = template_component_name.copy()
    primary["primary_name"] = True
    primary["component_name"] = format_title_string(data["component_primary_name"])
    if data["component_primary_name"] == data["botanical_name"]:
        primary["botanical_name"] = True
    else:
        if data["botanical_name"] and (data["botanical_name"] != "N/a" or data["botanical_name"] != "N/A"):
            botanical = template_component_name.copy()
            botanical["component_name"] = format_title_string(data["botanical_name"])
            botanical["botanical_name"] = True
            template["Component_Names"].append(botanical)
    template["Component_Names"].append(primary)
    for name in data["other_names"]:
        if name == "name":
            continue
        if name == "N/a" or name == "N/A":
            continue
        name_temp = template_component_name.copy()
        name_temp["component_name"] = format_title_string(name)
        template["Component_Names"].append(name_temp)
    return template

def verify_datetime(str, error_date):
    try:
        return datetime.datetime.fromisoformat(str.replace('Z', '+00:00')).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        # traceback.print_exc(file=sys.stdout)
        return datetime.datetime.fromisoformat(error_date.replace('Z', '+00:00')).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

def translate_data(template, data):
    
    # Root Component Data
    template["component_type"] = "powder"
    template["units"] = "kilograms"
    template["brand_id"] = None
    for cert, val in data["certifications"].items():
        template["certified_" + cert] = val
    
    # Component Names
    template = translate_component_names(template, data)
    
    # Specification Header Data
    template["doc"]["specifications"]["date_issued"] = verify_datetime(data["specifications"]["date_issued"], datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
    template["doc"]["specifications"]["date_revised"] = verify_datetime(data["specifications"]["date_revised"], datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
    template["doc"]["specifications"]["revision_number"] = data["specifications"]["revision_number"]
    template["doc"]["specifications"]["description_statement"] = data["specifications"]["description_statement"]
    template["doc"]["specifications"]["identity_statement"] = data["specifications"]["identity_statement"]
    template["doc"]["specifications"]["purity_statement"] = data["specifications"]["purity_statement"]
    template["doc"]["specifications"]["strength_statement"] = data["specifications"]["strength_statement"]
    template["doc"]["specifications"]["origin"] = data["specifications"]["origin"]
    template["doc"]["specifications"]["parts_used"] = data["specifications"]["parts_used"]
    
    # Individual Specs
    specs = template["doc"]["specifications"]["specs"].keys()
    for spec_key in specs:
        old_spec_key = spec_key
        if spec_key == 'mesh_size':
            old_spec_key = 'foreign_matter'
        if spec_key in ["ftir", "hplc", "organochlorines", "insecticides", "herbicides", "microscopic", "example_cofas"]:
            continue
        
        # Translate Individual Specs
        try:
            template["doc"]["specifications"]["specs"][spec_key]["date_issued"] = verify_datetime(data["specifications"][old_spec_key]["date_issued"], template["doc"]["specifications"]["date_issued"])
            template["doc"]["specifications"]["specs"][spec_key]["date_revised"] = verify_datetime(data["specifications"][old_spec_key]["date_revised"], template["doc"]["specifications"]["date_issued"])
            template["doc"]["specifications"]["specs"][spec_key]["file_pointer"] = data["specifications"][old_spec_key]["file_pointer"]
            template["doc"]["specifications"]["specs"][spec_key]["id_code"] = data["specifications"][old_spec_key]["standard_sample_lot"]
            template["doc"]["specifications"]["specs"][spec_key]["locations"] = data["specifications"][old_spec_key]["locations"]
            template["doc"]["specifications"]["specs"][spec_key]["required_spec"] = data["specifications"][old_spec_key]["required_spec"]
            template["doc"]["specifications"]["specs"][spec_key]["revision_number"] = data["specifications"][old_spec_key]["revision_number"]
            if spec_key != 'organoleptic':
                template["doc"]["specifications"]["specs"][spec_key]["statement"] = data["specifications"][old_spec_key]["statement"]
            
            # Translate Individual Tests
            if spec_key in ["pesticides", "residual_solvents"]:
                continue
            tests = data["specifications"][old_spec_key]["tests"].keys()
            if "required_spec" not in tests and tests:
                for test in tests:
                    if test in ["anaerobic_plate_count", "sterio_microscope", "screen"]:
                        continue
                    if spec_key == "organoleptic":
                        template["doc"]["specifications"]["specs"][spec_key]["tests"][0]["visual"] = data["specifications"]["organoleptic"]["tests"]["taste_dry"]
                        template["doc"]["specifications"]["specs"][spec_key]["tests"][0]["odor"] = data["specifications"]["organoleptic"]["tests"]["taste_dry"]
                        template["doc"]["specifications"]["specs"][spec_key]["tests"][0]["taste_dry"] = data["specifications"]["organoleptic"]["tests"]["taste_dry"]
                        template["doc"]["specifications"]["specs"][spec_key]["tests"][0]["taste_dissolved"] = data["specifications"]["organoleptic"]["tests"]["taste_dissolved"]
                        template["doc"]["specifications"]["specs"][spec_key]["tests"][0]["date_issued"] = verify_datetime(data["specifications"][old_spec_key]["date_issued"], template["doc"]["specifications"]["date_issued"])
                        template["doc"]["specifications"]["specs"][spec_key]["tests"][0]["date_revised"] = verify_datetime(data["specifications"][old_spec_key]["date_revised"], template["doc"]["specifications"]["date_issued"])
                        continue
                    if spec_key == "nutritional_facts":
                        if (data["specifications"]["nutritional_facts"]["tests"][test]["unit_of_measure"] or data["specifications"]["nutritional_facts"]["tests"][test]["ammount_per_serving"]):
                            new_spec_test = new_test()
                            new_spec_test["test_name"] = format_title_string(test)
                            new_spec_test["count"] = data["specifications"][old_spec_key]["tests"][test]["ammount_per_serving"]
                            new_spec_test["unit_of_measure"] = data["specifications"][old_spec_key]["tests"][test]["unit_of_measure"]
                            for source in data["specifications"][old_spec_key]["tests"][test]["sources"]:
                                if source:
                                    new_spec_test["sources"].append(source)
                            for method in data["specifications"][old_spec_key]["tests"][test]["methods"]:
                                if method:
                                    new_spec_test["methods"].append(method)
                            new_spec_test["required_spec"] = data["specifications"][old_spec_key]["tests"][test]["required_spec"]
                            template["doc"]["specifications"]["specs"][spec_key]["tests"].append(new_spec_test)
                            continue
                        else:
                            continue
                    new_spec_test, new_spec_test_index = find_test(test, template["doc"]["specifications"]["specs"][spec_key]["tests"])
                    if spec_key == "gluten":
                        if (data["specifications"][old_spec_key]["tests"][test]["statement"] or data["specifications"][old_spec_key]["tests"][test]["count"]):
                            new_spec_test = new_test()
                            new_spec_test["test_name"] = "Gluten"
                            new_spec_test_index = 0
                        else:
                            continue
                    new_spec_test["required_spec"] = data["specifications"][old_spec_key]["tests"][test]["required_spec"]
                    if test == 'moisture':
                        new_spec_test["required_spec"] = False
                    new_spec_test["statement"] = data["specifications"][old_spec_key]["tests"][test]["statement"]
                    new_spec_test["count"] = data["specifications"][old_spec_key]["tests"][test]["count"]
                    sign = "="
                    less_than = data["specifications"][old_spec_key]["tests"][test]["less_than"]
                    greater_than = data["specifications"][old_spec_key]["tests"][test]["greater_than"]
                    if less_than:
                        sign = "<"
                    if greater_than:
                        sign = ">"
                    new_spec_test["inequality"] = sign
                    new_spec_test["unit_of_measure"] = data["specifications"][old_spec_key]["tests"][test]["unit_of_measure"]
                    for method in data["specifications"][old_spec_key]["tests"][test]["methods"]:
                        if method:
                            new_spec_test["methods"].append(method)
                    if template["doc"]["specifications"]["specs"][spec_key]["tests"]:
                        template["doc"]["specifications"]["specs"][spec_key]["tests"][new_spec_test_index] = new_spec_test
                    else:
                        template["doc"]["specifications"]["specs"][spec_key]["tests"].append(new_spec_test)
                
            
        except:
            traceback.print_exc(file=sys.stdout)
            print("Key: ", old_spec_key)
            print()
    
    return template

def new_test():
    return {
            "test_name": "",
            "statement": "",
            "magnification": "",
            "required_spec": False,
            "method": "",
            "methods": [],
            "unit_of_measure": "",
            "count": 0,
            "inequality": "=",
            "sources": [],
            "odor": "",
            "taste_dissolved": "",
            "taste_dry": "",
            "visual": "",
            "id_code": "",
            "file_pointer": "",
            "file_preview_pointer": "",
            "date_issued": "",
            "date_revised": ""
        }

def find_test(old_test_key, new_tests):
    if not new_tests:
        return {}, 0
    ret = {}
    index = 0
    for i, new_test in enumerate(new_tests):
        new_test_name = new_test["test_name"]
        if old_test_key == "escherichia_coli_count" and new_test_name == "Escherichia Coli Count (E.Coli)":
            ret = new_test
            index = i
            break
        if old_test_key == "moisture" and new_test_name == "Moisture/Loss on Drying":
            ret = new_test
            index = i
            break
        if old_test_key == "staphylococcus_count" and new_test_name == "Staphylococcus Count (Staph)":
            ret = new_test
            index = i
            break
        if old_test_key == "coliform_count" and new_test_name == "Coliforms Count":
            ret = new_test
            index = i
            break
        if old_test_key == "arsenic" and new_test_name == "Arsenic (As)":
            ret = new_test
            index = i
            break
        if old_test_key == "cadmium" and new_test_name == "Cadmium (Cd)":
            ret = new_test
            index = i
            break
        if old_test_key == "lead" and new_test_name == "Lead (Pb)":
            ret = new_test
            index = i
            break
        if old_test_key == "mercury" and new_test_name == "Mercury (Hg)":
            ret = new_test
            index = i
            break
        if old_test_key == "screen" and new_test_name == "Mesh Size":
            ret = new_test
            index = i
            break
        if old_test_key == format_key_string(new_test["test_name"]):
            ret = new_test
            index = i
            break
    if not ret:
        print("Could not find key: ", old_test_key)
    return ret, index
    
def save_json_file(data, directory, filename):
    path = os.path.join(directory, filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=3)
    return

def main():
    # directory = "./data"
    directory = "/home/natha/specs"
    filenames = get_filenames(directory)
    
    # for filename in filenames:
    #     data = read_json_file(directory, filename)
    #     out = translate_data(template.copy(), data)
    #     # save_json_file(out, "./out", filename)
    
    # component_columns = "component_id, brand_id, component_type, units, date_entered, certified_usda_organic, certified_halal, certified_kosher, certified_gluten_free, certified_national_sanitation_foundation, certified_us_pharmacopeia, certified_non_gmo, certified_vegan, doc\n"
    # path = './out/components_out.csv'
    # with open(path, "a") as f:
    #     f.write(component_columns)
    
    # path = './out/component_names_out.csv'
    # component_names_columns = "name_id, component_id, component_name, primary_name, botanical_name\n"
    # with open(path, "a") as f:
    #     f.write(component_names_columns)
    
    # path = './out/item_id_out.csv'
    # item_id_columns = "item_id, product_id, component_id\n"
    # with open(path, "a") as f:
    #     f.write(item_id_columns)
        
    component_id = 200
    component_name_id = 200
    item_id = 34
    for filename in filenames:
        template = read_json_file("./", "template.json")
        data = read_json_file(directory, filename)
        out = translate_data(template, data)
        print(filename)

        line = ""
        line += str(component_id) + "|"
        line += "1|"
        line += out["component_type"] + "|"
        line += out["units"] + "|"
        line += datetime.datetime.now().strftime('%Y-%m-%d') + "|"
        line += ("1" if out["certified_usda_organic"] else "0") + "|"
        line += ("1" if out["certified_halal"] else "0") + "|"
        line += ("1" if out["certified_kosher"] else "0") + "|"
        line += ("1" if out["certified_gluten_free"] else "0") + "|"
        line += ("1" if out["certified_national_sanitation_foundation"] else "0") + "|"
        line += ("1" if out["certified_us_pharmacopeia"] else "0") + "|"
        line += ("1" if out["certified_non_gmo"] else "0") + "|"
        line += ("1" if out["certified_vegan"] else "0") + "|"
        line += str(json.dumps(out["doc"])).replace('"','""')
        line += "\n"
        
        path = '/tmp/out/components_out.csv'
        with open(path, "a") as f:
            f.write(line)
        
        for name in out["Component_Names"]:
            line = ""
            line += str(component_name_id) + "|"
            line += str(component_id) + "|"
            line += name["component_name"] + "|"
            line += ("1" if name["primary_name"] else "0") + "|"
            line += ("1" if name["botanical_name"] else "0") + "|"
            line += "\n"
            
            path = '/tmp/out/component_names_out.csv'
            with open(path, "a") as f:
                f.write(line)
            component_name_id += 1
            
        line = ""
        line += str(item_id) + "|"
        line += "NULL" + "|"
        line += str(component_id) + "|"
        line += "\n"
        
        path = '/tmp/out/item_id_out.csv'
        with open(path, "a") as f:
            f.write(line)

        component_id += 1
        item_id += 1


if __name__ == '__main__':
    main()