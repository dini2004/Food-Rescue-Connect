-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: food_rescue_connect
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `food_donations`
--

DROP TABLE IF EXISTS `food_donations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `food_donations` (
  `donation_id` int NOT NULL AUTO_INCREMENT,
  `donor_id` int DEFAULT NULL,
  `food_name` varchar(100) DEFAULT NULL,
  `quantity` varchar(50) DEFAULT NULL,
  `expiry_time` datetime DEFAULT NULL,
  `pickup_address` text,
  `status` enum('Available','Accepted','Completed') DEFAULT 'Available',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `food_image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`donation_id`),
  KEY `donor_id` (`donor_id`),
  CONSTRAINT `food_donations_ibfk_1` FOREIGN KEY (`donor_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food_donations`
--

LOCK TABLES `food_donations` WRITE;
/*!40000 ALTER TABLE `food_donations` DISABLE KEYS */;
INSERT INTO `food_donations` VALUES (1,NULL,'rice','1kg','2026-07-24 12:03:00','mulb','Accepted','2026-07-23 06:33:27',NULL),(2,NULL,'rice','1kg','2026-07-24 12:03:00','mulb','Accepted','2026-07-23 06:34:07',NULL),(3,NULL,'bath','20 plates','2026-07-24 12:08:00','banglore','Accepted','2026-07-23 06:38:35',NULL),(4,1,'chapathi','10','2026-07-24 14:35:00','banglore','Accepted','2026-07-24 09:05:41',NULL),(7,1,'dd','2','2026-07-25 21:31:00','banglore as','Completed','2026-07-24 16:02:03',NULL),(9,6,'bath','10plates','2026-07-26 11:32:00','banglore','Completed','2026-07-25 06:02:15',NULL),(10,1,'bath','1kg','2026-07-26 18:23:00','banglore','Available','2026-07-25 12:53:34','WhatsApp_Image_2026-07-01_at_6.31.38_PM.jpeg'),(11,1,'bath','1kg','2026-07-27 09:10:00','banglore','Available','2026-07-26 03:40:58','WhatsApp_Image_2026-07-01_at_6.31.38_PM.jpeg'),(12,1,'bath','1kg','2026-07-26 09:11:00','ban','Available','2026-07-26 03:41:29','WhatsApp_Image_2026-07-01_at_6.31.38_PM.jpeg'),(13,1,'bath','1kg','2026-07-27 09:11:00','b','Available','2026-07-26 03:41:52','WhatsApp_Image_2026-07-01_at_6.29.44_PM.jpeg'),(14,1,'bath','1kg','2026-07-27 09:12:00','sa','Available','2026-07-26 03:42:26','WhatsApp_Image_2026-07-22_at_6.05.01_PM.jpeg'),(15,1,'asa','as','2026-07-27 09:12:00','ad','Available','2026-07-26 03:42:54','sig_1.jpeg'),(16,1,'ad','ad','2026-07-27 09:13:00','ads','Available','2026-07-26 03:43:16','WhatsApp_Image_2026-07-22_at_6.05.01_PM.jpeg'),(17,1,'ads','ad','2026-07-17 09:13:00','ad','Available','2026-07-26 03:43:46','WhatsApp_Image_2026-07-01_at_6.29.44_PM.jpeg'),(18,1,'bath','1kg','2026-07-30 17:43:00','hjn','Available','2026-07-26 12:13:46','WhatsApp_Image_2026-07-01_at_6.29.44_PM.jpeg'),(19,1,'wq','1','2026-07-27 17:54:00','w','Available','2026-07-26 12:24:24','WhatsApp_Image_2026-07-01_at_6.29.44_PM.jpeg'),(20,1,'q','1','2026-07-31 17:54:00','sd','Available','2026-07-26 12:24:54','WhatsApp_Image_2026-07-01_at_6.29.44_PM.jpeg');
/*!40000 ALTER TABLE `food_donations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ngo_requests`
--

DROP TABLE IF EXISTS `ngo_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ngo_requests` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `donation_id` int DEFAULT NULL,
  `ngo_id` int DEFAULT NULL,
  `status` enum('Pending','Accepted','Rejected') DEFAULT 'Pending',
  `request_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`request_id`),
  KEY `donation_id` (`donation_id`),
  KEY `ngo_id` (`ngo_id`),
  CONSTRAINT `ngo_requests_ibfk_1` FOREIGN KEY (`donation_id`) REFERENCES `food_donations` (`donation_id`),
  CONSTRAINT `ngo_requests_ibfk_2` FOREIGN KEY (`ngo_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ngo_requests`
--

LOCK TABLES `ngo_requests` WRITE;
/*!40000 ALTER TABLE `ngo_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `ngo_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `role` enum('Donor','NGO','Admin') DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `reward_points` int DEFAULT '0',
  `badge` varchar(50) DEFAULT 'Bronze Donor',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Dinesh','kp846132@gmail.com','@Dinesh1234','072048422611','Donor','2026-07-22 07:57:08',100,'? Gold Donor'),(6,'kempe','kempe@gmail.com','@kempe123','9845217554','Donor','2026-07-22 08:20:29',0,'? Bronze Donor'),(9,'Hemanth Kumar R V','hemanthkumarrv123@gmail.com','@hemanth123','06361081518','NGO','2026-07-23 07:43:45',0,'? Bronze Donor'),(11,'ambi','ambi@gmail.com','@Dinesh123','7845612311','NGO','2026-07-23 08:10:05',0,'? Bronze Donor'),(13,'dini','dini@gmail.com','@Dinesh123','7204842261','Admin','2026-07-24 10:10:23',0,'? Bronze Donor'),(14,'rahul','rahul@gmail.com','@Dinesh123','07204842261','NGO','2026-07-25 06:04:32',0,'? Bronze Donor');
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

-- Dump completed on 2026-07-28 13:49:22
