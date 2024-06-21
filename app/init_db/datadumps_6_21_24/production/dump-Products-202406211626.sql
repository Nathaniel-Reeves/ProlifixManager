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
-- Table structure for table `Component_Brands_Join`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Component_Brands_Join` (
  `_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `brand_id` int(10) unsigned DEFAULT NULL,
  `process_component_id` int(10) unsigned DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  PRIMARY KEY (`_id`),
  KEY `brand_id` (`brand_id`),
  CONSTRAINT `Component_Brands_Join_ibfk_1` FOREIGN KEY (`brand_id`) REFERENCES `Process_Components` (`process_component_id`),
  CONSTRAINT `Component_Brands_Join_ibfk_2` FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations` (`organization_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Component_Brands_Join`
--

LOCK TABLES `Component_Brands_Join` WRITE;
/*!40000 ALTER TABLE `Component_Brands_Join` DISABLE KEYS */;
/*!40000 ALTER TABLE `Component_Brands_Join` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Components_Join`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Components_Join` (
  `_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `process_component_id` int(10) unsigned DEFAULT NULL,
  `component_id` int(10) unsigned DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  PRIMARY KEY (`_id`),
  KEY `process_component_id` (`process_component_id`),
  KEY `component_id` (`component_id`),
  CONSTRAINT `Components_Join_ibfk_1` FOREIGN KEY (`process_component_id`) REFERENCES `Process_Components` (`process_component_id`),
  CONSTRAINT `Components_Join_ibfk_2` FOREIGN KEY (`component_id`) REFERENCES `Inventory`.`Components` (`component_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Components_Join`
--

LOCK TABLES `Components_Join` WRITE;
/*!40000 ALTER TABLE `Components_Join` DISABLE KEYS */;
/*!40000 ALTER TABLE `Components_Join` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Formula_Detail`
--

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Formula_Detail`
--

LOCK TABLES `Formula_Detail` WRITE;
/*!40000 ALTER TABLE `Formula_Detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `Formula_Detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Formula_Master`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Formula_Master` (
  `formula_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned DEFAULT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `formulation_version` int(10) unsigned DEFAULT NULL,
  `notes` varchar(1000) DEFAULT NULL,
  `total_grams_per_unit` double DEFAULT NULL,
  `total_capsules_per_unit` double DEFAULT NULL,
  `total_milliliters_per_unit` double DEFAULT NULL,
  `min_mg_per_capsule` double DEFAULT NULL,
  `max_mg_per_capsule` double DEFAULT NULL,
  `total_mg_per_capsule` double DEFAULT NULL,
  `mg_empty_capsule` double DEFAULT NULL,
  `capsule_size` enum('1','2','0','00') DEFAULT NULL,
  `min_grams_per_unit` double DEFAULT NULL,
  `max_grams_per_unit` double DEFAULT NULL,
  `min_milliliters_per_unit` double DEFAULT NULL,
  `max_milliliters_per_unit` double DEFAULT NULL,
  `capsule_weight` double DEFAULT NULL,
  PRIMARY KEY (`formula_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `Formula_Master_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Product_Master` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Formula_Master`
--

LOCK TABLES `Formula_Master` WRITE;
/*!40000 ALTER TABLE `Formula_Master` DISABLE KEYS */;
/*!40000 ALTER TABLE `Formula_Master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ingredient_Brands_Join`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ingredient_Brands_Join` (
  `_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `formula_ingredient_id` int(10) unsigned DEFAULT NULL,
  `brand_id` int(10) unsigned DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  PRIMARY KEY (`_id`),
  KEY `brand_id` (`brand_id`),
  KEY `formula_ingredient_id` (`formula_ingredient_id`),
  CONSTRAINT `Ingredient_Brands_Join_ibfk_1` FOREIGN KEY (`brand_id`) REFERENCES `Organizations`.`Organizations` (`organization_id`),
  CONSTRAINT `Ingredient_Brands_Join_ibfk_2` FOREIGN KEY (`formula_ingredient_id`) REFERENCES `Formula_Detail` (`formula_ingredient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ingredient_Brands_Join`
--

LOCK TABLES `Ingredient_Brands_Join` WRITE;
/*!40000 ALTER TABLE `Ingredient_Brands_Join` DISABLE KEYS */;
/*!40000 ALTER TABLE `Ingredient_Brands_Join` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ingredients_Join`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ingredients_Join` (
  `_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `formula_ingredient_id` int(10) unsigned DEFAULT NULL,
  `ingredient_id` int(10) unsigned DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  PRIMARY KEY (`_id`),
  KEY `ingredient_id` (`ingredient_id`),
  KEY `formula_ingredient_id` (`formula_ingredient_id`),
  CONSTRAINT `Ingredients_Join_ibfk_1` FOREIGN KEY (`ingredient_id`) REFERENCES `Inventory`.`Components` (`component_id`),
  CONSTRAINT `Ingredients_Join_ibfk_2` FOREIGN KEY (`formula_ingredient_id`) REFERENCES `Formula_Detail` (`formula_ingredient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ingredients_Join`
--

LOCK TABLES `Ingredients_Join` WRITE;
/*!40000 ALTER TABLE `Ingredients_Join` DISABLE KEYS */;
/*!40000 ALTER TABLE `Ingredients_Join` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Manufacturing_Process`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Manufacturing_Process` (
  `process_spec_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned DEFAULT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `date_modified` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  `current_default_process` tinyint(1) DEFAULT NULL,
  `process_order` int(10) unsigned DEFAULT NULL,
  `special_instruction` varchar(2500) DEFAULT NULL,
  `manufacturing_process_id` int(10) unsigned DEFAULT NULL,
  `process_bid_cost` decimal(16,4) DEFAULT NULL,
  `manufacturing_process_version` int(10) unsigned DEFAULT NULL,
  `position` varchar(30) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`process_spec_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `Manufacturing_Process_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Product_Master` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Manufacturing_Process`
--

LOCK TABLES `Manufacturing_Process` WRITE;
/*!40000 ALTER TABLE `Manufacturing_Process` DISABLE KEYS */;
/*!40000 ALTER TABLE `Manufacturing_Process` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Manufacturing_Process_Edges`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Manufacturing_Process_Edges` (
  `source` int(10) unsigned NOT NULL,
  `target` int(10) unsigned NOT NULL,
  `product_id` int(10) unsigned NOT NULL,
  `label` varchar(255) DEFAULT NULL,
  `animated` tinyint(1) DEFAULT 0,
  `marker_end` enum('Arrow','ArrowClosed') DEFAULT 'ArrowClosed',
  PRIMARY KEY (`source`,`target`),
  KEY `target` (`target`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `Manufacturing_Process_Edges_ibfk_1` FOREIGN KEY (`source`) REFERENCES `Manufacturing_Process` (`process_spec_id`),
  CONSTRAINT `Manufacturing_Process_Edges_ibfk_2` FOREIGN KEY (`target`) REFERENCES `Manufacturing_Process` (`process_spec_id`),
  CONSTRAINT `Manufacturing_Process_Edges_ibfk_3` FOREIGN KEY (`product_id`) REFERENCES `Product_Master` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Manufacturing_Process_Edges`
--

LOCK TABLES `Manufacturing_Process_Edges` WRITE;
/*!40000 ALTER TABLE `Manufacturing_Process_Edges` DISABLE KEYS */;
/*!40000 ALTER TABLE `Manufacturing_Process_Edges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Process_Components`
--

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
-- Dumping data for table `Process_Components`
--

LOCK TABLES `Process_Components` WRITE;
/*!40000 ALTER TABLE `Process_Components` DISABLE KEYS */;
/*!40000 ALTER TABLE `Process_Components` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Product_Master`
--

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
  PRIMARY KEY (`product_id`),
  KEY `organization_id` (`organization_id`),
  CONSTRAINT `Product_Master_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations` (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Product_Master`
--

LOCK TABLES `Product_Master` WRITE;
/*!40000 ALTER TABLE `Product_Master` DISABLE KEYS */;
INSERT INTO `Product_Master` VALUES (1,44,'Fiber & Spice',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(2,47,'Gold Fulvic Acid',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(3,47,'Gold Fulvic Acid',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(4,33,'Herbal Pixie Premix',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(5,33,'Viva Mix',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(6,34,'Best Start Functional Protein',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(7,34,'Limitless Protein',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(8,35,'Amazing Greens',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(9,35,'Amazing Greens',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(10,35,'Amore',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(11,35,'Breathe',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(12,35,'Fireworks',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(13,35,'Hemroid Harry',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(14,35,'Irish Sea Moss',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(15,35,'Irish Sea Moss (bladderwrack, burdock)',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(16,35,'My Secret',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(17,35,'Sweet Cheat Herbally',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(18,35,'System Cleanse Tea',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(19,36,'Blackseed Oil',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(20,36,'Dutch Chocolate Whey',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(21,36,'Earth Nutrutional Yeast',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(22,36,'Tahitian Vanilla',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(23,36,'Wheatgrass Juice',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(24,37,'Beet Juice',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(25,37,'Large Kamut Blend',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(26,37,'Small Kamut Blend',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(27,43,'Super 15 SBO',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(28,38,'Large Blackseed Oil',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(29,38,'Large Spirulina (Pouch)',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(30,38,'Small Blackseed Oil',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(31,38,'Small Spirulina (Pouch)',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(32,38,'Ashwagandha',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(33,38,'Black Seed Oil',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(34,38,'Camu Camu',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(35,35,'Candisolve',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(36,38,'Lions Mane',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(37,38,'Maca Plus',1,NULL,'2024-06-19 20:19:05',NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,'{\r\n  \"specifications\": {\r\n    \"date_issued\": \"2024-01-22T00:00:00.000000Z\",\r\n    \"date_revised\": \"2024-01-22T00:00:00.000000Z\",\r\n    \"file_pointer\": \"\",\r\n    \"revision_number\": 1,\r\n    \"id_code\": \"\",\r\n    \"description_statement\": \"A bright green fine powder.\",\r\n    \"identity_statement\": \"This ingredient is identified by in house organoleptic specs as well as microscopy specs.\",\r\n    \"purity_statement\": \"This ingredient is verified for purity via the supplier\'s Certificate of Analysis. We verify this supplier on a random/skip lot basis.\",\r\n    \"strength_statement\": \"Strength is not relevant to this ingredient.\",\r\n    \"origin\": \"Egypt\",\r\n    \"parts_used\": \"Leaves and leaf stems\",\r\n    \"specs\": {\r\n      \"mesh_size\": {\r\n        \"date_issued\": \"2024-01-22T00:00:00.000000Z\",\r\n        \"date_revised\": \"2024-01-22T00:00:00.000000Z\",\r\n        \"file_pointer\": \"\",\r\n        \"id_code\": \"\",\r\n        \"locations\": {\r\n          \"primary\": \"in_house\",\r\n          \"in_house\": true,\r\n          \"third_party_lab\": true,\r\n          \"supplier\": true\r\n        },\r\n        \"required_spec\": false,\r\n        \"revision_number\": 0,\r\n        \"statement\": \"\",\r\n        \"test_name\": \"Mesh Size\",\r\n        \"tests\": []\r\n      },\r\n      \"ftir\": {\r\n        \"date_issued\": \"\",\r\n        \"date_revised\": \"\",\r\n        \"file_pointer\": \"\",\r\n        \"locations\": {\r\n          \"in_house\": false,\r\n          \"primary\": \"supplier\",\r\n          \"supplier\": true,\r\n          \"third_party_lab\": true\r\n        },\r\n        \"required_spec\": false,\r\n        \"revision_number\": 0,\r\n        \"id_code\": \"\",\r\n        \"statement\": \"\",\r\n        \"test_name\": \"FTIR\",\r\n        \"methods\": [\r\n          \"FTIR\"\r\n        ],\r\n        \"tests\": []\r\n      },\r\n      \"gluten\": {\r\n        \"date_issued\": \"2024-01-22T00:00:00.000000Z\",\r\n        \"date_revised\": \"2024-01-23T00:00:00.000000Z\",\r\n        \"file_pointer\": \"\",\r\n        \"locations\": {\r\n          \"primary\": \"supplier\",\r\n          \"in_house\": false,\r\n          \"third_party_lab\": true,\r\n          \"supplier\": true\r\n        },\r\n        \"required_spec\": false,\r\n        \"revision_number\": 1,\r\n        \"id_code\": \"\",\r\n        \"statement\": \"The supplier\'s Certificate of Analysis states that it tests for gluten (for the protein Gliadin) using Allergen<ELISA>. This test produced a negative result even if it\'s not labelled as being gluten free.\",\r\n        \"test_name\": \"Gluten\",\r\n        \"tests\": []\r\n      },\r\n      \"heavy_metals\": {\r\n        \"date_issued\": \"2024-01-22T00:00:00.000000Z\",\r\n        \"date_revised\": \"2024-01-23T00:00:00.000000Z\",\r\n        \"file_pointer\": \"\",\r\n        \"locations\": {\r\n          \"primary\": \"supplier\",\r\n          \"in_house\": false,\r\n          \"third_party_lab\": true,\r\n          \"supplier\": true\r\n        },\r\n        \"required_spec\": true,\r\n        \"revision_number\": 1,\r\n        \"id_code\": \"\",\r\n        \"statement\": \"\",\r\n        \"test_name\": \"Heavy Metals\",\r\n        \"tests\": [\r\n          {\r\n            \"test_name\": \"Arsenic (As)\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"ICP-MS\",\r\n              \"USP <233>\"\r\n            ],\r\n            \"unit_of_measure\": \"ppm\",\r\n            \"count\": 3,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          },\r\n          {\r\n            \"test_name\": \"Cadmium (Cd)\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"ICP-MS\",\r\n              \"USP <233>\"\r\n            ],\r\n            \"unit_of_measure\": \"ppm\",\r\n            \"count\": 1.0,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          },\r\n          {\r\n            \"test_name\": \"Lead (Pb)\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"ICP-MS\",\r\n              \"USP <233>\"\r\n            ],\r\n            \"unit_of_measure\": \"ppm\",\r\n            \"count\": 1.0,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          },\r\n          {\r\n            \"test_name\": \"Mercury (Hg)\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"ICP-MS\",\r\n              \"USP <233>\"\r\n            ],\r\n            \"unit_of_measure\": \"ppm\",\r\n            \"count\": 1.0,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          },\r\n          {\r\n            \"test_name\": \"Total Heavy Metals\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"ICP-MS\",\r\n              \"USP <233>\"\r\n            ],\r\n            \"unit_of_measure\": \"\",\r\n            \"count\": 10,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          }\r\n        ]\r\n      },\r\n      \"hplc\": {\r\n        \"date_issued\": \"\",\r\n        \"date_revised\": \"\",\r\n        \"file_pointer\": \"\",\r\n        \"locations\": {\r\n          \"in_house\": false,\r\n          \"primary\": \"supplier\",\r\n          \"supplier\": true,\r\n          \"third_party_lab\": true\r\n        },\r\n        \"required_spec\": false,\r\n        \"revision_number\": 0,\r\n        \"id_code\": \"\",\r\n        \"statement\": \"\",\r\n        \"test_name\": \"HPLC\",\r\n        \"tests\": []\r\n      },\r\n      \"hptlc\": {\r\n        \"date_issued\": \"2024-01-22T00:00:00.000000Z\",\r\n        \"date_revised\": \"2024-01-22T00:00:00.000000Z\",\r\n        \"file_pointer\": \"\",\r\n        \"locations\": {\r\n          \"primary\": \"supplier\",\r\n          \"in_house\": false,\r\n          \"third_party_lab\": true,\r\n          \"supplier\": true\r\n        },\r\n        \"required_spec\": false,\r\n        \"revision_number\": 0,\r\n        \"id_code\": \"\",\r\n        \"statement\": \"\",\r\n        \"test_name\": \"HPTLC\",\r\n        \"tests\": []\r\n      },\r\n      \"microbiological\": {\r\n        \"date_issued\": \"2024-01-22T00:00:00.000000Z\",\r\n        \"date_revised\": \"2024-01-23T00:00:00.000000Z\",\r\n        \"file_pointer\": \"\",\r\n        \"locations\": {\r\n          \"primary\": \"supplier\",\r\n          \"in_house\": false,\r\n          \"third_party_lab\": true,\r\n          \"supplier\": true\r\n        },\r\n        \"required_spec\": true,\r\n        \"revision_number\": 1,\r\n        \"id_code\": \"\",\r\n        \"statement\": \"\",\r\n        \"test_name\": \"Microbiological\",\r\n        \"tests\": [\r\n          {\r\n            \"test_name\": \"Aerobic Plate Count\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"USP <2021>\"\r\n            ],\r\n            \"unit_of_measure\": \"cfu/g\",\r\n            \"count\": 30000000,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          },\r\n          {\r\n            \"test_name\": \"Coliforms Count\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"AOAC 991.14\"\r\n            ],\r\n            \"unit_of_measure\": \"cfu/g\",\r\n            \"count\": 10000,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          },\r\n          {\r\n            \"test_name\": \"Escherichia Coli Count (E.Coli)\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"USP <2022>\"\r\n            ],\r\n            \"unit_of_measure\": \"cfu/g\",\r\n            \"count\": 10,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          },\r\n          {\r\n            \"test_name\": \"Moisture/Loss on Drying\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": false,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"AOAC 966.02\",\r\n              \"LOD (Loss on Drying)\"\r\n            ],\r\n            \"unit_of_measure\": \"%\",\r\n            \"count\": 8.0,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          },\r\n          {\r\n            \"test_name\": \"Mold Count\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"USP <2021>\"\r\n            ],\r\n            \"unit_of_measure\": \"cfu/g\",\r\n            \"count\": 25000,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          },\r\n          {\r\n            \"test_name\": \"Salmonella Count\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"USP <2022>\",\r\n              \"AOAC 989.13\"\r\n            ],\r\n            \"unit_of_measure\": \"cfu/g\",\r\n            \"count\": 0,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          },\r\n          {\r\n            \"test_name\": \"Staphylococcus Count (Staph)\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"USP <2022>\"\r\n            ],\r\n            \"unit_of_measure\": \"cfu/g\",\r\n            \"count\": 0,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          },\r\n          {\r\n            \"test_name\": \"Total Plate Count\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"USP <2021>\"\r\n            ],\r\n            \"unit_of_measure\": \"cfu/g\",\r\n            \"count\": 30000000,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          },\r\n          {\r\n            \"test_name\": \"Yeast Count\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"USP <2021>\"\r\n            ],\r\n            \"unit_of_measure\": \"cfu/g\",\r\n            \"count\": 25000,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"\",\r\n            \"visual\": \"\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"\",\r\n            \"date_revised\": \"\"\r\n          }\r\n        ]\r\n      },\r\n      \"microscopic\": {\r\n        \"date_issued\": \"\",\r\n        \"date_revised\": \"\",\r\n        \"file_pointer\": \"\",\r\n        \"locations\": {\r\n          \"in_house\": true,\r\n          \"primary\": \"in_house\",\r\n          \"supplier\": true,\r\n          \"third_party_lab\": false\r\n        },\r\n        \"required_spec\": true,\r\n        \"revision_number\": 0,\r\n        \"id_code\": \"\",\r\n        \"statement\": \"\",\r\n        \"test_name\": \"Microscopic\",\r\n        \"tests\": []\r\n      },\r\n      \"nutritional_facts\": {\r\n        \"date_issued\": \"2024-01-22T00:00:00.000000Z\",\r\n        \"date_revised\": \"2024-01-22T00:00:00.000000Z\",\r\n        \"file_pointer\": \"\",\r\n        \"locations\": {\r\n          \"primary\": \"third_party_lab\",\r\n          \"in_house\": false,\r\n          \"third_party_lab\": true,\r\n          \"supplier\": true\r\n        },\r\n        \"required_spec\": false,\r\n        \"revision_number\": 0,\r\n        \"id_code\": \"\",\r\n        \"statement\": \"\",\r\n        \"test_name\": \"Nutritional Assay\",\r\n        \"tests\": []\r\n      },\r\n      \"organoleptic\": {\r\n        \"date_issued\": \"2024-01-22T00:00:00.000000Z\",\r\n        \"date_revised\": \"2024-01-22T00:00:00.000000Z\",\r\n        \"file_pointer\": \"\",\r\n        \"locations\": {\r\n          \"primary\": \"in_house\",\r\n          \"in_house\": true,\r\n          \"third_party_lab\": false,\r\n          \"supplier\": true\r\n        },\r\n        \"required_spec\": true,\r\n        \"revision_number\": 1,\r\n        \"id_code\": \"\",\r\n        \"test_name\": \"Organoleptic\",\r\n        \"tests\": [\r\n          {\r\n            \"test_name\": \"Organoleptic\",\r\n            \"statement\": \"\",\r\n            \"magnification\": \"\",\r\n            \"required_spec\": true,\r\n            \"method\": \"\",\r\n            \"methods\": [\r\n              \"SOP QA 04.02\"\r\n            ],\r\n            \"unit_of_measure\": \"cfu/g\",\r\n            \"count\": 0,\r\n            \"inequality\": \"<\",\r\n            \"sources\": [],\r\n            \"odor\": \"Grassy\",\r\n            \"taste_dissolved\": \"\",\r\n            \"taste_dry\": \"Grassy\",\r\n            \"visual\": \"Grassy\",\r\n            \"id_code\": \"\",\r\n            \"file_pointer\": \"\",\r\n            \"file_preview_pointer\": \"\",\r\n            \"date_issued\": \"2024-01-22T00:00:00.000000Z\",\r\n            \"date_revised\": \"2024-01-22T00:00:00.000000Z\"\r\n          }\r\n        ]\r\n      },\r\n      \"example_cofas\": {\r\n        \"date_issued\": \"\",\r\n        \"date_revised\": \"\",\r\n        \"file_pointer\": \"\",\r\n        \"locations\": {\r\n          \"in_house\": true,\r\n          \"primary\": \"in_house\",\r\n          \"supplier\": true,\r\n          \"third_party_lab\": false\r\n        },\r\n        \"required_spec\": true,\r\n        \"revision_number\": 0,\r\n        \"id_code\": \"\",\r\n        \"test_name\": \"Reference CofA\'s\",\r\n        \"tests\": []\r\n      },\r\n      \"pesticides\": {\r\n        \"date_issued\": \"2024-01-22T00:00:00.000000Z\",\r\n        \"date_revised\": \"2024-01-23T00:00:00.000000Z\",\r\n        \"file_pointer\": \"\",\r\n        \"locations\": {\r\n          \"primary\": \"supplier\",\r\n          \"in_house\": false,\r\n          \"third_party_lab\": true,\r\n          \"supplier\": true\r\n        },\r\n        \"required_spec\": false,\r\n        \"revision_number\": 1,\r\n        \"id_code\": \"\",\r\n        \"statement\": \"Since this is a certified organic product it\'s highly unlikely that pesticides would be present.\",\r\n        \"test_name\": \"Pesticides\",\r\n        \"tests\": []\r\n      },\r\n      \"residual_solvents\": {\r\n        \"date_issued\": \"2024-06-04T00:00:00.000000Z\",\r\n        \"date_revised\": \"2024-06-04T00:00:00.000000Z\",\r\n        \"file_pointer\": \"\",\r\n        \"locations\": {\r\n          \"primary\": \"supplier\",\r\n          \"in_house\": false,\r\n          \"third_party_lab\": true,\r\n          \"supplier\": true\r\n        },\r\n        \"required_spec\": false,\r\n        \"revision_number\": 0,\r\n        \"id_code\": \"\",\r\n        \"statement\": \"\",\r\n        \"test_name\": \"Residual Solvents\",\r\n        \"tests\": []\r\n      }\r\n    }\r\n  }\r\n}',0,0,0,0,1,0,1,1),(38,38,'Mental Mushroom',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(39,38,'Mental Mushroom',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(40,38,'Large Moringa',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(41,38,'Small Moringa',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(42,38,'Moringa Capsules',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(43,38,'Purple Sea Moss',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(44,38,'Raw Sea Moss',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(45,38,'Small Spirulina',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(46,38,'Large Spirulina',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(47,38,'Wheatgrass Juice',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(48,46,'Tranont',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(49,39,'Age Free',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(50,39,'Age Free',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(51,39,'Charconite',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(52,39,'Free Colon',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(53,39,'Free Colon',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(54,39,'Free Liver',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(55,39,'Free Liver',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(56,39,'Green Formula',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(57,39,'Green Pro C',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(58,39,'Happy Time',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(59,39,'Happy Time',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(60,39,'Heart Formula',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(61,39,'Heart Formula',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(62,39,'Kidney Formula',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(63,39,'Kidney Formula',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(64,39,'Manforce',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(65,39,'Manforce',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(66,39,'Small Markus Sweet',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(67,39,'Large Markus Sweet',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(68,39,'Night Rebuild',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(69,39,'Night Rebuild',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(70,39,'Parasite Free',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(71,39,'Power Formula',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(72,39,'Prebiotic Fiber',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(73,39,'Prostate Formula',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(74,39,'Prostate Formula',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(75,39,'Super Plant Protein',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(76,39,'Sweetened Super Plant Protein (Lupini)',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(77,39,'Trim Force',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(78,39,'Trim Force',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(79,39,'Unsweetened Green Formula (No Peppermint)',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(80,39,'Unsweetened Green Formula (With Peppermint)',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(81,39,'Unsweetened Super Plant Protein (Lupini)',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(82,39,'Unsweetened Super Plant Protein',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(83,39,'Vitamin C',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(84,45,'Aloe Path V15',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(85,45,'Aloe Path V17',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(86,45,'Biome Defense V77',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(87,45,'Biome Defense V79',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(88,45,'Bladder Builder (Vitamin E)',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(89,45,'Bladder Builder (Flow Agent)',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(90,45,'Bladder Rest V',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(91,45,'Bladder Smart V1',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(92,45,'CystoMend V13 (Flow Agent)',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(93,45,'CystoMend V9',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(94,45,'CystoMend V9 (Flow Agent)',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(95,45,'D-Mannose',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(96,45,'L. Flora v3',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(97,45,'PEAORA (Flow Agent)',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(98,45,'Peaora Omega 3',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(99,45,'Prevent Capsules',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(100,45,'Prevent Capsules (Flow Agent)',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(101,45,'Prostatitis V151',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(102,45,'Prostatitis V155',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(103,45,'Prostatitis V159',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(104,45,'Tru Test V1',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(105,45,'UroProstatitis V173',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(106,40,'Buddy Guard',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(107,41,'Prescript Assist 60ct (Lite)',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(108,41,'Prescript Assist 60ct (Advanced)',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(109,41,'Prescript Assist 60ct',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(110,41,'Prescript Assist 90ct',0,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(111,41,'Prescript Assist 90ct (Advanced)',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(112,41,'Prescript Assist 60ct (Pea Protein)',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(113,41,'Tas Alpha',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(114,42,'Large Inca Gold Maca',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(115,42,'Small Inca Gold Maca',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(116,42,'Large Inca Gold Maca',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(117,42,'Small Inca Gold Maca',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(118,44,'21ct Whole Produce Veggies',1,'2023-03-06 00:00:00',NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(119,41,'Prescript Assist Advanced wPea Protein 90ct',1,'2023-03-07 00:00:00',NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(120,36,'Barley Juice Powder Holistic Life',1,'2023-03-07 00:00:00',NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(121,38,'1lb Moringa Pouch',1,'2023-03-24 00:00:00',NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(122,38,'Red Maca',1,'2023-04-03 00:00:00',NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(123,38,'2oz Blackseed Oil',1,'2023-04-04 00:00:00',NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(124,44,'21ct Whole Produce Fruits',1,'2023-03-06 00:00:00',NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1),(125,38,'Blackseed Oil',1,NULL,NULL,NULL,'','',NULL,NULL,0,0,0,0,0,0,0,0,NULL,0,0,0,0,1,1,1,1);
/*!40000 ALTER TABLE `Product_Master` ENABLE KEYS */;
UNLOCK TABLES;

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

-- Dump completed on 2024-06-21 16:26:32
