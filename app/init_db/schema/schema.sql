-- Build all tables and databases.

CREATE DATABASE IF NOT EXISTS `Organizations`;
CREATE DATABASE IF NOT EXISTS `Inventory`;
CREATE DATABASE IF NOT EXISTS `Products`;
CREATE DATABASE IF NOT EXISTS `Manufacturing`;
CREATE DATABASE IF NOT EXISTS `Orders`;
CREATE DATABASE IF NOT EXISTS `Formulas`;
CREATE DATABASE IF NOT EXISTS `Files`;

CREATE TABLE IF NOT EXISTS `Files`.`Files` (
  `file_hash` VARCHAR(64) UNIQUE NOT NULL,
  `file_name` VARCHAR(1024) NOT NULL,
  `file_type` VARCHAR(255) NOT NULL,
  `file_pointer` VARCHAR(2048) NOT NULL,
  `id_code` VARCHAR(255) NOT NULL,
  `pg` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`file_hash`)
);

CREATE TABLE IF NOT EXISTS `Organizations`.`Users` (
  `user_id` INT UNSIGNED AUTO_INCREMENT UNIQUE NOT NULL,
  `person_id` INT UNSIGNED,
  `username` VARCHAR(100) UNIQUE NOT NULL,
  `encrypted_password` VARCHAR(250) NOT NULL,
  `profile_picture` VARCHAR(500),
  `color_theme` ENUM('Light','Dark'),
  `doc` json,
  PRIMARY KEY (`user_id`)
);

CREATE TABLE IF NOT EXISTS `Organizations`.`Organizations` (
  `organization_id` INT UNSIGNED AUTO_INCREMENT,
  `date_entered` DATE NULL DEFAULT NULL,
  `website_url` VARCHAR(200),
  `vetted` BOOL,
  `date_vetted` DATE NULL DEFAULT NULL,
  `risk_level` ENUM("UNKNOWN", "No_Risk", "Low_Risk", "Medium_Risk", "High_Risk"),
  `supplier` BOOL DEFAULT false,
  `client` BOOL DEFAULT false,
  `lab` BOOL DEFAULT false,
  `courier` BOOL DEFAULT false,
  `other` BOOL DEFAULT false,
  `doc` json,
  `notes` VARCHAR(2500),
  PRIMARY KEY (`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Organizations`.`Organization_Names` (
  `name_id` INT UNSIGNED AUTO_INCREMENT,
  `organization_id` INT UNSIGNED,
  `organization_name` VARCHAR(200) NOT NULL,
  `organization_initial` VARCHAR(10) NOT NULL,
  `primary_name` BOOL DEFAULT false,
  PRIMARY KEY (`name_id`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`),
  INDEX ( `organization_name` ),
  INDEX ( `organization_initial` )
);

CREATE TABLE IF NOT EXISTS `Organizations`.`Facilities` (
  `facility_id` INT UNSIGNED AUTO_INCREMENT,
  `organization_id` INT UNSIGNED,
  `building_name` VARCHAR(500),
  `building_type` ENUM('Head_Office', 'Office', 'Distribution_Warehouse', 'Manufacturing_Facility', 'Storefront') NOT NULL,
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
  `ship_time_units` ENUM( "Unknown", "Days", "Weeks", "Months") NOT NULL,
  `ship_time_in_days` INT,
  `notes` VARCHAR(2500),
  PRIMARY KEY (`facility_id`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Products`.`Product_Master` (
  `product_id` INT UNSIGNED AUTO_INCREMENT,
  `organization_id` INT UNSIGNED,
  `product_name` VARCHAR(300) NOT NULL,
  `type` ENUM('Powder','Capsule', 'Liquid','Other') NOT NULL,
  `current_product` BOOL,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `spec_issue_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `spec_revise_date` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `exp_time_frame` SMALLINT,
  `exp_unit` ENUM('Years','Months','Days') NOT NULL,
  `exp_type` ENUM('Best_By', 'Exp') NOT NULL,
  `exp_use_oldest_ingredient` BOOL,
  `default_formula_id` INT UNSIGNED DEFAULT NULL,
  `certified_usda_organic` BOOL DEFAULT FALSE,
  `certified_halal` BOOL DEFAULT FALSE,
  `certified_kosher` BOOL DEFAULT FALSE,
  `certified_gluten_free` BOOL DEFAULT FALSE,
  `certified_national_sanitation_foundation` BOOL DEFAULT FALSE,
  `certified_us_pharmacopeia` BOOL DEFAULT FALSE,
  `certified_non_gmo` BOOL DEFAULT FALSE,
  `certified_vegan` BOOL DEFAULT FALSE,
  `doc` json,
  PRIMARY KEY (`product_id`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Inventory`.`Components` (
  `component_id` INT UNSIGNED AUTO_INCREMENT,
  `component_type` ENUM(
    'powder', 
    'liquid', 
    'container', 
    'pouch', 
    'shrink_band', 
    'lid', 
    'label', 
    'capsule', 
    'misc', 
    'scoop', 
    'desiccant', 
    'box', 
    'carton', 
    'packaging_material'
  ) NOT NULL,
  `units` ENUM(
    "grams", 
    "kilograms", 
    "units", 
    "boxes", 
    "pallets", 
    "liters", 
    "rolls", 
    "totes", 
    "barrels", 
    "pounds"
  ) NOT NULL,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `doc` json,
  `certified_usda_organic` BOOL DEFAULT FALSE,
  `certified_halal` BOOL DEFAULT FALSE,
  `certified_kosher` BOOL DEFAULT FALSE,
  `certified_gluten_free` BOOL DEFAULT FALSE,
  `certified_national_sanitation_foundation` BOOL DEFAULT FALSE,
  `certified_us_pharmacopeia` BOOL DEFAULT FALSE,
  `certified_non_gmo` BOOL DEFAULT FALSE,
  `certified_vegan` BOOL DEFAULT FALSE,
  `brand_id` INT UNSIGNED,
  PRIMARY KEY (`component_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Inventory`.`Component_Names` (
  `name_id` INT UNSIGNED AUTO_INCREMENT,
  `component_id` INT UNSIGNED,
  `component_name` VARCHAR(300) NOT NULL,
  `primary_name` BOOL DEFAULT 0,
  `botanical_name` BOOL DEFAULT 0,
  PRIMARY KEY (`name_id`),
  FOREIGN KEY (`component_id`) REFERENCES `Inventory`.`Components`(`component_id`),
  INDEX ( `component_name` )
);

CREATE TABLE IF NOT EXISTS `Inventory`.`Item_id` (
  `item_id` INT UNSIGNED AUTO_INCREMENT,
  `component_id` INT UNSIGNED DEFAULT NULL,
  `product_id` INT UNSIGNED DEFAULT NULL,
  PRIMARY KEY (`item_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`),
  FOREIGN KEY (`component_id`) REFERENCES `Inventory`.`Components`(`component_id`)
);

CREATE TABLE IF NOT EXISTS `Inventory`.`Inventory` (
  `inv_id` INT UNSIGNED AUTO_INCREMENT,
  `item_id` INT UNSIGNED,
  `owner_id` INT UNSIGNED,
  `is_component` BOOL,
  `is_product` BOOL,
  `actual_inventory` DECIMAL(16,4) DEFAULT 0,
  `theoretical_inventory` DECIMAL(16,4) DEFAULT 0,
  `recent_cycle_count_id` INT UNSIGNED,
  PRIMARY KEY (`inv_id`, `owner_id`, `item_id`),
  FOREIGN KEY (`item_id`) REFERENCES `Inventory`.`Item_id`(`item_id`),
  FOREIGN KEY (`owner_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Orders`.`Purchase_Orders` (
  `prefix` VARCHAR(10) DEFAULT "" NOT NULL,
  `year` TINYINT NOT NULL,
  `month` TINYINT NOT NULL,
  `sec_number` SMALLINT NOT NULL,
  `suffix` VARCHAR(10) DEFAULT "" NOT NULL,
  `organization_id` INT UNSIGNED,
  `supplier_so_num` VARCHAR(30),
  `order_date` DATE,
  `eta_date` DATE,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `doc` json DEFAULT (CONCAT('{"_id":"',`prefix`, `year`, `month`, `sec_number`, `suffix`,'","files":[]}')),
  PRIMARY KEY (`prefix`, `year`, `month`, `sec_number`, `suffix`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Orders`.`Purchase_Order_Detail` (
  `po_detail_id` INT UNSIGNED AUTO_INCREMENT,
  `prefix` VARCHAR(10) DEFAULT "" NOT NULL,
  `year` TINYINT NOT NULL,
  `month` TINYINT NOT NULL,
  `sec_number` SMALLINT NOT NULL,
  `suffix` VARCHAR(10) DEFAULT "" NOT NULL,
  `component_id` INT UNSIGNED NOT NULL,
  `unit_order_qty` INT,
  `kilos_order_qty` DECIMAL(16,4),
  `special_instructions` VARCHAR(2000),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `bid_price_per_unit` DECIMAL(16,4),
  `bid_price_per_kilo` DECIMAL(16,4),
  `doc` json,
  PRIMARY KEY (`po_detail_id`),
  FOREIGN KEY (`prefix`, `year`, `month`, `sec_number`, `suffix`) REFERENCES `Orders`.`Purchase_Orders`(`prefix`, `year`, `month`, `sec_number`, `suffix`),
  FOREIGN KEY (`component_id`) REFERENCES `Inventory`.`Components`(`component_id`)
);

CREATE TABLE IF NOT EXISTS `Products`.`Manufacturing_Process` (
  `process_spec_id` INT UNSIGNED AUTO_INCREMENT,
  `product_id` INT UNSIGNED,
  `processes_collection` JSON,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `current_default_process` BOOL,
  PRIMARY KEY (`process_spec_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`)
);

CREATE TABLE IF NOT EXISTS `Manufacturing`.`Processes` (
  `process_id` INT UNSIGNED AUTO_INCREMENT,
  `process_name` VARCHAR(100) NOT NULL,
  `process_sop_id` VARCHAR(30),
  `doc` json,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`process_id`)
);

CREATE TABLE IF NOT EXISTS `Organizations`.`People` (
  `person_id` INT UNSIGNED AUTO_INCREMENT,
  `organization_id` INT UNSIGNED,
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
  `prefix` VARCHAR(10) DEFAULT "" NOT NULL,
  `year` TINYINT NOT NULL,
  `month` TINYINT NOT NULL,
  `sec_number` SMALLINT NOT NULL,
  `suffix` VARCHAR(10) DEFAULT "" NOT NULL,
  `organization_id` INT UNSIGNED NOT NULL,
  `client_po_num` VARCHAR(30),
  `order_date` DATE,
  `target_completion_date` DATE,
  `completion_date` DATE,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `doc` json DEFAULT (CONCAT('{"_id":"',`prefix`, `year`, `month`, `sec_number`, `suffix`, '","files":[]}')),
  `billed_date` DATE,
  `closed_date` DATE,
  `down_payment_actual` DOUBLE,
  `theoretical_po_amount` DOUBLE,
  `total_paid` DOUBLE,
  PRIMARY KEY (`prefix`, `year`, `month`, `sec_number`, `suffix`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Orders`.`Sales_Orders_Payments` (
  `prefix` VARCHAR(10) DEFAULT "" NOT NULL,
  `year` TINYINT NOT NULL,
  `month` TINYINT NOT NULL,
  `sec_number` SMALLINT NOT NULL,
  `suffix` VARCHAR(10) DEFAULT "" NOT NULL,
  `organization_id` INT,
  `payment_amount` DOUBLE,
  `payment_date` DATE,
  `payment_type` ENUM("down_payment", "other", "final_payment") NOT NULL,
  `payment_notes` VARCHAR(2500),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `doc` json DEFAULT (CONCAT('{"_id":"',`prefix`, `year`, `month`, `sec_number`, `suffix`, '","files":[]}')),
  PRIMARY KEY (`prefix`, `year`, `month`, `sec_number`, `suffix`),
  FOREIGN KEY (`prefix`, `year`, `month`, `sec_number`, `suffix`) REFERENCES `Orders`.`Sales_Orders`(`prefix`, `year`, `month`, `sec_number`, `suffix`)
);

CREATE TABLE IF NOT EXISTS `Orders`.`Sale_Order_Detail` (
  `so_detail_id` INT UNSIGNED AUTO_INCREMENT,
  `prefix` VARCHAR(10) DEFAULT "" NOT NULL,
  `year` TINYINT NOT NULL,
  `month` TINYINT NOT NULL,
  `sec_number` SMALLINT NOT NULL,
  `suffix` VARCHAR(10) DEFAULT "" NOT NULL,
  `product_id` INT UNSIGNED NOT NULL,
  `unit_order_qty` INT,
  `kilos_order_qty` DECIMAL(16,4),
  `special_instructions` VARCHAR(2000),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `bid_price_per_unit` DECIMAL(16,4),
  `final_ship_date` DATE,
  `doc` json,
  PRIMARY KEY (`so_detail_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`),
  FOREIGN KEY (`prefix`, `year`, `month`, `sec_number`, `suffix`) REFERENCES `Orders`.`Sales_Orders`(`prefix`, `year`, `month`, `sec_number`, `suffix`)
);

CREATE TABLE IF NOT EXISTS `Orders`.`Sales_Orders_Payments` (
  `payment_id` INT UNSIGNED AUTO_INCREMENT,
  `prefix` VARCHAR(10) DEFAULT "" NOT NULL,
  `year` TINYINT NOT NULL,
  `month` TINYINT NOT NULL,
  `sec_number` SMALLINT NOT NULL,
  `suffix` VARCHAR(10) DEFAULT "" NOT NULL,
  `payment_amount` DOUBLE,
  `payment_type` ENUM("down_payment", "other", "final_payment") NOT NULL,
  `payment_notes` VARCHAR(2500),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `doc` JSON,
  PRIMARY KEY (`payment_id`),
  FOREIGN KEY (`prefix`, `year`, `month`, `sec_number`, `suffix`) REFERENCES `Orders`.`Sales_Orders`(`prefix`, `year`, `month`, `sec_number`, `suffix`)
);

CREATE TABLE IF NOT EXISTS `Orders`.`Lot_Numbers` (
  `prefix` VARCHAR(15) DEFAULT "" NOT NULL,
  `year` TINYINT NOT NULL,
  `month` TINYINT NOT NULL,
  `sec_number` SMALLINT NOT NULL,
  `suffix` VARCHAR(15) DEFAULT "" NOT NULL,
  `product_id` INT UNSIGNED NOT NULL,
  `prolifix_lot_number` VARCHAR(20) DEFAULT (CONCAT(`prefix`, LPAD(`year`,2,"0"), LPAD(`month`,2,"0"), LPAD(`sec_number`,3,"0"), `suffix`)),
  `so_detail_id` INT UNSIGNED,
  `target_unit_yield` INT,
  `actual_unit_yield` INT,
  `retentions` INT,
  `total_shippable_product` INT,
  `doc` json DEFAULT (CONCAT('{"_id":"',`prolifix_lot_number`,'"}')),
  `batch_printed` BOOL,
  `bpr_printed` BOOL,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `exp_date` DATE,
  `exp_type` ENUM('Best By', 'Exp') NOT NULL,
  PRIMARY KEY (`prefix`, `year`, `month`, `sec_number`, `suffix`),
  FOREIGN KEY (`so_detail_id`) REFERENCES `Orders`.`Sale_Order_Detail`(`so_detail_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`)
);

CREATE TABLE IF NOT EXISTS `Products`.`Materials` (
  `material_id` INT UNSIGNED AUTO_INCREMENT,
  `component_id` INT UNSIGNED,
  `product_id` INT UNSIGNED,
  `material_qty_per_unit` INT NOT NULL,
  `current_default_component` BOOL NOT NULL,
  `component_list_version` SMALLINT NOT NULL,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`material_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`),
  FOREIGN KEY (`component_id`) REFERENCES `Inventory`.`Components`(`component_id`)
);

CREATE TABLE IF NOT EXISTS `Inventory`.`Inventory_Log` (
  `log_id` INT UNSIGNED AUTO_INCREMENT,
  `inv_id` INT UNSIGNED,
  `courier_id` INT UNSIGNED DEFAULT NULL,
  `facility_id` INT UNSIGNED DEFAULT NULL,
  `user_id` INT UNSIGNED,
  `po_detail_id` INT UNSIGNED DEFAULT NULL,
  `so_detail_id` INT UNSIGNED DEFAULT NULL,
  `previous_log_id` INT UNSIGNED DEFAULT NULL,
  `pre_change_actual_inventory` INT NOT NULL,
  `post_change_actual_inventory` INT NOT NULL,
  `pre_change_theoretic_inventory` INT NOT NULL,
  `post_change_theoretic_inventory` INT NOT NULL,
  `cycle_count_grade` BOOL DEFAULT NULL,
  `archived_tree` BOOL DEFAULT false,
  `supplier_item_id` VARCHAR(255),
  `lot_number` VARCHAR(255),
  `batch_number` VARCHAR(255),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `doc` JSON,
  `state` ENUM( 'Ordered', 'Revised_Order_Decreased', 'Revised_Order_Increased', 'In_Transit', 'Back_Order',  'Checkin_Quarantine', 'Received', 'Produced', 'Cycle_Count', 'Released', 'Returned', 'Allocated', 'Batched', 'Used', 'Quarantined', 'Lost', 'Expired', 'Wasted', 'Damaged', 'Destroyed', 'Shipped') NOT NULL,
  `state_notes` VARCHAR(1024),
  PRIMARY KEY (`log_id`),
  FOREIGN KEY (`inv_id`) REFERENCES `Inventory`.`Inventory`(`inv_id`),
  FOREIGN KEY (`facility_id`) REFERENCES `Organizations`.`Facilities`(`facility_id`),
  FOREIGN KEY (`courier_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`),
  FOREIGN KEY (`po_detail_id`) REFERENCES `Orders`.`Purchase_Order_Detail`(`po_detail_id`),
  FOREIGN KEY (`so_detail_id`) REFERENCES `Orders`.`Sale_Order_Detail`(`so_detail_id`),
  FOREIGN KEY (`user_id`) REFERENCES `Organizations`.`Users`(`user_id`)
);

CREATE TABLE IF NOT EXISTS `Formulas`.`Formula_Master` (
  `formula_id` INT UNSIGNED AUTO_INCREMENT,
  `product_id` INT UNSIGNED,
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
  `label_id` INT UNSIGNED,
  PRIMARY KEY (`formula_id`),
  FOREIGN KEY (`label_id`) REFERENCES `Inventory`.`Components`(`component_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`)
);

CREATE TABLE IF NOT EXISTS `Formulas`.`Formula_Detail` (
  `formula_ingredient_id` INT UNSIGNED AUTO_INCREMENT,
  `formula_id` INT UNSIGNED,
  `percent` DOUBLE,
  `mg_per_capsule` DOUBLE,
  `ml_per_unit` DOUBLE,
  `grams_per_unit` DOUBLE,
  `organic_spec` ENUM('organic', 'non_organic', 'cut_and_sifted', 'organic_or_wildcrafted', 'wildcrafted', 'any') NOT NULL,
  `ingredient_id` INT UNSIGNED,
  `notes` VARCHAR(1000),
  `brand_specific` BOOL,
  `organic_specific` BOOL,
  PRIMARY KEY (`formula_ingredient_id`),
  FOREIGN KEY (`ingredient_id`) REFERENCES `Inventory`.`Components`(`component_id`),
  FOREIGN KEY (`formula_id`) REFERENCES `Formulas`.`Formula_Master`(`formula_id`)
);

CREATE TABLE IF NOT EXISTS `Manufacturing`.`Equipment` (
  `equipment_id` INT UNSIGNED AUTO_INCREMENT,
  `process_id` INT UNSIGNED,
  `equipment_sn` VARCHAR(50),
  `status` ENUM('Working_Order', 'Broken', 'Removed') NOT NULL,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `equipment_history` JSON,
  PRIMARY KEY (`equipment_id`),
  FOREIGN KEY (`process_id`) REFERENCES `Manufacturing`.`Processes`(`process_id`)
);

CREATE TABLE IF NOT EXISTS `Formulas`.`Client_Spec_Group` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `formula_ingredient_id` INT UNSIGNED,
  `brand_id` INT UNSIGNED,
  `organic_spec` ENUM('organic', 'non_organic', 'cut_and_sifted', 'organic_or_wildcrafted', 'wildcrafted', 'any') NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`formula_ingredient_id`) REFERENCES `Formulas`.`Formula_Detail`(`formula_ingredient_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Formulas`.`Quaternary_Group` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `formula_id` INT UNSIGNED,
  `brand_id` INT UNSIGNED,
  `organic_spec` ENUM('organic', 'non_organic', 'cut_and_sifted', 'organic_or_wildcrafted', 'wildcrafted', 'any') NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`formula_id`) REFERENCES `Formulas`.`Formula_Detail`(`formula_ingredient_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Formulas`.`Tertiary_Group` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `formula_ingredient_id` INT UNSIGNED,
  `brand_id` INT UNSIGNED,
  `organic_spec` ENUM('organic', 'non_organic', 'cut_and_sifted', 'organic_or_wildcrafted', 'wildcrafted', 'any') NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`formula_ingredient_id`) REFERENCES `Formulas`.`Formula_Detail`(`formula_ingredient_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Formulas`.`Secondary_Group` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `formula_ingredient_id` INT UNSIGNED,
  `brand_id` INT UNSIGNED,
  `organic_spec` ENUM('organic', 'non_organic', 'cut_and_sifted', 'organic_or_wildcrafted', 'wildcrafted', 'any') NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`formula_ingredient_id`) REFERENCES `Formulas`.`Formula_Detail`(`formula_ingredient_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Formulas`.`Primary_Group` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `formula_ingredient_id` INT UNSIGNED,
  `brand_id` INT UNSIGNED,
  `organic_spec` ENUM('organic', 'non_organic', 'cut_and_sifted', 'organic_or_wildcrafted', 'wildcrafted', 'any') NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`formula_ingredient_id`) REFERENCES `Formulas`.`Formula_Detail`(`formula_ingredient_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);