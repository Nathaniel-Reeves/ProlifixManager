-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 192.168.1.133    Database: Orders
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
-- Current Database: `Orders`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Orders` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `Orders`;

--
-- Table structure for table `Lot_Numbers`
--

DROP TABLE IF EXISTS `Lot_Numbers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Lot_Numbers` (
  `prefix` varchar(15) NOT NULL DEFAULT '',
  `year` tinyint(4) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `sec_number` smallint(6) NOT NULL,
  `suffix` varchar(15) NOT NULL DEFAULT '',
  `product_id` int(10) unsigned NOT NULL,
  `prolifix_lot_number` varchar(20) DEFAULT concat(`prefix`,lpad(`year`,2,'0'),lpad(`month`,2,'0'),lpad(`sec_number`,3,'0'),`suffix`),
  `so_detail_id` int(10) unsigned DEFAULT NULL,
  `target_unit_yield` int(11) DEFAULT NULL,
  `actual_unit_yield` int(11) DEFAULT NULL,
  `retentions` int(11) DEFAULT NULL,
  `total_shippable_product` int(11) DEFAULT NULL,
  `doc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT concat('{"_id":"',`prolifix_lot_number`,'"}') CHECK (json_valid(`doc`)),
  `batch_printed` tinyint(1) DEFAULT NULL,
  `bpr_printed` tinyint(1) DEFAULT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `exp_date` date DEFAULT NULL,
  `exp_type` enum('Best By','Exp') NOT NULL,
  PRIMARY KEY (`prefix`,`year`,`month`,`sec_number`,`suffix`),
  KEY `so_detail_id` (`so_detail_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `Lot_Numbers_ibfk_1` FOREIGN KEY (`so_detail_id`) REFERENCES `Sale_Order_Detail` (`so_detail_id`),
  CONSTRAINT `Lot_Numbers_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Lot_Numbers`
--

LOCK TABLES `Lot_Numbers` WRITE;
/*!40000 ALTER TABLE `Lot_Numbers` DISABLE KEYS */;
/*!40000 ALTER TABLE `Lot_Numbers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Purchase_Order_Detail`
--

DROP TABLE IF EXISTS `Purchase_Order_Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Purchase_Order_Detail` (
  `po_detail_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `prefix` varchar(10) NOT NULL DEFAULT '',
  `year` tinyint(4) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `sec_number` smallint(6) NOT NULL,
  `suffix` varchar(10) NOT NULL DEFAULT '',
  `component_id` int(10) unsigned NOT NULL,
  `unit_order_qty` int(11) DEFAULT NULL,
  `kilos_order_qty` decimal(16,4) DEFAULT NULL,
  `special_instructions` varchar(2000) DEFAULT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `bid_price_per_unit` decimal(16,4) DEFAULT NULL,
  `bid_price_per_kilo` decimal(16,4) DEFAULT NULL,
  `doc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`doc`)),
  PRIMARY KEY (`po_detail_id`),
  KEY `prefix` (`prefix`,`year`,`month`,`sec_number`,`suffix`),
  KEY `component_id` (`component_id`),
  CONSTRAINT `Purchase_Order_Detail_ibfk_1` FOREIGN KEY (`prefix`, `year`, `month`, `sec_number`, `suffix`) REFERENCES `Purchase_Orders` (`prefix`, `year`, `month`, `sec_number`, `suffix`),
  CONSTRAINT `Purchase_Order_Detail_ibfk_2` FOREIGN KEY (`component_id`) REFERENCES `Inventory`.`Components` (`component_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Purchase_Order_Detail`
--

LOCK TABLES `Purchase_Order_Detail` WRITE;
/*!40000 ALTER TABLE `Purchase_Order_Detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `Purchase_Order_Detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Purchase_Orders`
--

DROP TABLE IF EXISTS `Purchase_Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Purchase_Orders` (
  `prefix` varchar(10) NOT NULL DEFAULT '',
  `year` tinyint(4) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `sec_number` smallint(6) NOT NULL,
  `suffix` varchar(10) NOT NULL DEFAULT '',
  `organization_id` int(10) unsigned DEFAULT NULL,
  `supplier_so_num` varchar(30) DEFAULT NULL,
  `order_date` date DEFAULT NULL,
  `eta_date` date DEFAULT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `doc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT concat('{"_id":"',`prefix`,`year`,`month`,`sec_number`,`suffix`,'","files":[]}') CHECK (json_valid(`doc`)),
  PRIMARY KEY (`prefix`,`year`,`month`,`sec_number`,`suffix`),
  KEY `organization_id` (`organization_id`),
  CONSTRAINT `Purchase_Orders_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations` (`organization_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Purchase_Orders`
--

LOCK TABLES `Purchase_Orders` WRITE;
/*!40000 ALTER TABLE `Purchase_Orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `Purchase_Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sale_Order_Detail`
--

DROP TABLE IF EXISTS `Sale_Order_Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Sale_Order_Detail` (
  `so_detail_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `prefix` varchar(10) NOT NULL DEFAULT '',
  `year` tinyint(4) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `sec_number` smallint(6) NOT NULL,
  `suffix` varchar(10) NOT NULL DEFAULT '',
  `product_id` int(10) unsigned NOT NULL,
  `unit_order_qty` int(11) DEFAULT NULL,
  `kilos_order_qty` decimal(16,4) DEFAULT NULL,
  `special_instructions` varchar(2000) DEFAULT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `bid_price_per_unit` decimal(16,4) DEFAULT NULL,
  `final_ship_date` date DEFAULT NULL,
  `doc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`doc`)),
  PRIMARY KEY (`so_detail_id`),
  KEY `product_id` (`product_id`),
  KEY `prefix` (`prefix`,`year`,`month`,`sec_number`,`suffix`),
  CONSTRAINT `Sale_Order_Detail_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Products`.`Product_Master` (`product_id`),
  CONSTRAINT `Sale_Order_Detail_ibfk_2` FOREIGN KEY (`prefix`, `year`, `month`, `sec_number`, `suffix`) REFERENCES `Sales_Orders` (`prefix`, `year`, `month`, `sec_number`, `suffix`)
) ENGINE=InnoDB AUTO_INCREMENT=186 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sale_Order_Detail`
--

LOCK TABLES `Sale_Order_Detail` WRITE;
/*!40000 ALTER TABLE `Sale_Order_Detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `Sale_Order_Detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sales_Orders`
--

DROP TABLE IF EXISTS `Sales_Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Sales_Orders` (
  `prefix` varchar(10) NOT NULL DEFAULT '',
  `year` tinyint(4) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `sec_number` smallint(6) NOT NULL,
  `suffix` varchar(10) NOT NULL DEFAULT '',
  `organization_id` int(10) unsigned NOT NULL,
  `client_po_num` varchar(30) DEFAULT NULL,
  `order_date` date DEFAULT NULL,
  `target_completion_date` date DEFAULT NULL,
  `completion_date` date DEFAULT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `doc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT concat('{"_id":"',`prefix`,`year`,`month`,`sec_number`,`suffix`,'","files":[]}') CHECK (json_valid(`doc`)),
  `billed_date` date DEFAULT NULL,
  `closed_date` date DEFAULT NULL,
  `down_payment_actual` double DEFAULT NULL,
  `theoretical_po_amount` double DEFAULT NULL,
  `total_paid` double DEFAULT NULL,
  PRIMARY KEY (`prefix`,`year`,`month`,`sec_number`,`suffix`),
  KEY `organization_id` (`organization_id`),
  CONSTRAINT `Sales_Orders_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `Organizations`.`Organizations` (`organization_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sales_Orders`
--

LOCK TABLES `Sales_Orders` WRITE;
/*!40000 ALTER TABLE `Sales_Orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `Sales_Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sales_Orders_Payments`
--

DROP TABLE IF EXISTS `Sales_Orders_Payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Sales_Orders_Payments` (
  `prefix` varchar(10) NOT NULL DEFAULT '',
  `year` tinyint(4) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `sec_number` smallint(6) NOT NULL,
  `suffix` varchar(10) NOT NULL DEFAULT '',
  `organization_id` int(11) DEFAULT NULL,
  `payment_amount` double DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `payment_type` enum('down_payment','other','final_payment') NOT NULL,
  `payment_notes` varchar(2500) DEFAULT NULL,
  `date_entered` timestamp NULL DEFAULT current_timestamp(),
  `doc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT concat('{"_id":"',`prefix`,`year`,`month`,`sec_number`,`suffix`,'","files":[]}') CHECK (json_valid(`doc`)),
  PRIMARY KEY (`prefix`,`year`,`month`,`sec_number`,`suffix`),
  CONSTRAINT `Sales_Orders_Payments_ibfk_1` FOREIGN KEY (`prefix`, `year`, `month`, `sec_number`, `suffix`) REFERENCES `Sales_Orders` (`prefix`, `year`, `month`, `sec_number`, `suffix`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sales_Orders_Payments`
--

LOCK TABLES `Sales_Orders_Payments` WRITE;
/*!40000 ALTER TABLE `Sales_Orders_Payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `Sales_Orders_Payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'Orders'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-19 12:12:42
