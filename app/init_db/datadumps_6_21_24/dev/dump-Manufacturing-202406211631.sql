-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 192.168.1.136    Database: Manufacturing
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
-- Table structure for table `Equipment`
--

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
  PRIMARY KEY (`equipment_id`),
  KEY `process_id` (`process_id`),
  CONSTRAINT `Equipment_ibfk_1` FOREIGN KEY (`process_id`) REFERENCES `Processes` (`process_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Equipment`
--

LOCK TABLES `Equipment` WRITE;
/*!40000 ALTER TABLE `Equipment` DISABLE KEYS */;
INSERT INTO `Equipment` VALUES (1,7,'Serial no.','Working_Order','2024-06-10 15:47:03',NULL,NULL);
/*!40000 ALTER TABLE `Equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Processes`
--

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
  PRIMARY KEY (`process_id`),
  CONSTRAINT `Processes_CHECK` CHECK (json_valid(`bpr_data_template`))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Processes`
--

LOCK TABLES `Processes` WRITE;
/*!40000 ALTER TABLE `Processes` DISABLE KEYS */;
INSERT INTO `Processes` VALUES (1,'Batching','SOP PRO ##.##','2024-05-20 14:21:16','2024-06-10 14:29:00',NULL,NULL,NULL,NULL,NULL),(2,'Screening','SOP PRO ##.##','2024-05-20 14:21:16','2024-06-10 14:29:00',NULL,NULL,NULL,NULL,NULL),(3,'Grinding','SOP PRO ##.##','2024-05-20 14:21:16','2024-06-10 14:29:00',NULL,NULL,NULL,NULL,NULL),(4,'Blending','SOP PRO ##.##','2024-05-20 14:21:16','2024-06-10 14:29:00',NULL,NULL,NULL,NULL,NULL),(5,'Powder Fill','SOP PRO ##.##','2024-05-20 14:21:16','2024-06-10 14:29:00',NULL,NULL,NULL,NULL,NULL),(6,'Labeling','SOP PRO ##.##','2024-05-20 14:21:16','2024-06-10 14:29:00',NULL,NULL,NULL,NULL,NULL),(7,'Capsulation','SOP PRO ##.##','2024-05-20 14:21:16','2024-06-10 21:12:16',NULL,1,2,NULL,NULL),(8,'Polishing','SOP PRO ##.##','2024-05-20 14:21:16','2024-06-10 14:29:00',NULL,NULL,NULL,NULL,NULL),(9,'Sorting','SOP PRO ##.##','2024-05-20 14:21:16','2024-06-10 14:29:00',NULL,NULL,NULL,NULL,NULL),(10,'Capsule Fill','SOP PRO ##.##','2024-05-20 14:21:16','2024-06-10 14:29:00',NULL,NULL,NULL,NULL,NULL),(11,'Palletize','SOP PRO ##.##','2024-05-20 14:21:16','2024-06-10 14:29:00',NULL,NULL,NULL,NULL,NULL),(12,'REWORK','SOP PRO ##.##','2024-06-06 17:51:45','2024-06-10 14:29:00',NULL,NULL,NULL,NULL,NULL);
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

-- Dump completed on 2024-06-21 16:31:06
