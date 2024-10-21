-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: time2dinedb
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `Id` char(36) NOT NULL DEFAULT (uuid()),
  `UserId` char(36) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `UserId` (`UserId`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('71a486d2-7b80-11ef-9c88-00090ffe0001','71a0a69e-7b80-11ef-9c88-00090ffe0001');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beverage`
--

DROP TABLE IF EXISTS `beverage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `beverage` (
  `Id` char(36) NOT NULL DEFAULT (uuid()),
  `IsAlcoholic` tinyint(1) NOT NULL,
  `NutId` char(36) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `NutId` (`NutId`),
  CONSTRAINT `beverage_ibfk_1` FOREIGN KEY (`NutId`) REFERENCES `nutritions` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beverage`
--

LOCK TABLES `beverage` WRITE;
/*!40000 ALTER TABLE `beverage` DISABLE KEYS */;
INSERT INTO `beverage` VALUES ('7f64c245-7b85-11ef-9c88-00090ffe0001',0,'7f633d51-7b85-11ef-9c88-00090ffe0001'),('7f64cb14-7b85-11ef-9c88-00090ffe0001',0,'7f6403ae-7b85-11ef-9c88-00090ffe0001'),('7f64cf50-7b85-11ef-9c88-00090ffe0001',0,'7f6405ab-7b85-11ef-9c88-00090ffe0001'),('7f64d113-7b85-11ef-9c88-00090ffe0001',0,'7f640756-7b85-11ef-9c88-00090ffe0001'),('7f64d275-7b85-11ef-9c88-00090ffe0001',1,'7f640869-7b85-11ef-9c88-00090ffe0001'),('7f64d3b4-7b85-11ef-9c88-00090ffe0001',1,'7f640979-7b85-11ef-9c88-00090ffe0001'),('7f64d4f2-7b85-11ef-9c88-00090ffe0001',1,'7f640a4e-7b85-11ef-9c88-00090ffe0001'),('7f64d632-7b85-11ef-9c88-00090ffe0001',0,'7f640b1c-7b85-11ef-9c88-00090ffe0001'),('7f64d773-7b85-11ef-9c88-00090ffe0001',0,'7f640be6-7b85-11ef-9c88-00090ffe0001'),('7f64d89c-7b85-11ef-9c88-00090ffe0001',1,'7f640cc4-7b85-11ef-9c88-00090ffe0001');
/*!40000 ALTER TABLE `beverage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cafe`
--

DROP TABLE IF EXISTS `cafe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cafe` (
  `Id` char(36) NOT NULL DEFAULT (uuid()),
  `FoodSpotId` char(36) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FoodSpotId` (`FoodSpotId`),
  CONSTRAINT `cafe_ibfk_1` FOREIGN KEY (`FoodSpotId`) REFERENCES `foodspot` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cafe`
--

LOCK TABLES `cafe` WRITE;
/*!40000 ALTER TABLE `cafe` DISABLE KEYS */;
INSERT INTO `cafe` VALUES ('6094efc5-8d4e-11ef-9396-00090ffe0001','6092f4dc-8d4e-11ef-9396-00090ffe0001'),('60950a68-8d4e-11ef-9396-00090ffe0001','609312ad-8d4e-11ef-9396-00090ffe0001'),('60950c83-8d4e-11ef-9396-00090ffe0001','60931550-8d4e-11ef-9396-00090ffe0001');
/*!40000 ALTER TABLE `cafe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `Id` char(36) NOT NULL DEFAULT (uuid()),
  `UserId` char(36) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `UserId` (`UserId`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES ('71a66441-7b80-11ef-9c88-00090ffe0001','71a2f6d2-7b80-11ef-9c88-00090ffe0001'),('71a77d69-7b80-11ef-9c88-00090ffe0001','71a2fb34-7b80-11ef-9c88-00090ffe0001'),('fd3c88f0-8cd2-11ef-9396-00090ffe0001','fd3c60c6-8cd2-11ef-9396-00090ffe0001');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorites` (
  `Id` char(36) NOT NULL DEFAULT (uuid()),
  `FoodSpotId` char(36) NOT NULL,
  `CustomerId` char(36) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `CustomerId` (`CustomerId`),
  KEY `FoodSpotId` (`FoodSpotId`),
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`CustomerId`) REFERENCES `customer` (`Id`),
  CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`FoodSpotId`) REFERENCES `foodspot` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
INSERT INTO `favorites` VALUES ('5af9a2cb-8d5a-11ef-9396-00090ffe0001','6092f4dc-8d4e-11ef-9396-00090ffe0001','71a77d69-7b80-11ef-9c88-00090ffe0001'),('5af9ab2c-8d5a-11ef-9396-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','71a77d69-7b80-11ef-9c88-00090ffe0001');
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `foodspot`
--

DROP TABLE IF EXISTS `foodspot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `foodspot` (
  `Id` char(36) NOT NULL DEFAULT (uuid()),
  `AdminId` char(36) NOT NULL,
  `Name` varchar(60) NOT NULL,
  `Address` varchar(255) NOT NULL,
  `ImageUrl` varchar(255) NOT NULL,
  `PhoneNumber` varchar(20) NOT NULL,
  `OpeningTime` time NOT NULL,
  `ClosingTime` time NOT NULL,
  `Rating` decimal(2,1) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `AdminId` (`AdminId`),
  CONSTRAINT `foodspot_ibfk_1` FOREIGN KEY (`AdminId`) REFERENCES `admin` (`Id`),
  CONSTRAINT `foodspot_chk_1` CHECK ((`Rating` between 0 and 5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `foodspot`
--

LOCK TABLES `foodspot` WRITE;
/*!40000 ALTER TABLE `foodspot` DISABLE KEYS */;
INSERT INTO `foodspot` VALUES ('6092f4dc-8d4e-11ef-9396-00090ffe0001','71a486d2-7b80-11ef-9c88-00090ffe0001','Starbucks','123 Coffee Street, Seattle, WA','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbZAP2L_b7w-A-la9roq2CEoR34HwYzC72kg&s','+1 800 782 7282','07:00:00','22:00:00',4.5),('60930fa1-8d4e-11ef-9396-00090ffe0001','71a486d2-7b80-11ef-9c88-00090ffe0001','McDonald\'s','500 Fast Food Ave, Chicago, IL','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvjNtUaOL9re9l9qI2Ar6GFOlIuy_2n7f9Cw&s','+1 800 244 6227','06:00:00','23:00:00',4.0),('609311fe-8d4e-11ef-9396-00090ffe0001','71a486d2-7b80-11ef-9c88-00090ffe0001','Pizza Hut','789 Pizza Lane, Dallas, TX','https://www.gruender.de/wp-content/uploads/2023/04/Pizza-Hut-Gruender-scaled.jpeg','+1 800 948 8488','11:00:00','23:00:00',4.2),('609312ad-8d4e-11ef-9396-00090ffe0001','71a486d2-7b80-11ef-9c88-00090ffe0001','Café Nero','456 Coffee Blvd, Boston, MA','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTs3o7mS3TpSqCOVH-YkN7m0GiQx6Gra_9B4Q&s','+1 888 535 8330','08:00:00','20:00:00',4.3),('60931317-8d4e-11ef-9396-00090ffe0001','71a486d2-7b80-11ef-9c88-00090ffe0001','Chipotle','321 Burrito Drive, Denver, CO','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMqD4RLCyMBkdv6lVk463mnGGkg8lPPBlu_A&s','+1 800 342 1444','10:30:00','22:00:00',4.1),('60931550-8d4e-11ef-9396-00090ffe0001','71a486d2-7b80-11ef-9c88-00090ffe0001','Costa Coffee','654 Espresso Road, London, UK','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQ4pkHXGGnUyUM4S-qz1U56mRQC2qejFgTrw&s','+44 800 276 2211','07:00:00','21:00:00',4.7);
/*!40000 ALTER TABLE `foodspot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meal`
--

DROP TABLE IF EXISTS `meal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meal` (
  `Id` char(36) NOT NULL DEFAULT (uuid()),
  `IsVegan` tinyint(1) NOT NULL,
  `NutId` char(36) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `NutId` (`NutId`),
  CONSTRAINT `meal_ibfk_1` FOREIGN KEY (`NutId`) REFERENCES `nutritions` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meal`
--

LOCK TABLES `meal` WRITE;
/*!40000 ALTER TABLE `meal` DISABLE KEYS */;
INSERT INTO `meal` VALUES ('7f656a6c-7b85-11ef-9c88-00090ffe0001',0,'7f640db2-7b85-11ef-9c88-00090ffe0001'),('7f657047-7b85-11ef-9c88-00090ffe0001',1,'7f640ef7-7b85-11ef-9c88-00090ffe0001'),('7f65723a-7b85-11ef-9c88-00090ffe0001',0,'7f640feb-7b85-11ef-9c88-00090ffe0001'),('7f657375-7b85-11ef-9c88-00090ffe0001',0,'7f6410e4-7b85-11ef-9c88-00090ffe0001'),('7f6574a5-7b85-11ef-9c88-00090ffe0001',0,'7f6411b7-7b85-11ef-9c88-00090ffe0001'),('7f6575d7-7b85-11ef-9c88-00090ffe0001',1,'7f6414ce-7b85-11ef-9c88-00090ffe0001'),('7f657704-7b85-11ef-9c88-00090ffe0001',0,'7f641844-7b85-11ef-9c88-00090ffe0001'),('7f657825-7b85-11ef-9c88-00090ffe0001',0,'7f64195a-7b85-11ef-9c88-00090ffe0001'),('7f657945-7b85-11ef-9c88-00090ffe0001',0,'7f641a3e-7b85-11ef-9c88-00090ffe0001'),('7f657bcc-7b85-11ef-9c88-00090ffe0001',1,'7f641b16-7b85-11ef-9c88-00090ffe0001');
/*!40000 ALTER TABLE `meal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nutritions`
--

DROP TABLE IF EXISTS `nutritions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nutritions` (
  `Id` char(36) NOT NULL DEFAULT (uuid()),
  `FoodSpotId` char(36) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `ImageUrl` varchar(255) NOT NULL,
  `Price` decimal(5,2) NOT NULL,
  `Rating` decimal(2,1) DEFAULT NULL,
  `Description` text,
  PRIMARY KEY (`Id`),
  KEY `FoodSpotId` (`FoodSpotId`),
  CONSTRAINT `nutritions_ibfk_1` FOREIGN KEY (`FoodSpotId`) REFERENCES `foodspot` (`Id`),
  CONSTRAINT `nutritions_chk_1` CHECK ((`Rating` between 0 and 5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nutritions`
--

LOCK TABLES `nutritions` WRITE;
/*!40000 ALTER TABLE `nutritions` DISABLE KEYS */;
INSERT INTO `nutritions` VALUES ('7f633d51-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Cappuccino','http://example.com/images/cappuccino.jpg',3.99,4.9,'Rich and creamy coffee beverage'),('7f6403ae-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Latte','http://example.com/images/latte.jpg',4.29,4.8,'Smooth and flavorful latte with steamed milk'),('7f6405ab-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Americano','http://example.com/images/americano.jpg',2.99,4.7,'Bold and strong coffee with added water'),('7f640756-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Espresso','http://example.com/images/espresso.jpg',2.49,4.6,'Concentrated coffee with a rich flavor'),('7f640869-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Red Wine','http://example.com/images/redwine.jpg',8.99,4.5,'Elegant red wine with deep flavors'),('7f640979-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','White Wine','http://example.com/images/whitewine.jpg',7.99,4.4,'Refreshing white wine with crisp acidity'),('7f640a4e-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Beer','http://example.com/images/beer.jpg',5.99,4.3,'Cold and refreshing beer with a light bitterness'),('7f640b1c-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Orange Juice','http://example.com/images/orangejuice.jpg',3.49,4.9,'Freshly squeezed orange juice'),('7f640be6-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Iced Tea','http://example.com/images/icedtea.jpg',3.29,4.8,'Chilled tea with a hint of lemon'),('7f640cc4-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Whiskey','http://example.com/images/whiskey.jpg',9.99,4.7,'Smooth and smoky whiskey with a complex flavor'),('7f640db2-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Classic Burger','http://example.com/images/classicburger.jpg',9.99,4.7,'Juicy beef patty with fresh lettuce, tomatoes, and cheese'),('7f640ef7-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Vegan Burger','http://example.com/images/veganburger.jpg',8.99,4.8,'Plant-based patty with vegan cheese, lettuce, and tomatoes'),('7f640feb-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Grilled Chicken Sandwich','http://example.com/images/grilledchicken.jpg',7.99,4.6,'Grilled chicken breast with fresh lettuce and tomatoes'),('7f6410e4-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Caesar Salad','http://example.com/images/caesarsalad.jpg',6.49,4.5,'Crispy romaine lettuce, croutons, and parmesan cheese with Caesar dressing'),('7f6411b7-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Margherita Pizza','http://example.com/images/margheritapizza.jpg',12.99,4.9,'Classic Italian pizza with fresh mozzarella and basil'),('7f6414ce-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Vegan Salad','http://example.com/images/vegansalad.jpg',5.99,4.7,'Mixed greens, cucumbers, cherry tomatoes, and avocado with olive oil dressing'),('7f641844-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Spaghetti Carbonara','http://example.com/images/spaghetticarbonara.jpg',10.49,4.8,'Classic Italian pasta with pancetta, egg, and parmesan cheese'),('7f64195a-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Vegetarian Pizza','http://example.com/images/vegetarianpizza.jpg',11.99,4.6,'Pizza topped with bell peppers, mushrooms, olives, and onions'),('7f641a3e-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Fish and Chips','http://example.com/images/fishandchips.jpg',9.49,4.5,'Crispy fried fish served with golden fries'),('7f641b16-7b85-11ef-9c88-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001','Vegan Wrap','http://example.com/images/veganwrap.jpg',7.99,4.7,'Tortilla wrap with hummus, fresh vegetables, and falafel');
/*!40000 ALTER TABLE `nutritions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservation`
--

DROP TABLE IF EXISTS `reservation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservation` (
  `Id` char(36) NOT NULL DEFAULT (uuid()),
  `CustomerId` char(36) DEFAULT NULL,
  `RestaurantId` char(36) DEFAULT NULL,
  `NumberOfSeats` int DEFAULT NULL,
  `Date` date NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `CustomerId` (`CustomerId`),
  KEY `RestaurantId` (`RestaurantId`),
  CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`CustomerId`) REFERENCES `customer` (`Id`),
  CONSTRAINT `reservation_ibfk_2` FOREIGN KEY (`RestaurantId`) REFERENCES `restaurant` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservation`
--

LOCK TABLES `reservation` WRITE;
/*!40000 ALTER TABLE `reservation` DISABLE KEYS */;
/*!40000 ALTER TABLE `reservation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurant`
--

DROP TABLE IF EXISTS `restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurant` (
  `Id` char(36) NOT NULL DEFAULT (uuid()),
  `FoodSpotId` char(36) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FoodSpotId` (`FoodSpotId`),
  CONSTRAINT `restaurant_ibfk_1` FOREIGN KEY (`FoodSpotId`) REFERENCES `foodspot` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurant`
--

LOCK TABLES `restaurant` WRITE;
/*!40000 ALTER TABLE `restaurant` DISABLE KEYS */;
INSERT INTO `restaurant` VALUES ('60945bcf-8d4e-11ef-9396-00090ffe0001','60930fa1-8d4e-11ef-9396-00090ffe0001'),('60946e91-8d4e-11ef-9396-00090ffe0001','609311fe-8d4e-11ef-9396-00090ffe0001'),('60947085-8d4e-11ef-9396-00090ffe0001','60931317-8d4e-11ef-9396-00090ffe0001');
/*!40000 ALTER TABLE `restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `Id` char(36) NOT NULL DEFAULT (uuid()),
  `FirstName` varchar(40) NOT NULL,
  `LastName` varchar(40) NOT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Password` varchar(255) NOT NULL,
  `DateOfBirth` date NOT NULL,
  `PhoneNumber` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('61d4b4c7-8ccc-11ef-9396-00090ffe0001','John','Doe','mm.doe@example.com','securepassword','1990-01-01','123-456-7890'),('71a0a69e-7b80-11ef-9c88-00090ffe0001','John','Doe','john.doe@example.com','hashed_password_123','1990-05-21','+1234567890'),('71a2f6d2-7b80-11ef-9c88-00090ffe0001','Jane','Smith','jane.smith@example.com','hashed_password_456','1992-07-15','+1987654321'),('71a2fb34-7b80-11ef-9c88-00090ffe0001','Matin','Abaszada','matin.abaszada@time2dine.com','hashed_password_matin','2005-04-18','+4915732912345'),('fd3c60c6-8cd2-11ef-9396-00090ffe0001','Qabil','Majidovvv','044@gmail.com','adasdas','2006-06-06','0508252006');
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

-- Dump completed on 2024-10-18 16:45:42
