-- Build all tables and databases.

CREATE DATABASE IF NOT EXISTS `Organizations`;
CREATE DATABASE IF NOT EXISTS `Inventory`;
CREATE DATABASE IF NOT EXISTS `Products`;
CREATE DATABASE IF NOT EXISTS `Manufacturing`;
CREATE DATABASE IF NOT EXISTS `Orders`;
CREATE DATABASE IF NOT EXISTS `Formulas`;

CREATE TABLE IF NOT EXISTS `Organizations`.`Users` (
  `user_id` INT,
  `person_id` INT,
  `username` VARCHAR(100) UNIQUE NOT NULL,
  `encrypted_password` VARCHAR(250) NOT NULL,
  `profile_picture` VARCHAR(500),
  `color_theme` ENUM('Light','Dark'),
  `_json_schema` json GENERATED ALWAYS AS (_utf8mb4'{"type":"object"}') VIRTUAL,
  `doc` json DEFAULT (CONCAT('{"_id":',`user_id`,',"access_privileges":{"human_resources":"staff", "client_relations":"staff", "supplier_relations":"staff", "production":"staff", "logistics":"staff"}}')),
  PRIMARY KEY (`user_id`),
  CONSTRAINT `Org_User_t1_chk_1` CHECK (json_schema_valid(`_json_schema`,`doc`)) /*!80016 NOT ENFORCED */
);

CREATE TABLE IF NOT EXISTS `Organizations`.`Organizations` (
  `organization_id` INT,
  `date_entered` DATE NULL DEFAULT NULL,
  `website_url` VARCHAR(200),
  `vetted` BOOL,
  `date_vetted` DATE NULL DEFAULT NULL,
  `risk_level` ENUM("UNKNOWN", "No Risk", "Low Risk", "Medium Risk", "High Risk"),
  `supplier` BOOL DEFAULT false,
  `client` BOOL DEFAULT false,
  `lab` BOOL DEFAULT false,
  `other` BOOL DEFAULT false,
  `_json_schema` json GENERATED ALWAYS AS (_utf8mb4'{"type":"object"}') VIRTUAL,
  `doc` json DEFAULT (CONCAT('{"_id":"',`organization_id`,'","files":[]}')),
  `notes` VARCHAR(2500),
  PRIMARY KEY (`organization_id`),
  CONSTRAINT `Org_Org_t1_chk_1` CHECK (json_schema_valid(`_json_schema`,`doc`)) /*!80016 NOT ENFORCED */
);

CREATE TABLE `Organizations`.`Organization_Names` (
  `name_id` INT,
  `organization_id` INT,
  `organization_name` VARCHAR(200) NOT NULL,
  `organization_initial` VARCHAR(10) NOT NULL,
  `primary_name` BOOL,
  PRIMARY KEY (`name_id`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`),
  INDEX ( `organization_name` ),
  INDEX ( `organization_initial` )
);

CREATE TABLE IF NOT EXISTS `Organizations`.`Facilities` (
  `facility_id` INT AUTO_INCREMENT,
  `organization_id` INT,
  `building_name` VARCHAR(500),
  `building_type` ENUM('Head Office', 'Office', 'Distribution Warehouse', 'Manufacturing Facility', 'Storefront'),
  `street_1_number` INT,
  `street_1_number_suffix` VARCHAR(10),
  `street_1_name` VARCHAR(500),
  `street_1_type` VARCHAR(300),
  `street_1_direction` VARCHAR(2),
  `street_2_number` INT,
  `street_2_number_suffix` VARCHAR(10),
  `street_2_name` VARCHAR(500),
  `street_2_type` VARCHAR(300),
  `street_2_direction` VARCHAR(2),
  `address_type` VARCHAR(300),
  `address_type_identifier` VARCHAR(100),
  `local_municipality` VARCHAR(500),
  `city_town` VARCHAR(500),
  `governing_district` VARCHAR(500),
  `postal_area` VARCHAR(100),
  `country` VARCHAR(500),
  `ship_time` INT,
  `ship_time_units` ENUM( "Unknown", "Day/s", "Week/s", "Month/s"),
  `ship_time_in_days` INT,
  `notes` VARCHAR(2500),
  PRIMARY KEY (`facility_id`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Products`.`Product_Master` (
  `product_id` INT,
  `organization_id` INT,
  `product_name` VARCHAR(300) NOT NULL,
  `type` ENUM('Powder','Capsule', 'Liquid','Other'),
  `current_product` BOOL,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `spec_issue_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `spec_revise_date` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `exp_time_frame` SMALLINT,
  `exp_unit` ENUM('Year/s','Month/s','Day/s'),
  `exp_type` ENUM('Best By', 'Exp'),
  `exp_use_oldest_ingredient` BOOL,
  `default_formula_id` INT DEFAULT NULL,
  `_json_schema` json GENERATED ALWAYS AS (_utf8mb4'{"type":"object"}') VIRTUAL,
  `doc` json DEFAULT (CONCAT('{
    "_id":',`product_id`,',
    "lab_specs": {
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
            "test_name": "microbiological",
            "required_spec": "",
            "spec_issue_date": "",
            "spec_reviced_date": "",
            "standard_sample_lot": "",
            "file_pointer": "",
            "tests": {
                "total_plate_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "coliform_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "escherichia_coli_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "staphylococcus_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "salmonella_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "yeast_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "mold_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "moisture": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
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
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "arsenic": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "cadmium": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "lead": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "mercury": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
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
}')),
  PRIMARY KEY (`product_id`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`),
  CONSTRAINT `Products_Master_t1_chk_1` CHECK (json_schema_valid(`_json_schema`,`doc`)) /*!80016 NOT ENFORCED */
);

CREATE TABLE IF NOT EXISTS `Inventory`.`Components` (
  `component_id` INT,
  `component_type` Enum('Powder', 'Liquid', 'Jar/Container', 'Bag', 'Shrink Band', 'Lid/Cap', 'Label', 'Capsule', 'MISC', 'Scoop', 'Desiccant', 'Box/Carton', 'Packaging Material'),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `owner_id` INT,
  `_json_schema` json GENERATED ALWAYS AS (_utf8mb4'{"type":"object"}') VIRTUAL,
  `doc` json DEFAULT (CONCAT('{
    "_id":',`component_id`,',
    "lab_specs": {
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
            "test_name": "microbiological",
            "required_spec": "",
            "spec_issue_date": "",
            "spec_reviced_date": "",
            "standard_sample_lot": "",
            "file_pointer": "",
            "tests": {
                "total_plate_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "coliform_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "escherichia_coli_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "staphylococcus_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "salmonella_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "yeast_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "mold_count": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "moisture": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
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
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "arsenic": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "cadmium": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "lead": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
                },
                "mercury": {
                    "required_spec": 0,
                    "method": "",
                    "summary": "",
                    "count": "",
                    "units": "",
                    "less_than": 0
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
}')),
  PRIMARY KEY (`component_id`),
  FOREIGN KEY (`owner_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`),
  CONSTRAINT `Inv_components_t1_chk_1` CHECK (json_schema_valid(`_json_schema`,`doc`)) /*!80016 NOT ENFORCED */
);

CREATE TABLE IF NOT EXISTS `Inventory`.`Component_Names` (
  `name_id` INT,
  `component_id` INT,
  `component_name` VARCHAR(300) NOT NULL,
  `primary_name` BOOL,
  PRIMARY KEY (`name_id`),
  FOREIGN KEY (`component_id`) REFERENCES `Inventory`.`Components`(`component_id`),
  INDEX ( `component_name` )
);

CREATE TABLE IF NOT EXISTS `Inventory`.`Inventory` (
  `inv_id` INT AUTO_INCREMENT,
  `item_id` INT,
  `actual_inventory` DECIMAL(16,4),
  `theoretical_inventory` DECIMAL(16,4),
  `recent_cycle_count_id` INT,
  `organic` ENUM('organic', 'non-organic', 'n/a'),
  `brand_id` INT,
  PRIMARY KEY (`inv_id`),
  FOREIGN KEY (`item_id`) REFERENCES `Products`.`Product_Master`(`product_id`),
  FOREIGN KEY (`item_id`) REFERENCES `Inventory`.`Components`(`component_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Orders`.`Purchase_Orders` (
  `prefix` VARCHAR(10),
  `year` TINYINT,
  `month` TINYINT,
  `sec_number` SMALLINT,
  `organization_id` INT,
  `supplier_so_num` VARCHAR(30),
  `order_date` DATE,
  `eta_date` DATE,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`prefix`, `year`, `month`, `sec_number`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Orders`.`Purchase_Order_Detail` (
  `po_detail_id` INT AUTO_INCREMENT,
  `prefix` VARCHAR(10),
  `year` TINYINT,
  `month` TINYINT,
  `sec_number` SMALLINT,
  `component_id` INT,
  `unit_order_qty` INT,
  `kilos_order_qty` DECIMAL(16,4),
  `special_instructions` VARCHAR(2000),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `bid_price_per_unit` DECIMAL(16,4),
  `bid_price_per_kilo` DECIMAL(16,4),
  PRIMARY KEY (`po_detail_id`),
  FOREIGN KEY (`prefix`, `year`, `month`, `sec_number`) REFERENCES `Orders`.`Purchase_Orders`(`prefix`, `year`, `month`, `sec_number`),
  FOREIGN KEY (`component_id`) REFERENCES `Inventory`.`Components`(`component_id`)
);

CREATE TABLE IF NOT EXISTS `Inventory`.`Cycle_Counts_Log` (
  `cycle_count_id` INT AUTO_INCREMENT,
  `inv_id` INT,
  `actual_inventory_precheck` DECIMAL(16,4),
  `cycle_count_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `amount_counted` DECIMAL(16,4),
  `cycle_count_grade` BOOL NOT NULL,
  `user_id` INT,
  `fixed_actual_inventory` DECIMAL(16,4) NOT NULL,
  `notes` VARCHAR(2000),
  PRIMARY KEY (`cycle_count_id`),
  FOREIGN KEY (`inv_id`) REFERENCES `Inventory`.`Inventory`(`inv_id`),
  FOREIGN KEY (`user_id`) REFERENCES `Organizations`.`Users`(`user_id`)
);

CREATE TABLE IF NOT EXISTS `Inventory`.`Check-in_Log` (
  `check_in_id` INT AUTO_INCREMENT,
  `inv_id` INT,
  `amount` DECIMAL(16,4),
  `status` JSON,
  `user_id` INT,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `po_detail_id` INT DEFAULT NULL,
  PRIMARY KEY (`check_in_id`),
  FOREIGN KEY (`inv_id`) REFERENCES `Inventory`.`Inventory`(`inv_id`),
  FOREIGN KEY (`user_id`) REFERENCES `Organizations`.`Users`(`user_id`),
  FOREIGN KEY (`po_detail_id`) REFERENCES `Orders`.`Purchase_Order_Detail`(`po_detail_id`)
);

CREATE TABLE IF NOT EXISTS `Products`.`Manufacturing_Process` (
  `process_spec_id` INT AUTO_INCREMENT,
  `product_id` INT,
  `processes_collection` JSON,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `current_default_process` BOOL,
  PRIMARY KEY (`process_spec_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`)
);

CREATE TABLE IF NOT EXISTS `Manufacturing`.`Processes` (
  `process_id` INT,
  `process_name` VARCHAR(100) NOT NULL,
  `process_sop_id` VARCHAR(30),
  `_json_schema` json GENERATED ALWAYS AS (_utf8mb4'{"type":"object"}') VIRTUAL,
  `doc` json DEFAULT (CONCAT('{"_id":',`process_id`,'}')),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`process_id`),
  CONSTRAINT `man_process_t1_chk_1` CHECK (json_schema_valid(`_json_schema`,`doc`)) /*!80016 NOT ENFORCED */
);

CREATE TABLE IF NOT EXISTS `Organizations`.`People` (
  `person_id` INT AUTO_INCREMENT,
  `organization_id` INT,
  `first_name` VARCHAR(100),
  `last_name` VARCHAR(100),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `job_description` VARCHAR(100),
  `department` VARCHAR(500),
  `phone_number_primary` VARCHAR(20),
  `phone_number_secondary` VARCHAR(20),
  `email_address_primary` VARCHAR(100),
  `email_address_secondary` VARCHAR(100),
  `birthday` DATE,
  `is_employee` BOOL,
  `contract_date` DATE,
  `termination_date` DATE,
  `clock_number` VARCHAR(20),
  PRIMARY KEY (`person_id`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Orders`.`Sales_Orders` (
  `prefix` VARCHAR(10),
  `year` TINYINT,
  `month` TINYINT,
  `sec_number` SMALLINT,
  `organization_id` INT,
  `client_po_num` VARCHAR(30),
  `order_date` DATE,
  `target_completion_date` DATE,
  `completion_date` DATE,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`prefix`, `year`, `month`, `sec_number`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Orders`.`Sale_Order_Detail` (
  `so_detail_id` INT AUTO_INCREMENT,
  `prefix` VARCHAR(10),
  `year` TINYINT,
  `month` TINYINT,
  `sec_number` SMALLINT,
  `product_id` INT,
  `unit_order_qty` INT,
  `kilos_order_qty` DECIMAL(16,4),
  `special_instructions` VARCHAR(2000),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `bid_price_per_unit` DECIMAL(16,4),
  `completed_and_billed` BOOL,
  `final_ship_date` DATE,
  PRIMARY KEY (`so_detail_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`),
  FOREIGN KEY (`prefix`, `year`, `month`, `sec_number`) REFERENCES `Orders`.`Sales_Orders`(`prefix`, `year`, `month`, `sec_number`)
);

CREATE TABLE IF NOT EXISTS `Orders`.`Lot_Numbers` (
  `prefix` VARCHAR(15),
  `year` TINYINT,
  `month` TINYINT,
  `sec_number` SMALLINT,
  `suffix` VARCHAR(15),
  `product_id` INT,
  `prolifix_lot_number` VARCHAR(20) DEFAULT (CONCAT(`prefix`, LPAD(`year`,2,"0"), LPAD(`month`,2,"0"), LPAD(`sec_number`,3,"0"), `suffix`)),
  `so_detail_id` INT,
  `target_unit_yield` INT,
  `actual_unit_yield` INT,
  `retentions` INT,
  `total_shippable_product` INT,
  `_json_schema` json GENERATED ALWAYS AS (_utf8mb4'{"type":"object"}') VIRTUAL,
  `doc` json DEFAULT (CONCAT('{"_id":"',`prolifix_lot_number`,'"}')),
  `batch_printed` BOOL,
  `bpr_printed` BOOL,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `exp_date` DATE,
  `exp_type` ENUM('Best By', 'Exp'),
  PRIMARY KEY (`prefix`, `year`, `month`, `sec_number`, `suffix`),
  FOREIGN KEY (`so_detail_id`) REFERENCES `Orders`.`Sale_Order_Detail`(`so_detail_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`),
  CONSTRAINT `Org_Org_t1_chk_1` CHECK (json_schema_valid(`_json_schema`,`doc`)) /*!80016 NOT ENFORCED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `Products`.`Components` (
  `component_id` INT AUTO_INCREMENT,
  `materials_id` INT,
  `product_id` INT,
  `material_qty_per_unit` INT NOT NULL,
  `current_default_component` BOOL NOT NULL,
  `component_list_version` SMALLINT NOT NULL,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`component_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`),
  FOREIGN KEY (`materials_id`) REFERENCES `Inventory`.`Components`(`component_id`)
);

CREATE TABLE IF NOT EXISTS `Formulas`.`Formula_Master` (
  `formula_id` INT AUTO_INCREMENT,
  `product_id` INT,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `formulation_version` SMALLINT,
  `notes` VARCHAR(1000),
  `capsule_size` VARCHAR(100),
  `empty_capsule_mg` DOUBLE,
  `total_grams_per_unit` DOUBLE,
  `total_capsules_per_unit` DOUBLE,
  `total_milliliters_per_unit` DOUBLE,
  `fill_min` DOUBLE,
  `fill_max` DOUBLE,
  `label_id` INT,
  PRIMARY KEY (`formula_id`),
  FOREIGN KEY (`label_id`) REFERENCES `Inventory`.`Components`(`component_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`)
);

CREATE TABLE IF NOT EXISTS `Formulas`.`Formula_Detail` (
  `formula_ingredient_id` INT AUTO_INCREMENT,
  `formula_id` INT,
  `percent` DOUBLE,
  `mg_per_capsule` DOUBLE,
  `ml_per_unit` DOUBLE,
  `grams_per_unit` DOUBLE,
  `organic_spec` ENUM('organic', 'non-organic', 'any'),
  `ingredient_id` INT,
  `notes` VARCHAR(1000),
  `brand_specific` BOOL,
  `organic_specific` BOOL,
  PRIMARY KEY (`formula_ingredient_id`),
  FOREIGN KEY (`ingredient_id`) REFERENCES `Inventory`.`Components`(`component_id`),
  FOREIGN KEY (`formula_id`) REFERENCES `Formulas`.`Formula_Master`(`formula_id`)
);

CREATE TABLE IF NOT EXISTS `Manufacturing`.`Equipment` (
  `equipment_id` INT AUTO_INCREMENT,
  `process_id` INT,
  `equipment_sn` VARCHAR(50),
  `status` ENUM('Working Order', 'Broken', 'Removed'),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `equipment_history` JSON,
  PRIMARY KEY (`equipment_id`),
  FOREIGN KEY (`process_id`) REFERENCES `Manufacturing`.`Processes`(`process_id`)
);

CREATE TABLE IF NOT EXISTS `Formulas`.`Quaternary_Group` (
  `id` INT AUTO_INCREMENT,
  `formula_id` INT,
  `brand_id` INT,
  `organic_spec` ENUM('organic', 'non-organic', 'any'),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`formula_id`) REFERENCES `Formulas`.`Formula_Detail`(`formula_ingredient_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Formulas`.`Tertiary_Group` (
  `id` INT AUTO_INCREMENT,
  `formula_ingredient_id` INT,
  `brand_id` INT,
  `organic_spec` ENUM('organic', 'non-organic', 'any'),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`formula_ingredient_id`) REFERENCES `Formulas`.`Formula_Detail`(`formula_ingredient_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Formulas`.`Secondary_Group` (
  `id` INT AUTO_INCREMENT,
  `formula_ingredient_id` INT,
  `brand_id` INT,
  `organic_spec` ENUM('organic', 'non-organic', 'any'),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`formula_ingredient_id`) REFERENCES `Formulas`.`Formula_Detail`(`formula_ingredient_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Formulas`.`Primary_Group` (
  `id` INT AUTO_INCREMENT,
  `formula_ingredient_id` INT,
  `brand_id` INT,
  `organic_spec` ENUM('organic', 'non-organic', 'any'),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`formula_ingredient_id`) REFERENCES `Formulas`.`Formula_Detail`(`formula_ingredient_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);