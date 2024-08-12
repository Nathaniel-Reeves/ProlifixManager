-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 192.168.1.133    Database: Products
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
-- Current Database: `Products`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Products` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `Products`;

--
-- Table structure for table `Component_Brands_Join`
--

DROP TABLE IF EXISTS `Component_Brands_Join`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Component_Brands_Join` (
  `_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `brand_id` int(10) unsigned NOT NULL,
  `process_component_id` int(10) unsigned NOT NULL,
  `priority` int(11) NOT NULL,
  PRIMARY KEY (`_id`),
  KEY `brand_id` (`brand_id`),
  CONSTRAINT `Component_Brands_Join_ibfk_2` FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations` (`organization_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Components_Join`
--

DROP TABLE IF EXISTS `Components_Join`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Components_Join` (
  `_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `process_component_id` int(10) unsigned NOT NULL,
  `component_id` int(10) unsigned NOT NULL,
  `priority` int(11) NOT NULL,
  PRIMARY KEY (`_id`),
  KEY `process_component_id` (`process_component_id`),
  KEY `component_id` (`component_id`),
  CONSTRAINT `Components_Join_ibfk_1` FOREIGN KEY (`process_component_id`) REFERENCES `Process_Components` (`process_component_id`),
  CONSTRAINT `Components_Join_ibfk_2` FOREIGN KEY (`component_id`) REFERENCES `Inventory`.`Components` (`component_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Formula_Detail`
--

DROP TABLE IF EXISTS `Formula_Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Formula_Detail` (
  `formula_ingredient_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `formula_id` int(10) unsigned DEFAULT NULL,
  `percent` double DEFAULT NULL,
  `mg_per_capsule` double DEFAULT NULL,
  `ml_per_unit` double DEFAULT NULL,
  `grams_per_unit` double DEFAULT NULL,
  `notes` varchar(1000) DEFAULT NULL,
  `approved_brands` int(10) unsigned DEFAULT NULL,
  `approved_ingredients` int(10) unsigned DEFAULT NULL,
  `specific_brand_required` tinyint(1) DEFAULT 0,
  `specific_ingredient_required` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`formula_ingredient_id`),
  KEY `formula_id` (`formula_id`),
  CONSTRAINT `Formula_Detail_ibfk_1` FOREIGN KEY (`formula_id`) REFERENCES `Formula_Master` (`formula_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Formula_Master`
--

DROP TABLE IF EXISTS `Formula_Master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Formula_Master` (
  `formula_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned DEFAULT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `formulation_version` int(10) unsigned DEFAULT NULL,
  `notes` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`formula_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `Formula_Master_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Product_Master` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Ingredient_Brands_Join`
--

DROP TABLE IF EXISTS `Ingredient_Brands_Join`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ingredient_Brands_Join` (
  `_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `formula_ingredient_id` int(10) unsigned NOT NULL,
  `brand_id` int(10) unsigned NOT NULL,
  `priority` int(11) NOT NULL,
  PRIMARY KEY (`_id`),
  KEY `brand_id` (`brand_id`),
  KEY `formula_ingredient_id` (`formula_ingredient_id`),
  CONSTRAINT `Ingredient_Brands_Join_ibfk_1` FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations` (`organization_id`),
  CONSTRAINT `Ingredient_Brands_Join_ibfk_2` FOREIGN KEY (`formula_ingredient_id`) REFERENCES `Formula_Detail` (`formula_ingredient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Ingredients_Join`
--

DROP TABLE IF EXISTS `Ingredients_Join`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ingredients_Join` (
  `_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `formula_ingredient_id` int(10) unsigned NOT NULL,
  `ingredient_id` int(10) unsigned NOT NULL,
  `priority` int(11) NOT NULL,
  PRIMARY KEY (`_id`),
  KEY `ingredient_id` (`ingredient_id`),
  KEY `formula_ingredient_id` (`formula_ingredient_id`),
  CONSTRAINT `Ingredients_Join_ibfk_1` FOREIGN KEY (`ingredient_id`) REFERENCES `Inventory`.`Components` (`component_id`),
  CONSTRAINT `Ingredients_Join_ibfk_2` FOREIGN KEY (`formula_ingredient_id`) REFERENCES `Formula_Detail` (`formula_ingredient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Manufacturing_Process`
--

DROP TABLE IF EXISTS `Manufacturing_Process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Manufacturing_Process` (
  `process_spec_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned NOT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `date_modified` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  `current_default_process` tinyint(1) DEFAULT NULL,
  `process_order` int(10) unsigned DEFAULT NULL,
  `special_instruction` varchar(2500) DEFAULT NULL,
  `manufacturing_process_id` int(10) unsigned NOT NULL,
  `manufacturing_process_version` int(10) unsigned DEFAULT NULL,
  `position` varchar(30) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `variant_id` int(10) unsigned DEFAULT NULL,
  `qty_per_box` smallint(5) unsigned DEFAULT NULL,
  `box_weight_in_lbs` double DEFAULT NULL,
  `box_sticker_required` tinyint(1) DEFAULT 0,
  `percent_loss` double DEFAULT 0,
  `target_process_rate` double DEFAULT NULL,
  `target_process_rate_unit` enum('Products','Barrels','Kilos','Liters','Capsules','Ingredients','Batches') DEFAULT NULL,
  `target_process_rate_per` double DEFAULT NULL,
  `target_process_rate_per_unit` enum('Seconds','Minutes','Hours','Days') DEFAULT NULL,
  `primary_process` tinyint(1) DEFAULT 0,
  `max_pallet_layers` tinyint(3) unsigned DEFAULT NULL,
  `box_id` int(10) unsigned DEFAULT NULL,
  `custom_setup_time` double DEFAULT NULL,
  `custom_setup_time_units` enum('Seconds','Minutes','Hours','Days') DEFAULT NULL,
  `custom_setup_num_employees` tinyint(3) unsigned DEFAULT NULL,
  `custom_setup_time_use_default` tinyint(1) DEFAULT 1,
  `custom_cleaning_time` double DEFAULT NULL,
  `custom_cleaning_time_units` enum('Seconds','Minutes','Hours','Days') DEFAULT NULL,
  `custom_cleaning_num_employees` tinyint(3) unsigned DEFAULT NULL,
  `custom_cleaning_time_use_default` tinyint(1) DEFAULT 1,
  `target_process_num_employees` tinyint(3) unsigned DEFAULT NULL,
  `bid_notes` varchar(2500) DEFAULT NULL,
  `custom_ave_percent_loss` double DEFAULT NULL,
  `use_default_ave_percent_loss` tinyint(1) DEFAULT NULL,
  `num_retentions` tinyint(3) unsigned DEFAULT 2,
  `lab_sample_size` double DEFAULT 100,
  `qc_sample_size` double DEFAULT 5,
  PRIMARY KEY (`process_spec_id`),
  KEY `product_id` (`product_id`),
  KEY `Manufacturing_Process_Product_Variant_FK` (`variant_id`),
  KEY `Manufacturing_Process_Components_FK` (`box_id`),
  CONSTRAINT `Manufacturing_Process_Components_FK` FOREIGN KEY (`box_id`) REFERENCES `Inventory`.`Components` (`component_id`),
  CONSTRAINT `Manufacturing_Process_Product_Variant_FK` FOREIGN KEY (`variant_id`) REFERENCES `Product_Variant` (`variant_id`),
  CONSTRAINT `Manufacturing_Process_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Product_Master` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Manufacturing_Process_Edges`
--

DROP TABLE IF EXISTS `Manufacturing_Process_Edges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Manufacturing_Process_Edges` (
  `source` int(10) unsigned NOT NULL,
  `target` int(10) unsigned NOT NULL,
  `product_id` int(10) unsigned NOT NULL,
  `label` varchar(255) DEFAULT NULL,
  `animated` tinyint(1) DEFAULT NULL,
  `marker_end` enum('Arrow','ArrowClosed') DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `source` (`source`),
  KEY `target` (`target`),
  CONSTRAINT `Manufacturing_Process_Edges_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Product_Master` (`product_id`),
  CONSTRAINT `Manufacturing_Process_Edges_ibfk_2` FOREIGN KEY (`source`) REFERENCES `Manufacturing_Process` (`process_spec_id`),
  CONSTRAINT `Manufacturing_Process_Edges_ibfk_3` FOREIGN KEY (`target`) REFERENCES `Manufacturing_Process` (`process_spec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Process_Components`
--

DROP TABLE IF EXISTS `Process_Components`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Process_Components` (
  `process_component_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `process_spec_id` int(10) unsigned DEFAULT NULL,
  `specific_component_required` tinyint(1) DEFAULT 0,
  `specific_brand_required` tinyint(1) DEFAULT 0,
  `qty_per_unit` double DEFAULT NULL,
  PRIMARY KEY (`process_component_id`),
  KEY `process_spec_id` (`process_spec_id`),
  CONSTRAINT `Process_Components_ibfk_1` FOREIGN KEY (`process_spec_id`) REFERENCES `Manufacturing_Process` (`process_spec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Product_Master`
--

DROP TABLE IF EXISTS `Product_Master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Product_Master` (
  `product_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int(10) unsigned DEFAULT NULL,
  `product_name` varchar(300) NOT NULL,
  `current_product` tinyint(1) DEFAULT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `spec_revise_date` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  `exp_time_frame` smallint(6) DEFAULT NULL,
  `exp_unit` enum('Years','Months','Days') NOT NULL,
  `exp_type` enum('Best_By','Exp') NOT NULL,
  `exp_use_oldest_ingredient` tinyint(1) DEFAULT NULL,
  `default_formula_id` int(10) unsigned DEFAULT NULL,
  `certified_usda_organic` tinyint(1) DEFAULT 0,
  `certified_halal` tinyint(1) DEFAULT 0,
  `certified_kosher` tinyint(1) DEFAULT 0,
  `certified_gluten_free` tinyint(1) DEFAULT 0,
  `certified_national_sanitation_foundation` tinyint(1) DEFAULT 0,
  `certified_us_pharmacopeia` tinyint(1) DEFAULT 0,
  `certified_non_gmo` tinyint(1) DEFAULT 0,
  `certified_vegan` tinyint(1) DEFAULT 0,
  `doc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `certified_fda` tinyint(1) DEFAULT 0,
  `certified_gmp` tinyint(1) DEFAULT 0,
  `certified_made_with_organic` tinyint(1) DEFAULT 0,
  `certified_wildcrafted` tinyint(1) DEFAULT 0,
  `default_formula_version` int(10) unsigned DEFAULT 1,
  `num_formula_versions` int(10) unsigned DEFAULT 1,
  `default_manufacturing_version` int(10) unsigned DEFAULT 1,
  `num_manufacturing_versions` int(10) unsigned DEFAULT 1,
  `num_product_variants` int(11) DEFAULT 0,
  PRIMARY KEY (`product_id`),
  KEY `organization_id` (`organization_id`),
  CONSTRAINT `Product_Master_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations` (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Product_Variant`
--

DROP TABLE IF EXISTS `Product_Variant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Product_Variant` (
  `variant_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned DEFAULT NULL,
  `variant_title` varchar(200) DEFAULT NULL,
  `variant_type` enum('powder','liquid','capsule') DEFAULT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `date_modified` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  `primary_variant` tinyint(1) DEFAULT NULL,
  `discontinued` tinyint(1) DEFAULT NULL,
  `discontinued_reason` varchar(1000) DEFAULT NULL,
  `notes` varchar(1000) DEFAULT NULL,
  `total_grams_per_unit` double DEFAULT NULL,
  `total_capsules_per_unit` double DEFAULT NULL,
  `total_mg_per_capsule` double DEFAULT NULL,
  `mg_empty_capsule` double DEFAULT NULL,
  `capsule_size` enum('1','2','0','00') DEFAULT NULL,
  `total_milliliters_per_unit` double DEFAULT NULL,
  `min_grams_per_unit` double DEFAULT NULL,
  `max_grams_per_unit` double DEFAULT NULL,
  `min_mg_per_capsule` double DEFAULT NULL,
  `max_mg_per_capsule` double DEFAULT NULL,
  `min_milliliters_per_unit` double DEFAULT NULL,
  `max_milliliters_per_unit` double DEFAULT NULL,
  `variant_title_suffix` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`variant_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `Product_Variant_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Product_Master` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'Products'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-12 15:45:28
