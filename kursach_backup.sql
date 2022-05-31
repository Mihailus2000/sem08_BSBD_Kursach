-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: kursach
-- ------------------------------------------------------
-- Server version	8.0.29

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
-- Table structure for table `carriage_types`
--

DROP TABLE IF EXISTS `carriage_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carriage_types` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `type_name` varchar(45) NOT NULL,
  `is_archived` bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carriage_types`
--

LOCK TABLES `carriage_types` WRITE;
/*!40000 ALTER TABLE `carriage_types` DISABLE KEYS */;
INSERT INTO `carriage_types` VALUES (1,'Плацкартный',_binary '\0'),(2,'Купе',_binary '\0'),(3,'Сидячий',_binary '\0');
/*!40000 ALTER TABLE `carriage_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carriages`
--

DROP TABLE IF EXISTS `carriages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carriages` (
  `carriage_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `carriage_name` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_general_ci NOT NULL,
  `carriage_type` bigint unsigned NOT NULL,
  PRIMARY KEY (`carriage_id`),
  UNIQUE KEY `carriage_id_UNIQUE` (`carriage_id`),
  KEY `fk_carriages_carriage_types1_idx` (`carriage_type`),
  CONSTRAINT `fk_carriages_carriage_types1` FOREIGN KEY (`carriage_type`) REFERENCES `carriage_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carriages`
--

LOCK TABLES `carriages` WRITE;
/*!40000 ALTER TABLE `carriages` DISABLE KEYS */;
INSERT INTO `carriages` VALUES (1,'B001',1),(2,'B002',1),(3,'B003',1),(4,'B004',1),(5,'B005',1),(6,'B006',1),(7,'B007',1),(8,'B008',1),(9,'B009',1),(10,'B010',1),(11,'B011',1),(12,'B012',1),(13,'B013',1),(14,'B014',1),(15,'B015',1),(16,'B016',1),(17,'B017',1),(18,'B018',1),(19,'B019',1),(20,'B020',1),(21,'B021',1),(22,'B022',1),(23,'B023',1),(24,'B024',1),(25,'B025',1),(26,'B026',1),(27,'B027',1),(28,'B028',1),(29,'B029',1),(30,'B030',1),(31,'B100',2),(32,'B101',2),(33,'B102',2),(34,'B103',2),(35,'B104',2),(36,'B105',2),(37,'B106',2),(38,'B107',2),(39,'B108',2),(40,'B109',2),(41,'B110',2),(42,'B111',2),(43,'B112',2),(44,'B113',2),(45,'B114',2),(46,'B115',2),(47,'B116',2),(48,'B117',2),(49,'B118',2),(50,'B119',2),(51,'B120',2),(52,'B121',2),(53,'B122',2),(54,'B123',2),(55,'B124',2),(56,'B125',2),(57,'B126',2),(58,'B127',2),(59,'B128',2),(60,'B129',2),(61,'B130',2),(62,'B200',3),(63,'B201',3),(64,'B202',3),(65,'B203',3),(66,'B204',3),(67,'B205',3),(68,'B206',3),(69,'B207',3),(70,'B208',3),(71,'B209',3),(72,'B210',3),(73,'B211',3),(74,'B212',3),(75,'B213',3),(76,'B214',3),(77,'B215',3),(78,'B216',3),(79,'B217',3),(80,'B218',3),(81,'B219',3),(82,'B220',3),(83,'B221',3),(84,'B222',3),(85,'B223',3),(86,'B224',3),(87,'B225',3),(88,'B226',3),(89,'B227',3),(90,'B228',3),(91,'B229',3),(92,'B230',3);
/*!40000 ALTER TABLE `carriages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carriages_to_train`
--

DROP TABLE IF EXISTS `carriages_to_train`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carriages_to_train` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `order_num` int unsigned NOT NULL,
  `train_id` bigint unsigned NOT NULL,
  `carriage_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_carriages_to_train_trains1_idx` (`train_id`),
  KEY `fk_carriages_to_train_carriages1_idx` (`carriage_id`),
  CONSTRAINT `fk_carriages_to_train_carriages1` FOREIGN KEY (`carriage_id`) REFERENCES `carriages` (`carriage_id`),
  CONSTRAINT `fk_carriages_to_train_trains1` FOREIGN KEY (`train_id`) REFERENCES `trains` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carriages_to_train`
--

LOCK TABLES `carriages_to_train` WRITE;
/*!40000 ALTER TABLE `carriages_to_train` DISABLE KEYS */;
INSERT INTO `carriages_to_train` VALUES (1,1,8,1),(2,2,8,2),(3,3,8,3),(7,4,8,7),(8,5,8,8),(20,8,9,4),(21,7,9,6),(23,6,9,19),(24,5,9,20),(25,4,9,31),(26,3,9,32),(28,6,8,29),(29,7,8,5),(30,2,9,21),(31,1,9,22),(32,1,12,9),(33,2,12,10),(35,1,13,12),(36,2,13,13),(38,1,14,15),(39,2,14,16),(40,3,14,33),(41,4,14,34),(42,3,13,35),(43,3,12,41),(44,1,16,11),(45,2,16,14),(46,3,16,36),(47,4,16,62);
/*!40000 ALTER TABLE `carriages_to_train` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_general_ci NOT NULL,
  `second_name` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_general_ci NOT NULL,
  `patronym` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_general_ci DEFAULT NULL,
  `login` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_general_ci DEFAULT NULL,
  `passwd` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_general_ci DEFAULT NULL,
  `email` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `order_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `train_id` bigint unsigned NOT NULL,
  `route_id` bigint unsigned NOT NULL,
  `carriage_id` bigint unsigned NOT NULL,
  `seat_id` bigint unsigned NOT NULL,
  `FIO` varchar(45) NOT NULL,
  `station_from_id` bigint unsigned NOT NULL,
  `station_to_id` bigint unsigned NOT NULL,
  `date_from` date DEFAULT NULL,
  `date_train_from` date NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `fk_order_trains1_idx` (`train_id`),
  KEY `fk_order_carriages1_idx` (`carriage_id`),
  KEY `fk_order_global_seat_type_id_to_carriage_type1_idx` (`seat_id`),
  KEY `fk_order_stations1_idx` (`station_from_id`),
  KEY `fk_order_stations2_idx` (`station_to_id`),
  KEY `fk_order_routes1_idx` (`route_id`),
  CONSTRAINT `fk_order_carriages1` FOREIGN KEY (`carriage_id`) REFERENCES `carriages` (`carriage_id`),
  CONSTRAINT `fk_order_global_seat_type_id_to_carriage_type1` FOREIGN KEY (`seat_id`) REFERENCES `seats` (`id`),
  CONSTRAINT `fk_order_routes1` FOREIGN KEY (`route_id`) REFERENCES `routes` (`route_id`),
  CONSTRAINT `fk_order_stations1` FOREIGN KEY (`station_from_id`) REFERENCES `stations` (`station_id`),
  CONSTRAINT `fk_order_stations2` FOREIGN KEY (`station_to_id`) REFERENCES `stations` (`station_id`),
  CONSTRAINT `fk_order_trains1` FOREIGN KEY (`train_id`) REFERENCES `trains` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,12,93,9,132,'ФИО1',1,2,'2022-06-01','0000-00-00'),(2,12,93,9,140,'ФИО2',4,7,'2022-06-01','0000-00-00'),(3,14,93,12,130,'ФИО3',2,3,'2022-05-30','0000-00-00'),(4,14,94,15,133,'ФИО11',8,9,'2022-06-03','0000-00-00'),(6,14,94,16,145,'ФИО33',8,9,'2022-06-03','2022-05-28'),(7,12,93,9,133,'Березин Михаил Алексеевич',1,7,'2022-05-30','2022-05-30'),(8,16,96,36,91,'Чел1',2,7,'2022-05-30','2022-05-30'),(9,16,96,62,182,'Березин Михаил Алексеевич',2,9,'2022-05-30','2022-05-30'),(10,16,96,11,127,'Березин Михаил Алексеевич',2,9,'2022-05-30','2022-05-30'),(11,16,96,11,128,'Березин Михаил Алексеевич2',2,9,'2022-05-30','2022-05-30'),(12,16,96,11,171,'Березин Михаил Алексеевич',2,9,'2022-05-30','2022-05-30'),(13,12,93,9,130,'Ф И О',1,4,'2022-06-01','2022-06-01');
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passages`
--

DROP TABLE IF EXISTS `passages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passages` (
  `passage_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `day_of_week` tinyint unsigned DEFAULT NULL,
  `train_id` bigint unsigned NOT NULL,
  `passage_first_station_to_route_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`passage_id`),
  KEY `fk_routes_to_fromstation_to_train_day_of_week_trains1_idx` (`train_id`),
  KEY `fk_routes_to_fromstation_to_train_day_of_week_stations_to_r_idx` (`passage_first_station_to_route_id`),
  CONSTRAINT `fk_passages_stations_to_routes1` FOREIGN KEY (`passage_first_station_to_route_id`) REFERENCES `stations_to_routes` (`id`),
  CONSTRAINT `fk_passages_trains1` FOREIGN KEY (`train_id`) REFERENCES `trains` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passages`
--

LOCK TABLES `passages` WRITE;
/*!40000 ALTER TABLE `passages` DISABLE KEYS */;
INSERT INTO `passages` VALUES (100,0,12,34),(102,1,12,34),(103,2,12,34),(104,3,13,34),(105,4,13,34),(107,5,13,34),(108,2,13,34),(111,6,14,36),(115,0,16,48),(116,1,16,48),(117,2,16,48),(118,3,16,48),(119,4,16,48),(120,5,16,48),(121,6,16,48),(122,2,16,34),(123,3,16,34),(124,5,16,34);
/*!40000 ALTER TABLE `passages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prices`
--

DROP TABLE IF EXISTS `prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prices` (
  `price_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `route_id` bigint unsigned NOT NULL,
  `station_from_id` bigint unsigned NOT NULL,
  `station_to_id` bigint unsigned NOT NULL,
  `coefficient` float unsigned NOT NULL,
  `seat_type_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`price_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prices`
--

LOCK TABLES `prices` WRITE;
/*!40000 ALTER TABLE `prices` DISABLE KEYS */;
/*!40000 ALTER TABLE `prices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `routes`
--

DROP TABLE IF EXISTS `routes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `routes` (
  `route_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `number` varchar(15) CHARACTER SET utf8mb3 COLLATE utf8_general_ci DEFAULT NULL,
  `tariff` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`route_id`),
  UNIQUE KEY `number_UNIQUE` (`number`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `routes`
--

LOCK TABLES `routes` WRITE;
/*!40000 ALTER TABLE `routes` DISABLE KEYS */;
INSERT INTO `routes` VALUES (93,'МскВоск','1',1000),(94,'ЧапСамара','2',300),(96,'МскХзВоскр','3',1700);
/*!40000 ALTER TABLE `routes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seat_types`
--

DROP TABLE IF EXISTS `seat_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seat_types` (
  `seat_type_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `type_name` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_general_ci DEFAULT NULL,
  `is_archived` bit(1) DEFAULT b'0',
  PRIMARY KEY (`seat_type_id`),
  UNIQUE KEY `type_name_UNIQUE` (`type_name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seat_types`
--

LOCK TABLES `seat_types` WRITE;
/*!40000 ALTER TABLE `seat_types` DISABLE KEYS */;
INSERT INTO `seat_types` VALUES (1,'Верхнее',_binary '\0'),(2,'Нижнее',_binary '\0'),(3,'Верхнее боковое',_binary '\0'),(4,'Нижнее боковое',_binary '\0'),(5,'Сидячее',_binary '\0');
/*!40000 ALTER TABLE `seat_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seats`
--

DROP TABLE IF EXISTS `seats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seats` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `number` int unsigned NOT NULL,
  `carriage_type` bigint NOT NULL,
  `seat_type` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=249 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seats`
--

LOCK TABLES `seats` WRITE;
/*!40000 ALTER TABLE `seats` DISABLE KEYS */;
INSERT INTO `seats` VALUES (91,1,2,2),(92,2,2,1),(93,3,2,2),(94,4,2,1),(95,5,2,2),(96,6,2,1),(97,7,2,2),(98,8,2,1),(99,9,2,2),(100,10,2,1),(101,11,2,2),(102,12,2,1),(103,13,2,2),(104,14,2,1),(105,15,2,2),(106,16,2,1),(107,17,2,2),(108,18,2,1),(109,19,2,2),(110,20,2,1),(111,21,2,2),(112,22,2,1),(113,23,2,2),(114,24,2,1),(115,25,2,2),(116,26,2,1),(117,27,2,2),(118,28,2,1),(119,29,2,2),(120,30,2,1),(121,31,2,2),(122,32,2,1),(123,33,2,2),(124,34,2,1),(125,35,2,2),(126,36,2,1),(127,1,1,2),(128,2,1,1),(129,3,1,2),(130,4,1,1),(131,5,1,2),(132,6,1,1),(133,7,1,2),(134,8,1,1),(135,9,1,2),(136,10,1,1),(137,11,1,2),(138,12,1,1),(139,13,1,2),(140,14,1,1),(141,15,1,2),(142,16,1,1),(143,17,1,2),(144,18,1,1),(145,19,1,2),(146,20,1,1),(147,21,1,2),(148,22,1,1),(149,23,1,2),(150,24,1,1),(151,25,1,2),(152,26,1,1),(153,27,1,2),(154,28,1,1),(155,29,1,2),(156,30,1,1),(157,31,1,2),(158,32,1,1),(159,33,1,2),(160,34,1,1),(161,35,1,2),(162,36,1,1),(163,37,1,4),(164,38,1,3),(165,39,1,4),(166,40,1,3),(167,41,1,4),(168,42,1,3),(169,43,1,4),(170,44,1,3),(171,45,1,4),(172,46,1,3),(173,47,1,4),(174,48,1,3),(175,49,1,4),(176,50,1,3),(177,51,1,4),(178,52,1,3),(179,53,1,4),(180,54,1,3),(181,1,3,5),(182,2,3,5),(183,3,3,5),(184,4,3,5),(185,5,3,5),(186,6,3,5),(187,7,3,5),(188,8,3,5),(189,9,3,5),(190,10,3,5),(191,11,3,5),(192,12,3,5),(193,13,3,5),(194,14,3,5),(195,15,3,5),(196,16,3,5),(197,17,3,5),(198,18,3,5),(199,19,3,5),(200,20,3,5),(201,21,3,5),(202,22,3,5),(203,23,3,5),(204,24,3,5),(205,25,3,5),(206,26,3,5),(207,27,3,5),(208,28,3,5),(209,29,3,5),(210,30,3,5),(211,31,3,5),(212,32,3,5),(213,33,3,5),(214,34,3,5),(215,35,3,5),(216,36,3,5),(217,37,3,5),(218,38,3,5),(219,39,3,5),(220,40,3,5),(221,41,3,5),(222,42,3,5),(223,43,3,5),(224,44,3,5),(225,45,3,5),(226,46,3,5),(227,47,3,5),(228,48,3,5),(229,49,3,5),(230,50,3,5),(231,51,3,5),(232,52,3,5),(233,53,3,5),(234,54,3,5),(235,55,3,5),(236,56,3,5),(237,57,3,5),(238,58,3,5),(239,59,3,5),(240,60,3,5),(241,61,3,5),(242,62,3,5),(243,63,3,5),(244,64,3,5),(245,65,3,5),(246,66,3,5),(247,67,3,5),(248,68,3,5);
/*!40000 ALTER TABLE `seats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stations`
--

DROP TABLE IF EXISTS `stations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stations` (
  `station_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `station_name` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_general_ci DEFAULT NULL,
  `is_active` bit(1) NOT NULL DEFAULT b'1',
  PRIMARY KEY (`station_id`),
  UNIQUE KEY `station_name_UNIQUE` (`station_name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stations`
--

LOCK TABLES `stations` WRITE;
/*!40000 ALTER TABLE `stations` DISABLE KEYS */;
INSERT INTO `stations` VALUES (1,'Москва',_binary ''),(2,'Выхино',_binary ''),(3,'Люберцы',_binary ''),(4,'Воскресенск',_binary ''),(5,'Рязань',_binary ''),(6,'Инза',_binary ''),(7,'Сызрань',_binary ''),(8,'Чапаевск',_binary ''),(9,'Самара',_binary '');
/*!40000 ALTER TABLE `stations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stations_to_routes`
--

DROP TABLE IF EXISTS `stations_to_routes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stations_to_routes` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `station_id` bigint unsigned NOT NULL,
  `route_id` bigint unsigned NOT NULL,
  `sort_order` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_stations_to_routes_routes1_idx` (`route_id`),
  KEY `fk_stations_to_routes_stations1_idx` (`station_id`),
  CONSTRAINT `fk_stations_to_routes_routes` FOREIGN KEY (`route_id`) REFERENCES `routes` (`route_id`),
  CONSTRAINT `fk_stations_to_routes_stations1` FOREIGN KEY (`station_id`) REFERENCES `stations` (`station_id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stations_to_routes`
--

LOCK TABLES `stations_to_routes` WRITE;
/*!40000 ALTER TABLE `stations_to_routes` DISABLE KEYS */;
INSERT INTO `stations_to_routes` VALUES (34,1,93,1),(36,8,94,1),(37,9,94,2),(39,2,93,2),(40,3,93,3),(41,4,93,4),(42,3,94,3),(43,7,93,5),(48,1,96,1),(49,6,96,2),(50,2,96,3),(51,3,96,4),(52,4,96,5),(53,5,96,6),(54,7,96,7),(55,8,96,8),(56,9,96,9);
/*!40000 ALTER TABLE `stations_to_routes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tickets` (
  `ticket_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `route_id` bigint unsigned NOT NULL,
  `station_from_id` bigint unsigned NOT NULL,
  `station_to_id` bigint unsigned NOT NULL,
  `date_travel_from` date NOT NULL,
  `date_travel_to` date NOT NULL,
  `seat_id` bigint unsigned NOT NULL,
  `price` int unsigned NOT NULL,
  `customer_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`ticket_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timetable`
--

DROP TABLE IF EXISTS `timetable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timetable` (
  `time_table_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `station_id` bigint unsigned NOT NULL,
  `arrival_time` time NOT NULL,
  `delay` smallint unsigned NOT NULL,
  `route_id` bigint unsigned NOT NULL,
  `train_id` bigint unsigned NOT NULL,
  `minutes_to_next_station` int NOT NULL DEFAULT '0',
  `price_coeff` double unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`time_table_id`),
  KEY `fk_timetable_stations1_idx` (`station_id`),
  KEY `fk_timetable_routes1_idx` (`route_id`),
  KEY `fk_timetable_trains1_idx` (`train_id`),
  CONSTRAINT `fk_timetable_routes1` FOREIGN KEY (`route_id`) REFERENCES `routes` (`route_id`),
  CONSTRAINT `fk_timetable_stations1` FOREIGN KEY (`station_id`) REFERENCES `stations` (`station_id`),
  CONSTRAINT `fk_timetable_trains1` FOREIGN KEY (`train_id`) REFERENCES `trains` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timetable`
--

LOCK TABLES `timetable` WRITE;
/*!40000 ALTER TABLE `timetable` DISABLE KEYS */;
INSERT INTO `timetable` VALUES (84,1,'01:00:00',12,93,12,60,0.4),(85,2,'02:00:00',13,93,12,60,0.9),(86,3,'03:00:00',12,93,12,60,1.2),(87,4,'04:00:00',20,93,12,60,0.6),(88,2,'11:00:00',10,93,13,60,0.5),(89,3,'12:00:00',13,93,13,120,0.7),(93,7,'05:00:00',0,93,12,0,0.49),(94,7,'14:00:00',0,93,13,0,0.5),(98,8,'01:00:00',25,94,14,120,0.8),(100,3,'05:00:00',0,94,14,0,0.8),(104,9,'00:00:00',0,94,14,0,1.3),(105,1,'01:30:00',20,96,16,120,0.1),(106,6,'03:40:00',10,96,16,10,0.08),(107,2,'03:55:00',5,96,16,60,0.15),(108,3,'04:59:00',4,96,16,31,0.11),(109,4,'05:40:00',10,96,16,40,0.14),(110,5,'06:35:00',15,96,16,25,0.13),(111,7,'07:10:00',10,96,16,30,0.09),(112,9,'08:50:00',0,96,16,0,0.1),(113,8,'07:50:00',10,96,16,60,0.1),(115,2,'00:00:00',0,93,16,0,0),(116,4,'00:00:00',0,93,16,0,0);
/*!40000 ALTER TABLE `timetable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trains`
--

DROP TABLE IF EXISTS `trains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trains` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `number` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `number_UNIQUE` (`number`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trains`
--

LOCK TABLES `trains` WRITE;
/*!40000 ALTER TABLE `trains` DISABLE KEYS */;
INSERT INTO `trains` VALUES (17,'поезд007'),(12,'Поезд1'),(13,'Поезд2'),(14,'Поезд3'),(16,'поезд4');
/*!40000 ALTER TABLE `trains` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `login` varchar(20) NOT NULL,
  `password` varchar(45) NOT NULL,
  `privelegy_level` int unsigned NOT NULL DEFAULT '10',
  PRIMARY KEY (`user_id`,`login`),
  UNIQUE KEY `login_UNIQUE` (`login`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'micberezin','c9834de854df995a830e89c2347a8667',0),(2,'user01','2d25eb22775dbfee8a4e201d974bfae7',10),(3,'user02','d02f3fc80bc5f7bab417e5acfe0355e9',10),(4,'user007','8a38e13f02a7823e5d0567ff2de17902',10),(5,'','650e2e193a7da900f43dc8eedabb8731',10);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-31  7:40:09
