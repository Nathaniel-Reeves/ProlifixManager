-- Refresh Databases
DROP TABLE IF EXISTS `Inventory`.`Check-in_Log`;
DROP TABLE IF EXISTS `Inventory`.`Check-out_Log`;
DROP TABLE IF EXISTS `Inventory`.`Cycle_Counts_Log`;
DROP TABLE IF EXISTS `Organizations`.`User`;
DROP TABLE IF EXISTS `Organizations`.`People`;
DROP TABLE IF EXISTS `Products`.`Components`;
DROP DATABASE IF EXISTS `Inventory`;
DROP DATABASE IF EXISTS `Orders`;
DROP DATABASE IF EXISTS `Products`;
DROP DATABASE IF EXISTS `Manufacturing`;
DROP DATABASE IF EXISTS `Organizations`;


CREATE DATABASE `Organizations`;
CREATE DATABASE `Inventory`;
CREATE DATABASE `Products`;
CREATE DATABASE `Manufacturing`;
CREATE DATABASE `Orders`;

CREATE TABLE `Organizations`.`User` (
  `user_id` INT,
  `person_id` INT,
  `username` VARCHAR(100) UNIQUE NOT NULL,
  `encrypted_password` VARCHAR(250) NOT NULL,
  `_json_schema` json GENERATED ALWAYS AS (_utf8mb4'{"type":"object"}') VIRTUAL,
  `doc` json DEFAULT (CONCAT('{"_id":',`user_id`,',"access_privileges":{"human_resources":"staff", "client_relations":"staff", "supplier_relations":"staff", "production":"staff", "logistics":"staff"}}')),
  PRIMARY KEY (`user_id`),
  CONSTRAINT `Org_User_t1_chk_1` CHECK (json_schema_valid(`_json_schema`,`doc`)) /*!80016 NOT ENFORCED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Organizations`.`Organizations` (
  `organization_id` INT,
  `organization_name` VARCHAR(200) NOT NULL,
  `alias_names` VARCHAR(1000),
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
  PRIMARY KEY (`organization_id`),
  CONSTRAINT `Org_Org_t1_chk_1` CHECK (json_schema_valid(`_json_schema`,`doc`)) /*!80016 NOT ENFORCED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Organizations`.`Facilities` (
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
  `local_municipality` VARCHAR(500),
  `city_town` VARCHAR(500),
  `governing_district` VARCHAR(500),
  `postal_area` VARCHAR(100),
  `country` VARCHAR(500),
  `ship_time` INT,
  `ship_time_units` ENUM( "Unknown","Day/s", "Week/s", "Month/s"),
  `ship_time_days` INT,
  `notes` VARCHAR(2500),
  PRIMARY KEY (`facility_id`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE `Products`.`Product_Master` (
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
  PRIMARY KEY (`product_id`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE `Inventory`.`Components` (
  `component_id` VARCHAR(250),
  `component_name` VARCHAR(300),
  `brand_id` INT,
  `category` Enum('Organic Powder', 'Non-Organic Powder', 'Jar/Container', 'Bag', 'Shrink Band', 'Lid/Cap', 'Label', 'Capsule', 'MISC', 'Scoop', 'Desicant', 'Box/Carton', 'Packaging Material'),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `client_owned` INT,
  `supplier_id` INT,
  `component_collection` JSON,
  PRIMARY KEY (`component_id`),
  FOREIGN KEY (`supplier_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`),
  FOREIGN KEY (`client_owned`) REFERENCES `Organizations`.`Organizations`(`organization_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE `Inventory`.`Inventory` (
  `inv_id` INT AUTO_INCREMENT,
  `item_id` VARCHAR(250),
  `actual_inventory` DECIMAL(16,4),
  `theoretical_inventory` DECIMAL(16,4),
  `recent_cycle_count_id` INT,
  PRIMARY KEY (`inv_id`),
  FOREIGN KEY (`item_id`) REFERENCES `Products`.`Product_Master`(`product_id`),
  FOREIGN KEY (`item_id`) REFERENCES `Inventory`.`Components`(`component_id`)
);

CREATE TABLE `Inventory`.`Check-in_Log` (
  `check_in_id` INT AUTO_INCREMENT,
  `inv_id` INT,
  `amount` DECIMAL(16,4),
  `status` JSON,
  `user_id` INT,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`check_in_id`),
  FOREIGN KEY (`inv_id`) REFERENCES `Inventory`.`Inventory`(`inv_id`),
  FOREIGN KEY (`user_id`) REFERENCES `Organizations`.`User`(`user_id`)
);

CREATE TABLE `Inventory`.`Cycle_Counts_Log` (
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
  FOREIGN KEY (`user_id`) REFERENCES `Organizations`.`User`(`user_id`)
);

CREATE TABLE `Inventory`.`Check-out_Log` (
  `check_out_id` INT AUTO_INCREMENT,
  `inv_id` INT,
  `amount` DECIMAL(16,4),
  `status` JSON,
  `user_id` INT,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`check_out_id`),
  FOREIGN KEY (`inv_id`) REFERENCES `Inventory`.`Inventory`(`inv_id`),
  FOREIGN KEY (`user_id`) REFERENCES `Organizations`.`User`(`user_id`)
);

CREATE TABLE `Products`.`Manufacturing_Process` (
  `process_spec_id` INT AUTO_INCREMENT,
  `product_id` VARCHAR(250),
  `processes_collection` JSON,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `current_default_process` BOOL,
  PRIMARY KEY (`process_spec_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`)
);

CREATE TABLE `Manufacturing`.`Processes` (
  `process_id` INT AUTO_INCREMENT,
  `process_name` VARCHAR(100) NOT NULL,
  `number_of_operators` TINYINT NOT NULL,
  `process_sop` VARCHAR(30),
  `process_record_template` JSON,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`process_id`)
);

CREATE TABLE `Organizations`.`People` (
  `person_id` INT AUTO_INCREMENT,
  `organization_id` INT,
  `first_name` VARCHAR(100),
  `last_name` VARCHAR(100),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `job_title` VARCHAR(100),
  `phone_number` VARCHAR(500),
  `email_address` VARCHAR(100),
  `is_employee` BOOL,
  `hourly_wage` INT,
  `contract_date` DATE,
  `termination_date` DATE,
  PRIMARY KEY (`person_id`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE `Orders`.`Purchase_Orders` (
  `prefix` VARCHAR(10),
  `year` TINYINT,
  `month` TINYINT,
  `sec_number` SMALLINT,
  `prolifix_purchase_order_id` VARCHAR(15),
  `organization_id` INT,
  `client_po_num` VARCHAR(30),
  `order_date` DATE,
  `target_completion_date` DATE,
  `completion_date` DATE,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`prolifix_purchase_order_id`),
  FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);

CREATE TABLE `Orders`.`Purchase_Orders_Detail` (
  `po_detail_id` INT AUTO_INCREMENT,
  `prolifix_purchase_order_id` VARCHAR(15),
  `product_id` VARCHAR(250),
  `unit_order_qty` INT,
  `kilos_order_qty` DECIMAL(16,4),
  `special_instructions` VARCHAR(2000),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`po_detail_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`),
  FOREIGN KEY (`prolifix_purchase_order_id`) REFERENCES `Orders`.`Purchase_Orders`(`prolifix_purchase_order_id`)
);

CREATE TABLE `Orders`.`Lot_Numbers` (
  `prefix` VARCHAR(15),
  `year` TINYINT,
  `month` TINYINT,
  `sec_number` SMALLINT,
  `suffix` VARCHAR(15),
  `product_id` VARCHAR(250),
  `prolifix_lot_number` VARCHAR(20),
  `po_detail_id` INT,
  `target_unit_yield` INT,
  `actual_unit_yield` INT,
  `production_runs_collection` JSON,
  `batch_printed` BOOL,
  `bpr_printed` BOOL,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `exp_date` DATE,
  `exp_type` ENUM('Best By', 'Exp'),
  PRIMARY KEY (`prolifix_lot_number`),
  FOREIGN KEY (`po_detail_id`) REFERENCES `Orders`.`Purchase_Orders_Detail`(`po_detail_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`)
);

CREATE TABLE `Products`.`Components` (
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

CREATE TABLE `Products`.`Formula` (
  `formula_id` INT AUTO_INCREMENT,
  `product_id` VARCHAR(250),
  `ingredient_and_brand` JSON,
  `percent` DOUBLE,
  `mg_per_capsule` DOUBLE,
  `gram_per_unit` DOUBLE,
  `ml_per_unit` DOUBLE,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `formulation_version` SMALLINT,
  `current_default_formula` BOOL,
  PRIMARY KEY (`formula_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`)
);

CREATE TABLE `Manufacturing`.`Equipment` (
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

-- Create Views

USE `Organizations`;
CREATE OR REPLACE VIEW `org_and_people_detail` AS
SELECT 
	`People`.`person_id`,
    `People`.`first_name`,
    `People`.`last_name`,
    `People`.`job_title`,
    `People`.`phone_number`,
    `People`.`email_address`,
    `People`.`is_employee`,
    `People`.`hourly_wage`,
    `People`.`contract_date`,
    `People`.`termination_date`,
    `Organizations`.`organization_id`,
    `Organizations`.`organization_name`,
    `Organizations`.`organization_initial`,
    `Organizations`.`alias_names`,
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



-- Create Owner and Dev Accounts

-- Insert Prolifix Nutrition Information
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `website`, `supplier`, `client`, `risk_level`) VALUES (
--      "1", "Prolifix Nutrition", "PLX", "https://www.prolifixnutrition.com/", True, True, "No Risk" );

-- -- Some Client Information
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `client`) VALUES ("2", "Markus", "MK", True);
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `client`) VALUES ("3", "Maju", "MJ", True);
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `client`) VALUES ("4", "Herbally Grounded", "MG", True);

-- -- Some Supplier Information
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `supplier`) VALUES ("5", "Equadorian Rainforest", "ER", true);
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `supplier`) VALUES ("6", "Stryka", "SK", true);
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `supplier`) VALUES ("7", "Ingredients Online", "IO", true);

-- Insert Nathaniel Reeves Person Info
-- INSERT INTO `Organizations`.`People` (`organization_id`, `first_name`, `last_name`, `job_title`, `phone_number`, `email_address`, `is_employee`, `hourly_wage`, `contract_date`) VALUES 
-- 	(1, "Nathaniel", "Reeves", "Developer", "8013801953", "nathaniel.jacob.reeves@gmail.com", true, 18.50, '2020-6-16');

-- -- Insert Nathaniel Reeves User Info  (Password = testpassword)
-- INSERT INTO `Organizations`.`User` (`user_id`, `person_id`, `username`, `encrypted_password`) VALUES (1, 1, "nreeves", "pbkdf2:sha256:260000$xwmRNkYGEsbVxWQk$598deee9e52133d7d3a96eeb060c81f90b06d3ea17fb705b1e834855f5234df6");
-- UPDATE `Organizations`.`User` SET `doc` = JSON_SET(`doc`, '$.access_privileges', '{human_resources:manager, client_relations:manager, supplier_relations:manager, production:manager, logistics:manager}') WHERE `user_id` = 1;

-- -- Insert Kathy Jensen Person Info
-- INSERT INTO `Organizations`.`People` (`organization_id`, `first_name`, `last_name`, `job_title`, `phone_number`, `email_address`, `is_employee`, `hourly_wage`, `contract_date`) VALUES 
-- 	(1, "Kathy", "Jensen", "Owner", "8016025244 ", "Info@holisticlifesupplements.com", true, 0, '2016-1-1');

-- -- Insert Kathy Jensen User Info  (Password = password)
-- INSERT INTO `Organizations`.`User` (`user_id`, `person_id`, `username`, `encrypted_password`) VALUES (2, 2, "kathyj", "pbkdf2:sha256:260000$D8qPhRKS15pNXdWb$7bd4d1a2603d4365d0711b7342a1a59f67fad6354b8424e574d0654cf276ec5c");
-- UPDATE `Organizations`.`User` SET `doc` = JSON_SET(`doc`, '$.access_privileges', '{human_resources:manager, client_relations:manager, supplier_relations:manager, production:manager, logistics:manager}') WHERE `user_id` = 2;