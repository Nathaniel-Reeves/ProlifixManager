-- Refresh Databases
DROP TABLE IF EXISTS `Inventory`.`Check-in_Log`;
DROP TABLE IF EXISTS `Inventory`.`Check-out_Log`;
DROP TABLE IF EXISTS `Inventory`.`Cycle_Counts_Log`;
DROP TABLE IF EXISTS `Organizations`.`User`;
DROP TABLE IF EXISTS `Organizations`.`People`;
DROP TABLE IF EXISTS `Formulas`.`Formula_Master`;
DROP TABLE IF EXISTS `Products`.`Components`;
DROP DATABASE IF EXISTS `Inventory`;
DROP DATABASE IF EXISTS `Orders`;
DROP DATABASE IF EXISTS `Products`;
DROP DATABASE IF EXISTS `Manufacturing`;
DROP DATABASE IF EXISTS `Organizations`;
DROP DATABASE IF EXISTS `Formulas`;


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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `Organizations`.`Organizations` (
  `organization_id` INT,
  `organization_name` VARCHAR(200) NOT NULL,
  `alias_name_1` VARCHAR(200),
  `alias_name_2` VARCHAR(200),
  `alias_name_3` VARCHAR(200),
  `organization_initial` VARCHAR(10) NOT NULL,
  `date_entered` DATE DEFAULT NULL,
  `website_url` VARCHAR(200),
  `vetted` BOOL,
  `date_vetted` DATE DEFAULT NULL,
  `risk_level` ENUM("UNKNOWN", "No Risk", "Low Risk", "Medium Risk", "High Risk"),
  `supplier` BOOL DEFAULT false,
  `client` BOOL DEFAULT false,
  `lab` BOOL DEFAULT false,
  `other` BOOL DEFAULT false,
  `_json_schema` json GENERATED ALWAYS AS (_utf8mb4'{"type":"object"}') VIRTUAL,
  `doc` json DEFAULT (CONCAT('{"_id":"',`organization_id`,'","files":[]}')),
  `notes` VARCHAR(2500),
  FULLTEXT INDEX `SECONDARY` (`organization_name`, `alias_name_1`, `alias_name_2`, `alias_name_3`) VISIBLE,
  PRIMARY KEY (`organization_id`),
  CONSTRAINT `Org_Org_t1_chk_1` CHECK (json_schema_valid(`_json_schema`,`doc`)) /*!80016 NOT ENFORCED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
  `ship_time_days` INT,
  `notes` VARCHAR(2500),
  PRIMARY KEY (`facility_id`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Products`.`Product_Master` (
  `product_id` VARCHAR(250),
  `organization_id` INT,
  `product_name` VARCHAR(300) NOT NULL,
  `type` ENUM('Powder',' Capsule', 'Liquid','NS'),
  `current_product` BOOL,
  `label_id` VARCHAR(250),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `spec_issue_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `spec_revise_date` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `products_collection` JSON,
  `exp_time_frame` SMALLINT,
  `exp_unit` ENUM('Years','Months','Days'),
  `exp_type` ENUM('Best By', 'Exp'),
  `exp_use_oldest_ingredient` BOOL,
  PRIMARY KEY (`product_id`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Inventory`.`Components` (
  `component_id` VARCHAR(250),
  `component_name` VARCHAR(300),
  `component_type` Enum('Powder', 'Liquid', 'Jar/Container', 'Bag', 'Shrink Band', 'Lid/Cap', 'Label', 'Capsule', 'MISC', 'Scoop', 'Desiccant', 'Box/Carton', 'Packaging Material'),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `owner_id` INT,
  `component_collection` JSON,
  `alias_name_1` VARCHAR(300),
  `alias_name_2` VARCHAR(300),
  `alias_name_3` VARCHAR(300),
  PRIMARY KEY (`component_id`),
  FOREIGN KEY (`owner_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE IF NOT EXISTS `Inventory`.`Inventory` (
  `inv_id` INT AUTO_INCREMENT,
  `item_id` VARCHAR(250),
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

CREATE TABLE IF NOT EXISTS `Inventory`.`Check-in_Log` (
  `check_in_id` INT AUTO_INCREMENT,
  `inv_id` INT,
  `amount` DECIMAL(16,4),
  `status` JSON,
  `user_id` INT,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`check_in_id`),
  FOREIGN KEY (`inv_id`) REFERENCES `Inventory`.`Inventory`(`inv_id`),
  FOREIGN KEY (`user_id`) REFERENCES `Organizations`.`Users`(`user_id`)
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

CREATE TABLE IF NOT EXISTS `Inventory`.`Check-out_Log` (
  `check_out_id` INT AUTO_INCREMENT,
  `inv_id` INT,
  `amount` DECIMAL(16,4),
  `status` JSON,
  `user_id` INT,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`check_out_id`),
  FOREIGN KEY (`inv_id`) REFERENCES `Inventory`.`Inventory`(`inv_id`),
  FOREIGN KEY (`user_id`) REFERENCES `Organizations`.`Users`(`user_id`)
);

CREATE TABLE IF NOT EXISTS `Products`.`Manufacturing_Process` (
  `process_spec_id` INT AUTO_INCREMENT,
  `product_id` VARCHAR(250),
  `processes_collection` JSON,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `current_default_process` BOOL,
  PRIMARY KEY (`process_spec_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`)
);

CREATE TABLE IF NOT EXISTS `Manufacturing`.`Processes` (
  `process_id` INT AUTO_INCREMENT,
  `process_name` VARCHAR(100) NOT NULL,
  `number_of_operators` TINYINT NOT NULL,
  `process_sop` VARCHAR(30),
  `process_record_template` JSON,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`process_id`)
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

CREATE TABLE IF NOT EXISTS `Orders`.`Purchase_Orders` (
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

CREATE TABLE IF NOT EXISTS `Orders`.`Purchase_Orders_Detail` (
  `po_detail_id` INT AUTO_INCREMENT,
  `prefix` VARCHAR(10),
  `year` TINYINT,
  `month` TINYINT,
  `sec_number` SMALLINT,
  `product_id` VARCHAR(250),
  `unit_order_qty` INT,
  `kilos_order_qty` DECIMAL(16,4),
  `special_instructions` VARCHAR(2000),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`po_detail_id`),
  CONSTRAINT `fk_Purchase_Orders_Detail_pk` 
	  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`),
      FOREIGN KEY (`prefix`, `year`, `month`, `sec_number`) REFERENCES `Orders`.`Purchase_Orders`(`prefix`, `year`, `month`, `sec_number`)
);

CREATE TABLE IF NOT EXISTS `Orders`.`Lot_Numbers` (
  `prefix` VARCHAR(15),
  `year` TINYINT,
  `month` TINYINT,
  `sec_number` SMALLINT,
  `suffix` VARCHAR(15),
  `product_id` VARCHAR(250),
  `po_detail_id` INT,
  `target_unit_yield` INT,
  `actual_unit_yield` INT,
  `production_runs_collection` JSON,
  `batch_printed` BOOL,
  `bpr_printed` BOOL,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `exp_date` DATE,
  `exp_type` ENUM('Best By', 'Exp'),
  PRIMARY KEY (`prefix`, `year`, `month`, `sec_number`, `suffix`),
  FOREIGN KEY (`po_detail_id`) REFERENCES `Orders`.`Purchase_Orders_Detail`(`po_detail_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`)
);

CREATE TABLE IF NOT EXISTS `Products`.`Components` (
  `component_id` INT AUTO_INCREMENT,
  `materials_id` VARCHAR(250),
  `product_id` VARCHAR(250),
  `material_qty_per_unit` INT NOT NULL,
  `current_default_component` BOOL NOT NULL,
  `component_list_version` SMALLINT NOT NULL,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`component_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`),
  FOREIGN KEY (`materials_id`) REFERENCES `Inventory`.`Components`(`component_id`)
);

CREATE TABLE `Formulas`.`Formula_Master` (
  `formula_id` INT AUTO_INCREMENT,
  `product_id` VARCHAR(250),
  `percent` DOUBLE,
  `mg_per_capsule` DOUBLE,
  `gram_per_unit` DOUBLE,
  `ml_per_unit` DOUBLE,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `formulation_version` SMALLINT,
  `organic_spec` ENUM('organic', 'non-organic', 'any'),
  `ingredient_id` VARCHAR(250),
  PRIMARY KEY (`formula_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`),
  FOREIGN KEY (`ingredient_id`) REFERENCES `Inventory`.`Components`(`component_id`)
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

CREATE TABLE `Formulas`.`Quaternary_Group` (
  `id` INT AUTO_INCREMENT,
  `formula_id` INT,
  `brand_id` INT,
  `organic_spec` ENUM('organic', 'non-organic', 'any'),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`formula_id`) REFERENCES `Formulas`.`Formula_Master`(`formula_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE `Formulas`.`Tertiary_Group` (
  `id` INT AUTO_INCREMENT,
  `formula_id` INT,
  `brand_id` INT,
  `organic_spec` ENUM('organic', 'non-organic', 'any'),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`formula_id`) REFERENCES `Formulas`.`Formula_Master`(`formula_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE `Formulas`.`Secondary_Group` (
  `id` INT AUTO_INCREMENT,
  `formula_id` INT,
  `brand_id` INT,
  `organic_spec` ENUM('organic', 'non-organic', 'any'),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`formula_id`) REFERENCES `Formulas`.`Formula_Master`(`formula_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE `Formulas`.`Primary_Group` (
  `id` INT AUTO_INCREMENT,
  `formula_id` INT,
  `brand_id` INT,
  `organic_spec` ENUM('organic', 'non-organic', 'any'),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`formula_id`) REFERENCES `Formulas`.`Formula_Master`(`formula_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

-- Create Views

USE `Organizations`;
CREATE OR REPLACE VIEW `org_and_people_detail` AS
SELECT 
	`People`.`person_id`,
    `People`.`first_name`,
    `People`.`last_name`,
    `People`.`job_description`,
    `People`.`department`,
    `People`.`phone_number_primary`,
    `People`.`phone_number_secondary`,
    `People`.`email_address_primary`,
    `People`.`email_address_secondary`,
    `People`.`birthday`,
    `People`.`is_employee`,
    `People`.`contract_date`,
    `People`.`termination_date`,
    `People`.`clock_number`,
    `Organizations`.`organization_id`,
    `Organizations`.`organization_name`,
    `Organizations`.`organization_initial`,
    `Organizations`.`alias_name_1`,
    `Organizations`.`alias_name_2`,
    `Organizations`.`alias_name_3`,
    `Organizations`.`date_entered`,
    `Organizations`.`website_url`,
    `Organizations`.`date_vetted`,
    `Organizations`.`risk_level`,
    `Organizations`.`supplier`,
    `Organizations`.`client`,
    `Organizations`.`lab`,
    `Organizations`.`other`,
    `Organizations`.`doc`,
    `Organizations`.`notes`
FROM `Organizations`
LEFT JOIN `People` ON `Organizations`.`organization_id` = `People`.`organization_id`;



