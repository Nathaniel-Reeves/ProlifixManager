import os
import csv
import json


file_path = "Orders/Orders db - Lot_Numbers.csv"

file = open(os.getcwd() + "/" + file_path, newline='')
data = list(csv.DictReader(file))
file.close()

labs = {
    "organoleptic": {
            "required_spec": "",
            "spec_issue_date": "",
            "spec_reviced_date": "",
            "standard_sample_lot": "",
            "file_pointer": "",
            "visual": "",
            "odor": "",
            "taste_dry": "",
            "taste_dissolved": "",
            "texture": "",
            "mesh": ""
    },
    "microbiological": {
        "required_spec": "",
        "spec_issue_date": "",
        "spec_reviced_date": "",
        "standard_sample_lot": "",
        "file_pointer": "",
        "tests": {
            "total_plate_count": {
                "required_spec": "",
                "method": "",
                "count": "",
                "units": "",
                "less_than": ""
            },
            "coliform_count": {
                "required_spec": "",
                "method": "",
                "count": "",
                "units": "",
                "less_than": ""
            },
            "escherichia_coli_count": {
                "required_spec": "",
                "method": "",
                "count": "",
                "units": "",
                "less_than": ""
            },
            "staphylococcus_count": {
                "required_spec": "",
                "method": "",
                "count": "",
                "units": "",
                "less_than": ""
            },
            "salmonella_count": {
                "required_spec": "",
                "method": "",
                "count": "",
                "units": "",
                "less_than": ""
            },
            "yeast_count": {
                "required_spec": "",
                "method": "",
                "count": "",
                "units": "",
                "less_than": ""
            },
            "mold_count": {
                "required_spec": "",
                "method": "",
                "count": "",
                "units": "",
                "less_than": ""
            },
            "moisture": {
                "required_spec": "",
                "method": "",
                "count": "",
                "units": "",
                "less_than": ""
            }
        }
    },
    "heavy_metals": {
        "required_spec": "",
        "spec_issue_date": "",
        "spec_reviced_date": "",
        "standard_sampleLot": "",
        "file_pointer": "",
        "tests": {
            "total_heavy_metals": {
                "required_spec": "",
                "method": "",
                "count": "",
                "units": "",
                "less_than": ""
            },
            "arsenic": {
                "required_spec": "",
                "method": "",
                "count": "",
                "units": "",
                "less_than": ""
            },
            "cadmium": {
                "required_spec": "",
                "method": "",
                "count": "",
                "units": "",
                "less_than": ""
            },
            "lead": {
                "required_spec": "",
                "method": "",
                "count": "",
                "units": "",
                "less_than": ""
            },
            "mercury": {
                "required_spec": "",
                "method": "",
                "count": "",
                "units": "",
                "less_than": ""
            }
        }
    },
    "ftir": {
        "required_spec": "",
        "spec_issue_date": "",
        "spec_reviced_date": "",
        "standard_sample_lot": "",
        "file_pointer": "",
        "percent_match_standard": "",
        "method": "",
        "rf_value": ""
    },
    "microscopic": {
        "required_spec": "",
        "spec_issue_date": "",
        "spec_reviced_date": "",
        "standard_sample_lot": "",
        "file_pointer": "",
        "image_file_pointer": "",
        "description": "",
        "magnification": "",
        "microscope_type": ""
    },
    "chromatography": {
        "required_spec": "",
        "spec_issue_date": "",
        "spec_reviced_date": "",
        "standard_sample_lot": "",
        "file_pointer": "",
        "method": "",
        "description": ""
    },
    "nutritionalFacts": {
        "required_spec": "",
        "spec_issue_date": "",
        "spec_reviced_date": "",
        "standard_sample_lot": "",
        "file_pointer": "",
        "serving_size": "",
        "serving_units": "",
        "tests": {
            "calories": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "total_fats": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "saturated_fats": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "trans_fats": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "cholesterol": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "total_carbohydrate": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "dietary_fiber": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "total_sugars": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "added_sugars": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "protein": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "sodium": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "potassium": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "calcium": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "zinc": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "iron": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "copper": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "magnesium": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "selenium": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "manganese": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "biotin": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "vitamin_a": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "vitamin_b1": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "vitamin_b2": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "vitamin_b3": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "vitamin_b5": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "vitamin_b6": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "vitamin_b12": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "vitamin_c": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "vitamin_d3": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "vitamin_e": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            },
            "vitamin_k2": {
                "ammount_per_serving": "",
                "units": "",
                "source": ""
            }
        }
    },
    "pesticides": {
        "required_spec": "",
        "spec_issue_date": "",
        "spec_reviced_date": "",
        "standard_sample_lot": "",
        "file_pointer": ""
    },
    "foreign_matter": {
        "required_spec": "",
        "spec_issue_date": "",
        "spec_reviced_date": "",
        "standard_sample_lot": "",
        "file_pointer": ""
    }
}

headers = str(list(data[0].keys())).replace("'","").replace(", ","|")[1:-1]

for row in data:
    doc = json.loads(row["doc"])
    doc.pop("lab_results")
    doc["lab_results"] = labs
    str_doc = json.dumps(doc).replace(",", "&")
    row["doc"] = "`"+str_doc+"`"


output_csv_file = "out.csv"
with open(output_csv_file, "w") as f:
    f.write(headers + "\n")
    for i in range(len(data)):
        row = str(list(data[i].values())).replace("'", "").replace(", ","|").replace("&",",").replace("`","")[1:-1]
        f.write(row + "\n")

