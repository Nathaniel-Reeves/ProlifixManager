ALTER TABLE Products.Formula_Master MODIFY COLUMN formulation_version INT UNSIGNED DEFAULT NULL NULL;
ALTER TABLE Products.Manufacturing_Process MODIFY COLUMN process_order INT UNSIGNED DEFAULT NULL NULL;
ALTER TABLE Products.Manufacturing_Process ADD manufacturing_process_version INT UNSIGNED NULL;
ALTER TABLE Products.Manufacturing_Process ADD `position` varchar(30) NULL;
ALTER TABLE Products.Manufacturing_Process ADD `type` varchar(100) NULL;
ALTER TABLE Products.Product_Master DROP COLUMN `type`;
ALTER TABLE Products.Product_Master ADD default_formula_version INT UNSIGNED DEFAULT 1 NULL;
ALTER TABLE Products.Product_Master ADD num_formula_versions INT UNSIGNED DEFAULT 1 NULL;
ALTER TABLE Products.Product_Master ADD default_manufacturing_version INT UNSIGNED DEFAULT 1 NULL;
ALTER TABLE Products.Product_Master ADD num_manufacturing_versions INT UNSIGNED DEFAULT 1 NULL;
ALTER TABLE Products.Formula_Master ADD total_mg_per_capsule DOUBLE;
ALTER TABLE Products.Formula_Master ADD mg_empty_capsule DOUBLE;
ALTER TABLE Products.Formula_Master ADD capsule_size ENUM('1','2','0','00');
ALTER TABLE Manufacturing.Processes DROP COLUMN component_type;
ALTER TABLE Manufacturing.Processes ADD bpr_page_template varchar(500) NULL;
ALTER TABLE Manufacturing.Processes ADD bpr_data_template LONGTEXT NULL;
ALTER TABLE Manufacturing.Processes ADD CONSTRAINT Processes_CHECK CHECK (json_valid(`bpr_data_template`));
ALTER TABLE Products.Product_Master CHANGE lab_specifications doc longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL NULL;
DROP TABLE Inventory.Inventory_Log;
DROP TABLE Inventory.Inventory;
CREATE TABLE `Inventory`.`Inventory` (
  `inv_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `item_id` int(10) unsigned NOT NULL,
  `owner_id` int(10) unsigned NOT NULL,
  `is_component` tinyint(1) DEFAULT NULL,
  `is_product` tinyint(1) DEFAULT NULL,
  `actual_inventory` decimal(16,4) DEFAULT 0.0000,
  `theoretical_inventory` decimal(16,4) DEFAULT 0.0000,
  `recent_cycle_count_id` int(10) unsigned DEFAULT NULL,
  `lot_number` varchar(255) NOT NULL,
  PRIMARY KEY (`inv_id`,`owner_id`,`item_id`,`lot_number`),
  KEY `item_id` (`item_id`),
  KEY `owner_id` (`owner_id`),
  Key `lot_number` (`lot_number`),
  CONSTRAINT `Inventory_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `Item_id` (`item_id`),
  CONSTRAINT `Inventory_ibfk_2` FOREIGN KEY (`owner_id`) REFERENCES `Organizations`.`Organizations` (`organization_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE `Inventory`.`Inventory_Log` (
  `log_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `inv_id` int(10) unsigned DEFAULT NULL,
  `courier_id` int(10) unsigned DEFAULT NULL,
  `facility_id` int(10) unsigned DEFAULT NULL,
  `user_id` int(10) unsigned DEFAULT NULL,
  `po_detail_id` int(10) unsigned DEFAULT NULL,
  `so_detail_id` int(10) unsigned DEFAULT NULL,
  `pre_change_actual_inventory` int(11) NOT NULL,
  `post_change_actual_inventory` int(11) NOT NULL,
  `pre_change_theoretic_inventory` int(11) NOT NULL,
  `post_change_theoretic_inventory` int(11) NOT NULL,
  `cycle_count_grade` tinyint(1) DEFAULT NULL,
  `archived_tree` tinyint(1) DEFAULT 0,
  `supplier_item_id` varchar(255) DEFAULT NULL,
  `lot_number` varchar(255) DEFAULT NULL,
  `batch_number` varchar(255) DEFAULT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `doc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`doc`)),
  `state` enum('Ordered','Revised_Order_Decreased','Revised_Order_Increased','In_Transit','Back_Order','Checkin_Quarantine','Received','Produced','Cycle_Count','Released','Returned','Allocated','Batched','Used','Quarantined','Lost','Expired','Wasted','Damaged','Destroyed','Shipped') NOT NULL,
  `state_notes` varchar(1024) DEFAULT NULL,
  `position` varchar(30),
  `type` varchar(100),
  PRIMARY KEY (`log_id`),
  KEY `inv_id` (`inv_id`),
  KEY `facility_id` (`facility_id`),
  KEY `courier_id` (`courier_id`),
  KEY `po_detail_id` (`po_detail_id`),
  KEY `so_detail_id` (`so_detail_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `Inventory_Log_ibfk_1` FOREIGN KEY (`inv_id`) REFERENCES `Inventory` (`inv_id`),
  CONSTRAINT `Inventory_Log_ibfk_2` FOREIGN KEY (`facility_id`) REFERENCES `Organizations`.`Facilities` (`facility_id`),
  CONSTRAINT `Inventory_Log_ibfk_3` FOREIGN KEY (`courier_id`) REFERENCES `Organizations`.`Organizations` (`organization_id`),
  CONSTRAINT `Inventory_Log_ibfk_4` FOREIGN KEY (`po_detail_id`) REFERENCES `Orders`.`Purchase_Order_Detail` (`po_detail_id`),
  CONSTRAINT `Inventory_Log_ibfk_5` FOREIGN KEY (`so_detail_id`) REFERENCES `Orders`.`Sale_Order_Detail` (`so_detail_id`),
  CONSTRAINT `Inventory_Log_ibfk_6` FOREIGN KEY (`user_id`) REFERENCES `Organizations`.`Users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE `Inventory`.`Inventory_Log_Edges` (
  `source` INT UNSIGNED NOT NULL,
  `target` INT UNSIGNED NOT NULL,
  `inv_id` INT UNSIGNED NOT NULL,
  `label` VARCHAR(255),
  `animated` BOOL DEFAULT FALSE,
  `marker_end` ENUM('Arrow','ArrowClosed') DEFAULT 'ArrowClosed',
  PRIMARY KEY (`source`, `target`),
  KEY (`target`),
  FOREIGN KEY (`target`) REFERENCES `Inventory`.`Inventory_Log`(`log_id`),
  FOREIGN KEY (`source`) REFERENCES `Inventory`.`Inventory_Log`(`log_id`),
  FOREIGN KEY (`inv_id`) REFERENCES `Inventory`.`Inventory`(`inv_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE `Inventory`.`Inventory_Log_Graph`
ENGINE=OQGRAPH
data_table='Inventory_Log_Edges' origid='source' destid='target';
CREATE TABLE `Products`.`Manufacturing_Process_Edges` (
  `source` INT UNSIGNED NOT NULL,
  `target` INT UNSIGNED NOT NULL,
  `product_id` INT UNSIGNED NOT NULL,
  `label` VARCHAR(255),
  `animated` BOOL DEFAULT FALSE,
  `marker_end` ENUM('Arrow','ArrowClosed') DEFAULT 'ArrowClosed',
  PRIMARY KEY (`source`, `target`),
  KEY (`target`),
  FOREIGN KEY (`source`) REFERENCES `Products`.`Manufacturing_Process`(`process_spec_id`),
  FOREIGN KEY (`target`) REFERENCES `Products`.`Manufacturing_Process`(`process_spec_id`),
  FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master`(`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE `Inventory`.`Manufacturing_Process_Graph`
ENGINE=OQGRAPH
data_table='Manufacturing_Process_Edges' origid='source' destid='target';

