DROP SCHEMA `Formulas`;
DROP SCHEMA `Manufacturing`;
ALTER TABLE Products.Product_Master MODIFY COLUMN `type` enum('powder','capsule','liquid') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
-- ALTER TABLE Products.Product_Master CHANGE doc lab_specifications longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL NULL;
DROP TABLE Products.Materials;
DROP TABLE Products.Manufacturing_Process;
CREATE SCHEMA `Manufacturing`;

CREATE TABLE `Products`.`Manufacturing_Process` (
  `process_spec_id` INT UNSIGNED AUTO_INCREMENT,
  `product_id` INT UNSIGNED,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `current_default_process` BOOL,
  `process_order` INT,
  `special_instruction` VARCHAR(2500),
  `manufacturing_process_id` INT UNSIGNED,
  `process_bid_cost` DECIMAL(16,4),
  PRIMARY KEY (`process_spec_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`)
);

CREATE TABLE `Manufacturing`.`Processes` (
  `process_id` INT UNSIGNED AUTO_INCREMENT,
  `process_name` VARCHAR(100) NOT NULL,
  `process_sop` VARCHAR(30),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `rework_process` BOOL,
  `min_personnel` SMALLINT,
  `max_personnel` SMALLINT,
  `component_type` Enum('container', 'pouch', 'shrink_band', 'lid', 'label', 'capsule', 'misc', 'scoop', 'desiccant', 'box', 'carton', 'packaging_material'),
  PRIMARY KEY (`process_id`)
);

CREATE TABLE `Products`.`Formula_Master` (
  `formula_id` INT UNSIGNED AUTO_INCREMENT,
  `product_id` INT UNSIGNED,
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `formulation_version` SMALLINT,
  `notes` VARCHAR(1000),
  `total_grams_per_unit` DOUBLE,
  `total_capsules_per_unit` DOUBLE,
  `total_milliliters_per_unit` DOUBLE,
  `fill_min` DOUBLE,
  `fill_max` DOUBLE,
  PRIMARY KEY (`formula_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`)
);

CREATE TABLE `Products`.`Formula_Detail` (
  `formula_ingredient_id` INT UNSIGNED AUTO_INCREMENT,
  `formula_id` INT UNSIGNED,
  `percent` DOUBLE,
  `mg_per_capsule` DOUBLE,
  `ml_per_unit` DOUBLE,
  `grams_per_unit` DOUBLE,
  `notes` VARCHAR(1000),
  `approved_brands` INT UNSIGNED,
  `approved_ingredients` INT UNSIGNED,
  `specific_brand_required` BOOL DEFAULT FALSE,
  `specific_ingredient_required` BOOL DEFAULT FALSE,
  PRIMARY KEY (`formula_ingredient_id`),
  FOREIGN KEY (`formula_id`) REFERENCES `Products`.`Formula_Master`(`formula_id`)
);

CREATE TABLE `Manufacturing`.`Equipment` (
  `equipment_id` INT UNSIGNED AUTO_INCREMENT,
  `process_id` INT UNSIGNED,
  `equipment_sn` VARCHAR(50),
  `status` ENUM('Working_Order', 'Broken', 'Removed'),
  `date_entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `date_modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `equipment_history` JSON,
  PRIMARY KEY (`equipment_id`),
  FOREIGN KEY (`process_id`) REFERENCES `Manufacturing`.`Processes`(`process_id`)
);

CREATE TABLE `Products`.`Ingredient_Brands_Join` (
  `_id` INT UNSIGNED AUTO_INCREMENT,
  `formula_ingredient_id` INT UNSIGNED,
  `brand_id` INT UNSIGNED,
  `priority` INT,
  PRIMARY KEY (`_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`),
  FOREIGN KEY (`formula_ingredient_id`) REFERENCES `Products`.`Formula_Detail`(`formula_ingredient_id`)
);

CREATE TABLE `Products`.`Ingredients_Join` (
  `_id` INT UNSIGNED AUTO_INCREMENT,
  `formula_ingredient_id` INT UNSIGNED,
  `ingredient_id` INT UNSIGNED,
  `priority` INT,
  PRIMARY KEY (`_id`),
  FOREIGN KEY (`ingredient_id`) REFERENCES `Inventory`.`Components`(`component_id`),
  FOREIGN KEY (`formula_ingredient_id`) REFERENCES `Products`.`Formula_Detail`(`formula_ingredient_id`)
);

CREATE TABLE `Products`.`Process_Components` (
  `process_component_id` INT UNSIGNED AUTO_INCREMENT,
  `process_spec_id` INT UNSIGNED,
  `specific_component_required` BOOL DEFAULT FALSE,
  `specific_brand_required` BOOL DEFAULT FALSE,
  `qty_per_unit` DOUBLE,
  PRIMARY KEY (`process_component_id`),
  FOREIGN KEY (`process_spec_id`) REFERENCES `Products`.`Manufacturing_Process`(`process_spec_id`)
);

CREATE TABLE `Products`.`Components_Join` (
  `_id` INT UNSIGNED AUTO_INCREMENT,
  `process_component_id` INT UNSIGNED,
  `component_id` INT UNSIGNED,
  `priority` INT,
  PRIMARY KEY (`_id`),
  FOREIGN KEY (`process_component_id`) REFERENCES `Products`.`Process_Components`(`process_component_id`),
  FOREIGN KEY (`component_id`) REFERENCES `Inventory`.`Components`(`component_id`)
);

CREATE TABLE `Products`.`Component_Brands_Join` (
  `_id` INT UNSIGNED AUTO_INCREMENT,
  `brand_id` INT UNSIGNED,
  `process_component_id` INT UNSIGNED,
  `priority` INT,
  PRIMARY KEY (`_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Products`.`Process_Components`(`process_component_id`),
  FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations`(`organization_id`)
);
