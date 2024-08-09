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
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `date_modified` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  `equipment_history` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`equipment_history`)),
  `equipment_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`equipment_id`),
  KEY `process_id` (`process_id`),
  CONSTRAINT `Equipment_ibfk_1` FOREIGN KEY (`process_id`) REFERENCES `Processes` (`process_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `date_modified` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
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
  PRIMARY KEY (`process_id`),
  CONSTRAINT `Processes_CHECK` CHECK (json_valid(`bpr_data_template`))
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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

-- Dump completed on 2024-08-09 16:40:12
