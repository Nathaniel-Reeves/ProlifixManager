-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 192.168.1.133    Database: Organizations
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
-- Current Database: `Organizations`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Organizations` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `Organizations`;

--
-- Table structure for table `Facilities`
--

DROP TABLE IF EXISTS `Facilities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Facilities` (
  `facility_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int(10) unsigned DEFAULT NULL,
  `building_name` varchar(500) DEFAULT NULL,
  `building_type` enum('Head_Office','Office','Distribution_Warehouse','Manufacturing_Facility','Storefront') NOT NULL,
  `street_1_number` int(11) DEFAULT NULL,
  `street_1_number_suffix` varchar(10) DEFAULT NULL,
  `street_1_name` varchar(500) DEFAULT NULL,
  `street_1_type` varchar(300) DEFAULT NULL,
  `street_1_direction` varchar(2) DEFAULT NULL,
  `street_2_number` int(11) DEFAULT NULL,
  `street_2_number_suffix` varchar(10) DEFAULT NULL,
  `street_2_name` varchar(500) DEFAULT NULL,
  `street_2_type` varchar(300) DEFAULT NULL,
  `street_2_direction` varchar(2) DEFAULT NULL,
  `address_type` varchar(300) DEFAULT NULL,
  `address_type_identifier` varchar(100) DEFAULT NULL,
  `local_municipality` varchar(500) DEFAULT NULL,
  `city_town` varchar(500) DEFAULT NULL,
  `governing_district` varchar(500) DEFAULT NULL,
  `postal_area` varchar(100) DEFAULT NULL,
  `country` varchar(500) DEFAULT NULL,
  `ship_time` int(11) DEFAULT NULL,
  `ship_time_units` enum('Unknown','Days','Weeks','Months') NOT NULL,
  `ship_time_in_days` int(11) DEFAULT NULL,
  `notes` varchar(2500) DEFAULT NULL,
  PRIMARY KEY (`facility_id`),
  KEY `organization_id` (`organization_id`),
  CONSTRAINT `Facilities_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `Organizations` (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Organization_Names`
--

DROP TABLE IF EXISTS `Organization_Names`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Organization_Names` (
  `name_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int(10) unsigned DEFAULT NULL,
  `organization_name` varchar(200) NOT NULL,
  `organization_initial` varchar(10) NOT NULL,
  `primary_name` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`name_id`),
  KEY `organization_id` (`organization_id`),
  KEY `organization_name` (`organization_name`),
  KEY `organization_initial` (`organization_initial`),
  CONSTRAINT `Organization_Names_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `Organizations` (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=263 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Organizations`
--

DROP TABLE IF EXISTS `Organizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Organizations` (
  `organization_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `date_entered` date DEFAULT NULL,
  `website_url` varchar(200) DEFAULT NULL,
  `vetted` tinyint(1) DEFAULT NULL,
  `date_vetted` date DEFAULT NULL,
  `risk_level` enum('UNKNOWN','No_Risk','Low_Risk','Medium_Risk','High_Risk') DEFAULT NULL,
  `supplier` tinyint(1) DEFAULT 0,
  `client` tinyint(1) DEFAULT 0,
  `lab` tinyint(1) DEFAULT 0,
  `courier` tinyint(1) DEFAULT 0,
  `other` tinyint(1) DEFAULT 0,
  `doc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`doc`)),
  `notes` varchar(2500) DEFAULT NULL,
  `primary_name_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=229 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `People`
--

DROP TABLE IF EXISTS `People`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `People` (
  `person_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int(10) unsigned DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `job_description` varchar(100) DEFAULT NULL,
  `department` varchar(500) DEFAULT NULL,
  `phone_number_primary` varchar(20) DEFAULT NULL,
  `phone_number_secondary` varchar(20) DEFAULT NULL,
  `email_address_primary` varchar(100) DEFAULT NULL,
  `email_address_secondary` varchar(100) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `is_employee` tinyint(1) DEFAULT NULL,
  `contract_date` date DEFAULT NULL,
  `termination_date` date DEFAULT NULL,
  `clock_number` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`person_id`),
  KEY `organization_id` (`organization_id`),
  CONSTRAINT `People_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `Organizations` (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `person_id` int(10) unsigned DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `encrypted_password` varchar(250) NOT NULL,
  `profile_picture` varchar(500) DEFAULT NULL,
  `color_theme` enum('Light','Dark') DEFAULT NULL,
  `doc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`doc`)),
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `org_and_people_detail`
--

DROP TABLE IF EXISTS `org_and_people_detail`;
/*!50001 DROP VIEW IF EXISTS `org_and_people_detail`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `org_and_people_detail` AS SELECT 
 1 AS `person_id`,
 1 AS `first_name`,
 1 AS `last_name`,
 1 AS `job_description`,
 1 AS `department`,
 1 AS `phone_number_primary`,
 1 AS `phone_number_secondary`,
 1 AS `email_address_primary`,
 1 AS `email_address_secondary`,
 1 AS `birthday`,
 1 AS `is_employee`,
 1 AS `contract_date`,
 1 AS `termination_date`,
 1 AS `clock_number`,
 1 AS `organization_id`,
 1 AS `date_entered`,
 1 AS `website_url`,
 1 AS `date_vetted`,
 1 AS `risk_level`,
 1 AS `supplier`,
 1 AS `client`,
 1 AS `lab`,
 1 AS `other`,
 1 AS `doc`,
 1 AS `notes`,
 1 AS `organization_name`,
 1 AS `organization_initial`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `org_primary`
--

DROP TABLE IF EXISTS `org_primary`;
/*!50001 DROP VIEW IF EXISTS `org_primary`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `org_primary` AS SELECT 
 1 AS `organization_id`,
 1 AS `date_entered`,
 1 AS `website_url`,
 1 AS `date_vetted`,
 1 AS `risk_level`,
 1 AS `supplier`,
 1 AS `client`,
 1 AS `lab`,
 1 AS `other`,
 1 AS `doc`,
 1 AS `notes`,
 1 AS `organization_name`,
 1 AS `organization_initial`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping routines for database 'Organizations'
--

--
-- Current Database: `Organizations`
--

USE `Organizations`;

--
-- Final view structure for view `org_and_people_detail`
--

/*!50001 DROP VIEW IF EXISTS `org_and_people_detail`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`client`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `org_and_people_detail` AS select `People`.`person_id` AS `person_id`,`People`.`first_name` AS `first_name`,`People`.`last_name` AS `last_name`,`People`.`job_description` AS `job_description`,`People`.`department` AS `department`,`People`.`phone_number_primary` AS `phone_number_primary`,`People`.`phone_number_secondary` AS `phone_number_secondary`,`People`.`email_address_primary` AS `email_address_primary`,`People`.`email_address_secondary` AS `email_address_secondary`,`People`.`birthday` AS `birthday`,`People`.`is_employee` AS `is_employee`,`People`.`contract_date` AS `contract_date`,`People`.`termination_date` AS `termination_date`,`People`.`clock_number` AS `clock_number`,`Organizations`.`organization_id` AS `organization_id`,`Organizations`.`date_entered` AS `date_entered`,`Organizations`.`website_url` AS `website_url`,`Organizations`.`date_vetted` AS `date_vetted`,`Organizations`.`risk_level` AS `risk_level`,`Organizations`.`supplier` AS `supplier`,`Organizations`.`client` AS `client`,`Organizations`.`lab` AS `lab`,`Organizations`.`other` AS `other`,`Organizations`.`doc` AS `doc`,`Organizations`.`notes` AS `notes`,`Organization_Names`.`organization_name` AS `organization_name`,`Organization_Names`.`organization_initial` AS `organization_initial` from ((`Organizations` left join `People` on(`Organizations`.`organization_id` = `People`.`organization_id`)) left join `Organization_Names` on(`Organizations`.`organization_id` = `Organization_Names`.`organization_id` and `Organization_Names`.`primary_name` = 1)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `org_primary`
--

/*!50001 DROP VIEW IF EXISTS `org_primary`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`client`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `org_primary` AS select `Organizations`.`organization_id` AS `organization_id`,`Organizations`.`date_entered` AS `date_entered`,`Organizations`.`website_url` AS `website_url`,`Organizations`.`date_vetted` AS `date_vetted`,`Organizations`.`risk_level` AS `risk_level`,`Organizations`.`supplier` AS `supplier`,`Organizations`.`client` AS `client`,`Organizations`.`lab` AS `lab`,`Organizations`.`other` AS `other`,`Organizations`.`doc` AS `doc`,`Organizations`.`notes` AS `notes`,`Organization_Names`.`organization_name` AS `organization_name`,`Organization_Names`.`organization_initial` AS `organization_initial` from (`Organizations` left join `Organization_Names` on(`Organizations`.`organization_id` = `Organization_Names`.`organization_id` and `Organization_Names`.`primary_name` = 1)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-13 11:25:41
