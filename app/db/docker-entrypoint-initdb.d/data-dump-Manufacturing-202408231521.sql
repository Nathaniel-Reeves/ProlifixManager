-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 192.168.1.133    Database: Manufacturing
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
-- Current Database: `Manufacturing`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Manufacturing` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `Manufacturing`;

--
-- Table structure for table `Equipment`
--

DROP TABLE IF EXISTS `Equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Equipment` (
  `equipment_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `process_id` int(10) unsigned DEFAULT NULL,
  `equipment_sn` varchar(50) DEFAULT NULL,
  `status` enum('Working_Order','Broken','Removed') DEFAULT NULL,
  `timestamp_entered` timestamp(6) NOT NULL DEFAULT current_timestamp(6),
  `timestamp_modified` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `equipment_history` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`equipment_history`)),
  `equipment_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`equipment_id`),
  KEY `process_id` (`process_id`),
  CONSTRAINT `Equipment_ibfk_1` FOREIGN KEY (`process_id`) REFERENCES `Processes` (`process_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Equipment`
--

LOCK TABLES `Equipment` WRITE;
/*!40000 ALTER TABLE `Equipment` DISABLE KEYS */;
INSERT INTO `Equipment` VALUES (4,2,'LS48S88','Working_Order','2024-08-09 17:27:33.000000','2024-08-19 20:17:35','{}','Sweco Screener'),(5,3,NULL,'Working_Order','2024-08-09 17:27:33.000000','2024-08-19 20:17:35','{}','US Motors V Blender'),(6,NULL,NULL,'Working_Order','2024-08-09 17:27:33.000000','2024-08-19 20:17:35','{}','Grinder'),(7,8,'25103','Working_Order','2024-08-09 17:27:33.000000','2024-08-19 20:17:35','{}','All-fill Powder Filler'),(8,8,'A-100323','Working_Order','2024-08-09 17:27:33.000000','2024-08-19 20:17:35','{}','AMS Powder Filler'),(9,8,'16172','Working_Order','2024-08-09 17:27:33.000000','2024-08-19 20:17:35','{}','Bartelt Powder Filler'),(10,4,'YY0254-1997','Working_Order','2024-08-09 17:27:33.000000','2024-08-19 20:17:35','{}','Automatic ZJT900 Encapsulator'),(11,4,'07467','Working_Order','2024-08-09 17:27:33.000000','2024-08-12 21:44:21','{}','NJP1200 Encapsulator'),(12,5,'059','Working_Order','2024-08-09 17:27:33.000000','2024-08-12 21:44:21','{}','Semi Auto ZJTM Encapsulator'),(13,6,'0995-0-085','Working_Order','2024-08-09 17:27:33.000000','2024-08-12 21:44:21','{}','CPT Capsule Polisher'),(14,10,'','Working_Order','2024-08-09 17:27:33.000000','2024-08-12 21:44:21','{}','Ferguson Slat Capsule Counter'),(15,18,'129187F02','Working_Order','2024-08-09 17:27:33.000000','2024-08-12 21:44:21','{}','Bench Capsule Counter'),(16,12,'','Working_Order','2024-08-09 17:27:33.000000','2024-08-12 21:44:21','{}','Auto Mate Induction Lid Sealer'),(17,12,'61509-3','Working_Order','2024-08-09 17:27:33.000000','2024-08-12 21:44:21','{}','Pillar Tech Induction Lid Sealer'),(18,13,'CE-3000-HVE','Working_Order','2024-08-09 17:27:33.000000','2024-08-12 21:44:21','{}','Cleveland Bag Sealer '),(19,11,'A18404','Working_Order','2024-08-09 17:27:33.000000','2024-08-12 21:44:21','{}','Preferred Packaging Shrink Band Heat Tunnel'),(20,11,'EZ-24-BR','Working_Order','2024-08-09 17:27:34.000000','2024-08-12 21:44:21','{}','Axon Shrink Band Heat Tunnel'),(21,14,'9902163','Working_Order','2024-08-09 17:27:34.000000','2024-08-12 21:44:21','{}','CVC Labeler');
/*!40000 ALTER TABLE `Equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Processes`
--

DROP TABLE IF EXISTS `Processes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Processes` (
  `process_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `process_name` varchar(100) NOT NULL,
  `process_sop` varchar(30) DEFAULT NULL,
  `timestamp_entered` timestamp NOT NULL DEFAULT current_timestamp(),
  `timestamp_modified` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `rework_process` tinyint(1) DEFAULT NULL,
  `min_personnel` smallint(6) DEFAULT NULL,
  `max_personnel` smallint(6) DEFAULT NULL,
  `bpr_page_template` varchar(500) DEFAULT NULL,
  `bpr_data_template` longtext DEFAULT NULL,
  `requires_product_variant` tinyint(1) NOT NULL DEFAULT 0,
  `requires_components` tinyint(1) NOT NULL DEFAULT 0,
  `requires_box_specs` tinyint(1) NOT NULL DEFAULT 0,
  `top_handle` tinyint(1) NOT NULL DEFAULT 1,
  `bottom_handle` tinyint(1) NOT NULL DEFAULT 1,
  `left_handle` tinyint(1) NOT NULL DEFAULT 0,
  `right_handle` tinyint(1) NOT NULL DEFAULT 0,
  `ave_percent_loss` double DEFAULT NULL,
  `setup_time` double DEFAULT NULL,
  `setup_time_units` enum('Seconds','Minutes','Hours','Days') DEFAULT NULL,
  `setup_num_employees` tinyint(3) unsigned DEFAULT NULL,
  `cleaning_time` double DEFAULT NULL,
  `cleaning_time_units` enum('Seconds','Minutes','Hours','Days') DEFAULT NULL,
  `cleaning_num_employees` tinyint(3) unsigned DEFAULT NULL,
  `process_sop_link` varchar(500) DEFAULT NULL,
  `equipment_specific` tinyint(1) DEFAULT 0,
  `product_variant_type` enum('powder','liquid','capsule') DEFAULT NULL,
  `component_filters` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `requires_samples` tinyint(1) NOT NULL DEFAULT 0,
  `requires_retention` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`process_id`),
  CONSTRAINT `Processes_CHECK` CHECK (json_valid(`bpr_data_template`))
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Processes`
--

LOCK TABLES `Processes` WRITE;
/*!40000 ALTER TABLE `Processes` DISABLE KEYS */;
INSERT INTO `Processes` VALUES (1,'Batching','PRD 02.01','2024-08-08 21:59:07','2024-08-12 19:38:56.000000',0,2,2,NULL,NULL,0,0,0,0,1,0,0,0.5,0,'Seconds',0,1,'Hours',2,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.f0ysalwxc71k',0,NULL,NULL,0,0),(2,'Screening','PRD 02.02','2024-08-08 21:59:07','2024-08-12 19:38:56.000000',0,1,2,NULL,NULL,0,0,0,1,1,0,0,1,1,'Hours',1,2,'Hours',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.pbzs23bje2dq',0,NULL,NULL,0,0),(3,'Blending - VBlender','PRD 02.03','2024-08-08 21:59:07','2024-08-12 20:58:23.000000',0,1,2,NULL,NULL,0,0,0,1,1,0,0,0.5,30,'Minutes',1,3,'Hours',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.b8mzxlflrmt6',1,NULL,NULL,1,0),(4,'Auto Encapsulation','PRD 02.04','2024-08-08 21:59:07','2024-08-12 20:16:38.000000',0,1,2,NULL,NULL,1,1,0,1,1,0,0,2,8,'Hours',1,8,'Hours',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.gv8u0tjesfza',1,'capsule','[\"capsule\"]',0,0),(5,'Semi Auto Encapsulation','PRD 02.04','2024-08-08 21:59:07','2024-08-12 20:16:38.000000',0,1,2,NULL,NULL,1,1,0,1,1,0,0,2,4,'Hours',1,4,'Hours',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.gv8u0tjesfza',1,'capsule','[\"capsule\"]',1,0),(6,'Polishing','PRD 02.04','2024-08-08 21:59:07','2024-08-12 19:38:56.000000',0,1,2,NULL,NULL,1,0,0,1,1,0,0,0.5,30,'Minutes',1,1,'Hours',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.gv8u0tjesfza',0,'capsule',NULL,0,0),(7,'Sorting','PRD 02.04','2024-08-08 21:59:07','2024-08-12 19:38:56.000000',0,1,6,NULL,NULL,1,0,0,1,1,0,0,1,10,'Minutes',1,10,'Minutes',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.gv8u0tjesfza',0,'capsule',NULL,0,0),(8,'Powder Fill','PRD 02.05','2024-08-08 21:59:07','2024-08-12 20:16:38.000000',0,2,5,NULL,NULL,1,1,0,1,1,0,0,0.5,1,'Hours',1,1,'Hours',2,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.pa85mzo5drwu',0,'powder','[\"pouch\",\"container\",\"scoop\",\"misc\",\"desiccant\"]',0,0),(9,'Auto Liquid Fill','PRD 02.06','2024-08-08 21:59:07','2024-08-12 20:16:38.000000',0,2,4,NULL,NULL,1,1,0,1,1,0,0,0.2,1,'Hours',2,1,'Hours',2,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.72h2uiic83ez',1,'liquid','[\"container\",\"misc\",\"lid\"]',0,0),(10,'Slat Counter Capsule Fill','PRD 02.07','2024-08-08 21:59:07','2024-08-12 20:16:38.000000',0,2,4,NULL,NULL,1,1,0,1,1,0,0,0.5,2,'Hours',1,2,'Hours',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.lh51oqj3aov3',1,'capsule','[\"container\",\"scoop\",\"misc\",\"desiccant\"]',0,0),(11,'Heat Sealing','PRD 02.09','2024-08-08 21:59:07','2024-08-12 20:16:38.000000',0,1,2,NULL,NULL,1,1,0,1,1,0,0,0,1,'Hours',1,20,'Minutes',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.hjn76h4u2psn',0,NULL,'[\"lid\",\"shrink_band\"]',0,0),(12,'Induction Sealing','PRD 02.08','2024-08-08 21:59:07','2024-08-12 20:16:38.000000',0,1,2,NULL,NULL,1,1,0,1,1,0,0,0,20,'Minutes',1,20,'Minutes',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.i0ats83bpxbc',0,NULL,'[\"lid\"]',0,0),(13,'Bag Seal','PRD 02.11','2024-08-08 21:59:07','2024-08-12 20:16:38.000000',0,1,2,NULL,NULL,1,0,0,1,1,0,0,0,20,'Minutes',1,10,'Minutes',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.m1nffwofnjjb',0,'powder',NULL,0,1),(14,'Labeling','PRD 02.10','2024-08-08 21:59:07','2024-08-12 20:07:13.000000',0,1,1,NULL,NULL,1,1,0,1,1,0,0,0,1,'Hours',1,20,'Minutes',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.2966z5w9wku6',0,NULL,'[\"label\"]',0,0),(15,'Packaging','PRD 02.12','2024-08-08 21:59:07','2024-08-12 20:16:38.000000',0,1,6,NULL,NULL,1,1,0,1,1,0,0,0,1,'Hours',1,20,'Minutes',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.ria01jdewkvc',0,NULL,'[\"packaging_material\", \"carton\",\"label\",\"misc\"]',0,1),(16,'Boxing & Palletizing','PRD 02.12','2024-08-08 21:59:07','2024-08-12 20:16:38.000000',0,1,5,NULL,NULL,1,1,1,1,0,0,0,0,1,'Hours',1,20,'Minutes',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.ria01jdewkvc',0,NULL,'[\"box\"]',0,1),(17,'Semi Auto Liquid Fill','PRD 02.06','2024-08-09 17:09:17','2024-08-12 20:16:38.000000',0,2,4,NULL,NULL,1,1,0,1,1,0,0,0.2,30,'Minutes',1,1,'Hours',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.72h2uiic83ez',1,'liquid','[\"container\",\"misc\",\"lid\"]',0,0),(18,'Bench Counter Capsule Fill','PRD 02.07','2024-08-09 17:09:17','2024-08-12 20:16:38.000000',0,2,4,NULL,NULL,1,1,0,1,1,0,0,0.5,30,'Minutes',1,30,'Minutes',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.lh51oqj3aov3',1,'capsule','[\"container\",\"scoop\",\"misc\",\"desiccant\"]',1,0),(19,'Blending - Mixer','PRD 02.03','2024-08-08 21:59:07','2024-08-12 20:16:38.000000',0,1,2,NULL,NULL,0,0,0,1,1,0,0,0.5,30,'Minutes',1,3,'Hours',1,'https://docs.google.com/document/d/1sQ9IwEle2yAmMVUvp-7KWOXpxZv999luaoTWIxPT1bA/edit#bookmark=id.b8mzxlflrmt6',1,NULL,NULL,1,0);
/*!40000 ALTER TABLE `Processes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'Manufacturing'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-23 15:21:52
