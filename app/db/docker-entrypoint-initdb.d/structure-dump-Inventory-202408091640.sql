-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 192.168.1.133    Database: Inventory
-- ------------------------------------------------------
-- Server version	5.5.5-10.11.7-MariaDB-1:10.11.7+maria~ubu2204

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `Inventory`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Inventory` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `Inventory`;

--
-- Table structure for table `Component_Names`
--

DROP TABLE IF EXISTS `Component_Names`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Component_Names` (
  `name_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `component_id` int(10) unsigned DEFAULT NULL,
  `component_name` varchar(300) NOT NULL,
  `primary_name` tinyint(1) DEFAULT 0,
  `botanical_name` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`name_id`),
  KEY `component_id` (`component_id`),
  KEY `component_name` (`component_name`),
  CONSTRAINT `component_id` FOREIGN KEY (`component_id`) REFERENCES `Components` (`component_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1142 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Components`
--

DROP TABLE IF EXISTS `Components`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Components` (
  `component_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `component_type` enum('powder','liquid','container','pouch','shrink_band','lid','label','capsule','misc','scoop','desiccant','box','carton','packaging_material') NOT NULL,
  `units` enum('grams','kilograms','units','boxes','pallets','liters','rolls','totes','barrels','pounds') NOT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `doc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`doc`)),
  `certified_usda_organic` tinyint(1) DEFAULT 0,
  `certified_halal` tinyint(1) DEFAULT 0,
  `certified_kosher` tinyint(1) DEFAULT 0,
  `certified_gluten_free` tinyint(1) DEFAULT 0,
  `certified_national_sanitation_foundation` tinyint(1) DEFAULT 0,
  `certified_us_pharmacopeia` tinyint(1) DEFAULT 0,
  `certified_non_gmo` tinyint(1) DEFAULT 0,
  `certified_vegan` tinyint(1) DEFAULT 0,
  `brand_id` int(10) unsigned DEFAULT NULL,
  `certified_fda` tinyint(1) NOT NULL DEFAULT 0,
  `certified_wildcrafted` tinyint(1) DEFAULT 0,
  `certified_made_with_organic` tinyint(1) DEFAULT 0,
  `certified_gmp` tinyint(1) DEFAULT 0,
  `primary_name_id` int(10) unsigned DEFAULT NULL,
  `is_label` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`component_id`),
  KEY `brand_id` (`brand_id`),
  CONSTRAINT `Components_ibfk_1` FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations` (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=480 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Inventory`
--

DROP TABLE IF EXISTS `Inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Inventory` (
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
  KEY `lot_number` (`lot_number`),
  CONSTRAINT `Inventory_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `Item_id` (`item_id`),
  CONSTRAINT `Inventory_ibfk_2` FOREIGN KEY (`owner_id`) REFERENCES `Organizations`.`Organizations` (`organization_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Inventory_Log`
--

DROP TABLE IF EXISTS `Inventory_Log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Inventory_Log` (
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
  `position` varchar(30) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Inventory_Log_Edges`
--

DROP TABLE IF EXISTS `Inventory_Log_Edges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Inventory_Log_Edges` (
  `source` int(10) unsigned NOT NULL,
  `target` int(10) unsigned NOT NULL,
  `inv_id` int(10) unsigned NOT NULL,
  `label` varchar(255) DEFAULT NULL,
  `animated` tinyint(1) DEFAULT 0,
  `marker_end` enum('Arrow','ArrowClosed') DEFAULT 'ArrowClosed',
  PRIMARY KEY (`source`,`target`),
  KEY `target` (`target`),
  KEY `inv_id` (`inv_id`),
  CONSTRAINT `Inventory_Log_Edges_ibfk_1` FOREIGN KEY (`target`) REFERENCES `Inventory_Log` (`log_id`),
  CONSTRAINT `Inventory_Log_Edges_ibfk_2` FOREIGN KEY (`source`) REFERENCES `Inventory_Log` (`log_id`),
  CONSTRAINT `Inventory_Log_Edges_ibfk_3` FOREIGN KEY (`inv_id`) REFERENCES `Inventory` (`inv_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Item_id`
--

DROP TABLE IF EXISTS `Item_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Item_id` (
  `item_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `component_id` int(10) unsigned DEFAULT NULL,
  `product_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`item_id`),
  KEY `product_id` (`product_id`),
  KEY `component_id` (`component_id`),
  CONSTRAINT `Item_id_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master` (`product_id`),
  CONSTRAINT `Item_id_ibfk_2` FOREIGN KEY (`component_id`) REFERENCES `Components` (`component_id`)
) ENGINE=InnoDB AUTO_INCREMENT=279 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'Inventory'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-09 16:40:12
