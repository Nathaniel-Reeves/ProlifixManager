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
-- Table structure for table `Facilities`
--

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
-- Dumping data for table `Facilities`
--

LOCK TABLES `Facilities` WRITE;
/*!40000 ALTER TABLE `Facilities` DISABLE KEYS */;
INSERT INTO `Facilities` VALUES (1,1,'Prolifix Nutrition HQ','Head_Office',696,NULL,NULL,'street','S',5300,NULL,NULL,'street','W','suite','1-5',NULL,'Hurricane','Utah','84737','United States of America',0,'Days',0,NULL);
/*!40000 ALTER TABLE `Facilities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Organization_Names`
--

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
-- Dumping data for table `Organization_Names`
--

LOCK TABLES `Organization_Names` WRITE;
/*!40000 ALTER TABLE `Organization_Names` DISABLE KEYS */;
INSERT INTO `Organization_Names` VALUES (1,1,'Prolifix Nutrition','PLX',1),(2,1,'Prolifix','PLX',0),(3,2,'Albion laboratories','ARL',1),(4,2,'Albion','ARL',0),(5,3,'Aloha Medicinals','AM',1),(6,4,'AuNutra Industries Inc.','ANI',1),(7,4,'AuNutra','ANI',0),(8,5,'Azure Standard','AS',1),(9,5,'Azure Market','AS',0),(10,5,'Azure','AS',0),(11,6,'Bio Kinetics Corporation','BK',1),(12,6,'Bio-Kinetics','BK',0),(13,7,'Bulk Supplements','BS',1),(14,8,'Cambridge Commodities','CC',1),(15,9,'Ecuadorian Rainforest','ER',1),(16,9,'Ecuadorian','ER',0),(17,10,'Daesang','D',1),(18,11,'High Quality Organics','HQO',1),(19,12,'Honeyville Inc.','H',1),(20,12,'Honeyville','H',0),(21,13,'Hunan Nutramax Inc','HN',1),(22,13,'Hunan Nutramax','HN',0),(23,13,'Nutramax','HN',0),(24,14,'Liberty Natural','LN',1),(25,15,'LiquaDry','LD',1),(26,16,'LOOV Organic','LOOV',1),(27,16,'LOOV','LOOV',0),(28,17,'Nature\'s Flavors','NF',1),(29,18,'Nature\'s Power Nutraceuticals Corp. dba NP Nutra','NPN',1),(30,18,'NP Nutra','NPN',0),(31,18,'Nutraceuticals','NPN',0),(32,19,'Nexira International S.A.S.','N',1),(33,20,'North American Reishi Ltd. DBA Nammex','NAR',1),(34,21,'Om Foods Inc (Essential Organics)','OF',1),(35,21,'Essential Organics','OF',0),(36,22,'Pacific Botanicals Holding LLC','PB',1),(37,22,'Pacific Botanicals','PB',0),(38,23,'Prescribed for Life','PFL',1),(39,23,'Prescribed 4 life','PFL',0),(40,24,'Pure Bulk','PB',1),(41,25,'Specialty Enzymes E&P','SE',1),(42,25,'Specialty E+P','SE',0),(43,26,'The Australian Superfood Co.','AS',1),(44,26,'Australian Superfood','AS',0),(45,27,'To Your Health Sprouted Flour Co.','TYH',1),(46,27,'To Your Health','TYH',0),(47,28,'Unichem Enterprises','UE',1),(48,28,'Unichem','UE',0),(49,29,'Whole Herb Company','WH',1),(50,29,'Whole Herb','WH',0),(51,30,'Zhejiang Biosan Biotech Co.,Ltd','ZBB',1),(52,30,'Biosan','ZBB',0),(53,31,'Healthway Biotech','HB',1),(54,31,'Healthway Bio','HB',0),(55,31,'Xi\'an Healthway Biotech','HB',0),(56,31,'Healthway','HB',0),(57,32,'Stryka','S',1),(58,33,'Consulting Management','CM',1),(59,34,'Enerex','E',1),(60,35,'Herbally Grounded','HG',1),(61,35,'Herb Garden','HG',0),(62,36,'Holistic Earth Supplements','HES',1),(63,36,'Holistic Earth','HES',0),(64,37,'Immune Solution','IS',1),(65,38,'Maju Superfoods','MAJU',1),(66,38,'Maju','MAJU',0),(67,39,'Markus Rothcranz','M',1),(68,39,'Markus','M',0),(69,40,'Makes3Organics','M3O',1),(70,40,'Petsmot','M3O',0),(71,41,'Revelation Health','RH',1),(72,41,'Safer Medical','RH',0),(73,42,'Vita-myr','V',1),(74,43,'KN Life-Biotics','KN',1),(75,43,'Life-Biotics','KN',0),(76,44,'Balance of Nature','BON',1),(77,45,'Natrual Approch Nutrition','NAN',1),(78,45,'NAN Health','NAN',0),(79,46,'Tranont','T',1),(80,46,'Mana Life','T',0),(81,47,'Bloomfield Roots','BR',1),(82,48,'AG Commodities','',1),(83,49,'AIDP','',1),(84,50,'Albion','',1),(85,51,'Alpha Naturals','',1),(86,52,'Altaiga','',1),(87,53,'Altalena','',1),(88,54,'American Botanicals','',1),(89,55,'American Lecithin Company','',1),(90,56,'Ameriherb','',1),(91,57,'Aminature','',1),(92,58,'Anchor','',1),(93,59,'Anhui Sealong Bio','',1),(94,60,'APP Global','',1),(95,61,'Aroma Depot','',1),(96,62,'Austrade','',1),(97,63,'Aviva','',1),(98,64,'Balchem','',1),(99,65,'Baobab Foods','',1),(100,66,'Baolingbao Bio Co Ltd','',1),(101,67,'Bio-Gen','',1),(102,68,'Bioresponse','',1),(103,69,'Black Earth','',1),(104,70,'Blue Mountain','',1),(105,71,'Box Nutra Maxsun Industries','',1),(106,72,'Bulk Foods','',1),(107,73,'Bulkeez','',1),(108,74,'CarGill','',1),(109,75,'Changsha HuaKang Bio','',1),(110,76,'CI Inc','',1),(111,77,'Cypress','',1),(112,78,'diatomaceousearth.com','',1),(113,79,'DNP International','',1),(114,80,'DolCas Biotech','',1),(115,81,'Dongguan','',1),(116,82,'Earthrise','',1),(117,83,'Elite Ingredients','',1),(118,84,'Flora Aromatics','',1),(119,85,'Fying','',1),(120,86,'GeroNova Innovations','',1),(121,87,'Ginco','',1),(122,88,'Glory Bee','',1),(123,89,'Gold Coast','',1),(124,90,'Gourmet Mushroom','',1),(125,91,'Green Source Organic','',1),(126,92,'Green Wave Ingredients','',1),(127,93,'Greenjeeva','',1),(128,94,'GTX Technologies','',1),(129,95,'Hand Ground','',1),(130,96,'Harmony Concepts','',1),(131,97,'Health Tech','',1),(132,98,'Heartland Flax','',1),(133,99,'Hebei Changhao','',1),(134,100,'Hebei Huaheng','',1),(135,101,'Herb Green Health','',1),(136,102,'Hong Hao','',1),(137,103,'Hubei Grand Life Science','',1),(138,104,'Hunan Essence','',1),(139,105,'Imaherb','',1),(140,106,'IN Ingredients','',1),(141,107,'Ingredients Online','',1),(142,108,'Innomark','',1),(143,109,'Inter Naturales','',1),(144,110,'Jiangsu Jiushoutang','',1),(145,111,'JianGxi Tianxin','',1),(146,112,'Jinan Asia Pharmaceutical','',1),(147,113,'JoMar Labs','',1),(148,114,'Jubliant Ingrevia','',1),(149,115,'King-Year Bio','',1),(150,116,'KN Bioscience','',1),(151,117,'Konoshima Chemical','',1),(152,118,'Lakanto','',1),(153,119,'Lallemand','',1),(154,120,'Le-Sen Biotech','',1),(155,121,'Lin-he','',1),(156,122,'Live Earth','',1),(157,123,'Longze Bio','',1),(158,124,'Lycored','',1),(159,125,'Monterey Bay','',1),(160,126,'Mountain Rose','',1),(161,127,'Murray cevticals','',1),(162,128,'Mushroom Harvest','',1),(163,129,'Nammex','',1),(164,130,'National Enzyme Co.','',1),(165,131,'Natreon','',1),(166,132,'Natural Grocers','',1),(167,133,'Nature Vibe','',1),(168,134,'Nature\'s Harvest International','',1),(169,135,'Natures\'s Harvest International','',1),(170,136,'Naturex','',1),(171,137,'NB Foods','',1),(172,138,'Ningbo Herb','',1),(173,139,'Northe','',1),(174,140,'Novel Nutrients','',1),(175,141,'Novotech Nutraceuticals','',1),(176,142,'Now Foods','',1),(177,143,'Nuherbs','',1),(178,144,'Nura','',1),(179,145,'Nutrafood','',1),(180,146,'Nutri Vita','',1),(181,147,'Nutricargo','',1),(182,148,'Nutrient Innovations','',1),(183,149,'Nutriland','',1),(184,150,'Nutrisol Solutions','',1),(185,151,'Nuts.com','',1),(186,152,'OH Nuts','',1),(187,153,'Orcas Naturals','',1),(188,154,'Orgenetics','',1),(189,155,'Parashaunt','',1),(190,156,'Pioneer','',1),(191,157,'PNI','',1),(192,158,'ProNatrual','',1),(193,159,'PurCaf','',1),(194,160,'Pure Assay','',1),(195,161,'Qimei Industrial','',1),(196,162,'Raw Power','',1),(197,163,'RDV','',1),(198,164,'Redmond','',1),(199,165,'Rice Bran Technologies','',1),(200,166,'Rice Plus','',1),(201,167,'Ringing Cedar','',1),(202,168,'Rya Foods','',1),(203,169,'SA Herbal','',1),(204,170,'SA Retail','',1),(205,171,'Saherbal','',1),(206,172,'San Francisco Herb Co','',1),(207,173,'Sandong Aocter','',1),(208,174,'Saw Palmetto Florida','',1),(209,175,'Segment','',1),(210,176,'Shandong Tianli Pharmaceutical','',1),(211,177,'Shining Seas','',1),(212,178,'Shuangta Food','',1),(213,179,'Shuguang','',1),(214,180,'Siberian Green','',1),(215,181,'Silva','',1),(216,182,'Skystone Feed','',1),(217,183,'Skystone Pharm','',1),(218,184,'Small Town Specialties','',1),(219,185,'Starwest Botanicals','',1),(220,186,'Swanson','',1),(221,187,'Synergized','',1),(222,188,'Talya','',1),(223,189,'Teng Yun','',1),(224,190,'TheraPlantes','',1),(225,191,'Tianhua Pharmacy','',1),(226,192,'TruHerb','',1),(227,193,'Urmi Lifesciences','',1),(228,194,'USGreens','',1),(229,195,'Valensa','',1),(230,196,'Van Drunen','',1),(231,197,'Venkatesh','',1),(232,198,'VitaJoy','',1),(233,199,'VitaminSea','',1),(234,200,'Vivion','',1),(235,201,'Wonderful Herb','',1),(236,202,'Wuhan Grand Hoyo','',1),(237,203,'Xi\'an Dealing Biotechnology','',1),(238,204,'Yosin Bio','',1),(239,205,'Z Natural Foods','',1),(240,206,'ZHT Sci-Tech','',1),(241,207,'Alpha','',1),(242,208,'Bright Pharma','',1),(243,209,'Canyon Plastics','',1),(244,210,'Carolina','',1),(245,211,'Comar','',1),(246,212,'Consolidated Design','',1),(247,213,'Desiccare','',1),(248,214,'Industrial Container','',1),(249,215,'Keystone Corp.','',1),(250,216,'MeasureX','',1),(251,217,'Mold-Rite Plastics','',1),(252,218,'National Measures','',1),(253,219,'Performance Dry','',1),(254,220,'Phoenix','',1),(255,221,'PSPrint','',1),(256,222,'Rieke','',1),(257,223,'Silver Spur Corp.','',1),(258,224,'Sonic Plastic','',1),(259,225,'Super Shrink','',1),(260,226,'Total Label USA','',1),(261,227,'Uline','',1),(262,228,'Visible','',1);
/*!40000 ALTER TABLE `Organization_Names` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Organizations`
--

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
  PRIMARY KEY (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=229 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Organizations`
--

LOCK TABLES `Organizations` WRITE;
/*!40000 ALTER TABLE `Organizations` DISABLE KEYS */;
INSERT INTO `Organizations` VALUES (1,'2020-07-01','www.prolifixnutrition.com',1,NULL,'No_Risk',1,1,0,0,0,NULL,NULL),(2,'2022-02-17','balchem.com',0,'2022-02-17','No_Risk',0,0,1,0,0,NULL,'Data from survey'),(3,'2022-01-19','https://alohamedicinals.com/',0,'2022-01-19','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(4,'2022-02-09','www.aunutra.com',0,'2022-02-09','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(5,'2022-02-22','https://www.azurestandard.com/',0,'2022-02-22','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(6,'2022-01-20','allsprouts.com',0,'2022-01-20','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(7,'2022-03-09','bulksupplements.com',0,'2022-03-09','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(8,'2022-02-23','cambridgecommodities.com',0,'2022-02-23','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(9,'2022-02-25','intotherainforest.com',0,'2022-02-25','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(10,'2022-02-25','foodtopiausa.com',0,'2022-02-25','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(11,'2022-02-22','hqorganics.com',0,'2022-02-22','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(12,'2022-01-28','https://honeyville.com/',0,'2022-01-28','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(13,'2022-01-24','www.nutra-max.com',0,'2022-01-24','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(14,'2022-03-09','Libertynatural.com',0,'2022-03-09','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(15,'2022-01-19','LiquaDry.com',0,'2022-01-19','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(16,'2022-02-21','loovfood.com',0,'2022-02-21','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(17,'2022-02-21','naturesflavors.com',0,'2022-02-21','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(18,'2022-01-26','www.npnutra.com',0,'2022-01-26','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(19,'2022-03-01','nexira.com',0,'2022-03-01','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(20,'2022-02-02','https://www.nammex.com/',0,'2022-02-02','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(21,'2022-02-01','essentialorganicingredients.com',0,'2022-02-01','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(22,'2022-01-31','www.pacificbotanicals.com',0,'2022-01-31','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(23,'2022-02-17','pforlife.com',0,'2022-02-17','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(24,'2022-03-08','purebulk.com',0,'2022-03-08','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(25,'2022-03-08','specialtyenzymes.com',0,'2022-03-08','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(26,'2022-01-30','https://austsuperfoods.com.au/',0,'2022-01-30','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(27,'2022-01-30','Healthyflour.com',0,'2022-01-30','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(28,'2022-03-01','unichemsupply.com',0,'2022-03-01','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(29,'2022-02-17','wholeherbcompany.com',0,'2022-02-17','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(30,'2022-02-17','qualitymushroom.com',0,'2022-02-17','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(31,'2022-03-15','xahealthway.com',0,'2022-03-15','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(32,'2022-03-23','stryka.com',0,'2022-03-23','UNKNOWN',1,0,0,0,0,NULL,'Data from survey'),(33,NULL,NULL,0,NULL,'UNKNOWN',0,1,0,0,0,NULL,'Data from URL Library'),(34,NULL,'https://enerex.ca/',0,NULL,'UNKNOWN',0,1,0,0,0,NULL,'Data from URL Library'),(35,NULL,'https://herballygrounded.com/',0,NULL,'UNKNOWN',0,1,0,0,0,NULL,'Data from URL Library'),(36,NULL,NULL,0,NULL,'UNKNOWN',1,1,0,0,0,NULL,'Data from URL Library'),(37,NULL,'https://immunesolution.com/',0,NULL,'UNKNOWN',0,1,0,0,0,NULL,'Data from URL Library'),(38,NULL,'https://majusuperfoods.com/',0,NULL,'UNKNOWN',1,1,0,0,0,NULL,'Data from URL Library'),(39,NULL,'https://www.markusrothkranz.com/online-store/index.html',0,NULL,'UNKNOWN',1,1,0,0,0,NULL,'Data from URL Library'),(40,NULL,'https://makes3organics.com/',0,NULL,'UNKNOWN',0,1,0,0,0,NULL,'Data from URL Library'),(41,NULL,'https://revelationhealth.com/',0,NULL,'UNKNOWN',1,1,0,0,0,NULL,'Data from URL Library'),(42,NULL,'https://vita-myr.com/',0,NULL,'UNKNOWN',0,1,0,0,0,NULL,'Data from URL Library'),(43,NULL,'https://www.knlifebiotics.com/',0,NULL,'UNKNOWN',0,1,0,0,0,NULL,'Data from URL Library'),(44,NULL,'https://www.balanceofnature.com/',0,NULL,'UNKNOWN',0,1,0,0,0,NULL,'Data from URL Library'),(45,NULL,'https://www.naturalapproachnutrition.com/',0,NULL,'UNKNOWN',1,1,0,0,0,NULL,'Data from URL Library'),(46,NULL,'https://www.tranont.com/',0,NULL,'UNKNOWN',0,1,0,0,0,NULL,'Data from URL Library'),(47,NULL,'https://www.bloomfieldroots.com/',0,NULL,'UNKNOWN',1,1,0,0,0,NULL,'Data from URL Library'),(48,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(49,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(50,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(51,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(52,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(53,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(54,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(55,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(56,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(57,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(58,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(59,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(60,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(61,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(62,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(63,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(64,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(65,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(66,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(67,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(68,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(69,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(70,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(71,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(72,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(73,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(74,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(75,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(76,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(77,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(78,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(79,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(80,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(81,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(82,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(83,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(84,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(85,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(86,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(87,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(88,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(89,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(90,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(91,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(92,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(93,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(94,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(95,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(96,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(97,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(98,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(99,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(100,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(101,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(102,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(103,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(104,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(105,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(106,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(107,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(108,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(109,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(110,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(111,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(112,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(113,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(114,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(115,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(116,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(117,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(118,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(119,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(120,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(121,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(122,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(123,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(124,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(125,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(126,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(127,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(128,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(129,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(130,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(131,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(132,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(133,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(134,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(135,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(136,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(137,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(138,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(139,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(140,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(141,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(142,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(143,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(144,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(145,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(146,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(147,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(148,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(149,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(150,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(151,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(152,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(153,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(154,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(155,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(156,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(157,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(158,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(159,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(160,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(161,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(162,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(163,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(164,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(165,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(166,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(167,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(168,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(169,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(170,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(171,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(172,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(173,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(174,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(175,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(176,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(177,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(178,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(179,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(180,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(181,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(182,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(183,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(184,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(185,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(186,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(187,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(188,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(189,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(190,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(191,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(192,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(193,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(194,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(195,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(196,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(197,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(198,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(199,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(200,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(201,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(202,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(203,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(204,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(205,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(206,NULL,NULL,0,NULL,'UNKNOWN',1,0,0,0,0,NULL,'Data from Powders Inventory'),(207,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(208,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(209,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(210,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(211,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(212,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(213,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(214,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(215,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(216,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(217,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(218,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(219,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(220,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(221,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(222,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(223,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(224,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(225,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(226,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(227,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory'),(228,NULL,NULL,0,NULL,'No_Risk',1,0,0,0,0,NULL,'Data from Items Inventory');
/*!40000 ALTER TABLE `Organizations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `People`
--

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
-- Dumping data for table `People`
--

LOCK TABLES `People` WRITE;
/*!40000 ALTER TABLE `People` DISABLE KEYS */;
INSERT INTO `People` VALUES (1,1,'Kathy','Jensen','2024-03-22 22:39:06','Owner','Client Relations, Purchasing','8016025244',NULL,'info@holisticlifesupplements.com',NULL,NULL,1,NULL,NULL,NULL),(2,1,'Steven','Jensen','2024-03-22 22:39:06','Owner','Client Relations, Purchasing','8017873151',NULL,'stevej@prolifixnutrition.com',NULL,NULL,1,NULL,NULL,NULL),(3,1,'Ian','Bull','2024-03-22 22:39:06','Manager','Maintenance, Human Recources, Production','9285645378',NULL,'ianbullpn@gmail.com',NULL,NULL,1,NULL,'2024-02-15',NULL),(4,1,'Nathaniel','Reeves','2024-03-22 22:39:06','Manager','Quality, Information Technology, Software Development','8013801953',NULL,'nathanr@prolifixnutrition.com',NULL,'1998-12-14',1,'2020-06-20',NULL,'10399'),(5,1,'Anna','Thayer','2024-03-22 22:39:06','Batcher','Production','4352293919',NULL,NULL,NULL,NULL,1,NULL,NULL,'9188'),(6,1,'Coby','Thayer','2024-03-22 22:39:06','Team Lead','Production','4352159484',NULL,'colbyt@prolifixnutrition.com',NULL,NULL,1,NULL,NULL,'9187'),(7,1,'Benjamin','Black','2024-03-22 22:39:06','Staff','Production','4356164236',NULL,NULL,NULL,NULL,1,NULL,NULL,'9186'),(8,1,'James','Beckstrand','2024-03-22 22:39:06','Staff','Production',NULL,NULL,NULL,NULL,'1983-01-30',1,NULL,NULL,'10568'),(9,1,'Sage','Stockard','2024-03-22 22:39:06','Staff','Production',NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,'12475'),(10,1,'Jason','Hare','2024-03-22 22:39:06','Staff','Production',NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,'12460'),(11,1,'Amy','Hobbs-Densley','2024-03-22 22:39:06','Staff','Quality','4352224117',NULL,'amyhd@prolifixnutrition.com',NULL,NULL,1,'2023-09-26',NULL,'14539'),(12,1,'Dallas','Jensen','2024-03-22 22:39:06','Staff','Inventory','5183733307',NULL,NULL,NULL,NULL,1,'2023-09-26','2023-12-18',NULL),(13,1,'Krzysztof','Bednarczuk','2024-03-26 16:36:15','Staff','Inventory','3125363767',NULL,'krzysztofb@prolifixnutrition.com',NULL,NULL,1,'2024-03-25',NULL,NULL);
/*!40000 ALTER TABLE `People` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

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
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,1,'kathyj','pbkdf2:sha256:150000$OGmf0SV2$67a192b683bee0ee1e175b4a8601e7aec19bcb8319f66f920b9d608b352e74de','/users/kathyj001.jpg','Light','{\"_id\":1,\"database_priveleges\":{\"Formulas\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Inventory\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Manufacturing\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Orders\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Organizations\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Products\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]}}}'),(2,2,'stevej','pbkdf2:sha256:150000$ARAhwT0G$dbdad12136ad583e387d1521e22a511908fc18b46df53c96cc0e1a6db0afab9a','/users/stevej002.jpg','Light','{\"_id\":2,\"database_priveleges\":{\"Formulas\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Inventory\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Manufacturing\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Orders\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Organizations\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Products\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]}}}'),(4,4,'nathanielr','pbkdf2:sha256:150000$s5Atq4Gb$7a3fdad4b7b03fe84f7a5d94ac4ac8d07ec3c4c6ad198c5526859d9c114c4daf','/users/nathanielr004.jpg','Dark','{\"_id\":4,\"database_priveleges\":{\"Formulas\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Inventory\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Manufacturing\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Orders\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Organizations\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Products\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]}}}'),(5,5,'annat','pbkdf2:sha256:150000$vj0jLaNU$9da76e83ab714215800caf9c854b84b9572fa8d5f35c4a4ac4581cc80b7a3ce0','/users/annat005.jpg','Light','{\"_id\":5,\"database_priveleges\":{\"Formulas\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Inventory\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Manufacturing\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Orders\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Organizations\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Products\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]}}}'),(6,6,'cobyt','pbkdf2:sha256:150000$cN0b6XBh$9b72c6ac2b37491321ff0c29e9e60b8b942ce28d9dde316202f439395ee2f781','/users/cobyt006.jpg','Light','{\"_id\":6,\"database_priveleges\":{\"Formulas\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Inventory\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Manufacturing\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Orders\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Organizations\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Products\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]}}}'),(7,7,'benjaminb','pbkdf2:sha256:150000$x9OVJujD$63efba77e774384f5e7e3be8319d843796574e68f18eeca375488c9e8d85fa0a','/users/benjaminb007.jpg','Light','{\"_id\":7,\"database_priveleges\":{\"Formulas\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Inventory\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Manufacturing\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Orders\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Organizations\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Products\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]}}}'),(8,8,'jamesb','pbkdf2:sha256:150000$5ZFy30w3$7272e826a67c223d472910b0fe3f06078c68c5734ca613a9b0ccd90d58c6734a','/users/jamesb008.jpg','Light','{\"_id\":8,\"database_priveleges\":{\"Formulas\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Inventory\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Manufacturing\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Orders\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Organizations\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Products\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]}}}'),(9,9,'sages','pbkdf2:sha256:150000$KQYTZj4S$259903c44e6129803fc07c0e739913081e7cc539f3400316bc3771366ed17822','/users/sages009.jpg','Light','{\"_id\":9,\"database_priveleges\":{\"Formulas\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Inventory\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Manufacturing\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Orders\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Organizations\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Products\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]}}}'),(10,10,'jasonh','pbkdf2:sha256:150000$glYAAK2m$79460e46a62a8eb9c75c4e05fd61c6b2906aa3c83904ddb1aa5493ae2714256f','/users/jasonh010.jpg','Light','{\"_id\":10,\"database_priveleges\":{\"Formulas\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Inventory\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Manufacturing\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Orders\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Organizations\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Products\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]}}}'),(11,11,'amyh','pbkdf2:sha256:150000$glYAAK2m$79460e46a62a8eb9c75c4e05fd61c6b2906aa3c83904ddb1aa5493ae2714256f','/users/amyh011.jpg','Light','{\"_id\":11,\"database_priveleges\":{\"Formulas\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Inventory\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Manufacturing\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Orders\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Organizations\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Products\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]}}}'),(12,13,'krysztofb','scrypt:32768:8:1$sU2AQnq8K3PMI5dp$df01838bf240a551047df79c2a08733e2e7649cd6c72a59a24de950f4194e8c2ebad3abd45ac433ef3e1cb9ccf365daf23c77dc857fb1c6333523c02a341574b','/users/krystofb.jpg','Light','{\"_id\":12,\"database_priveleges\":{\"Formulas\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Inventory\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Manufacturing\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Orders\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Organizations\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]},\"Products\":{\"default\":[\"GET\",\"POST\",\"PUT\",\"DELETE\"]}}}');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `org_and_people_detail`
--

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

-- Dump completed on 2024-06-21 16:26:31
