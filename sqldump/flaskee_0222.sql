-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: flaskee
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `t_category`
--

DROP TABLE IF EXISTS `t_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(255) NOT NULL,
  `category_available` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_category`
--

LOCK TABLES `t_category` WRITE;
/*!40000 ALTER TABLE `t_category` DISABLE KEYS */;
INSERT INTO `t_category` VALUES (1,'A',1),(2,'B',1),(3,'C',1),(4,'D',1),(5,'E',1),(6,'F',1);
/*!40000 ALTER TABLE `t_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_comment`
--

DROP TABLE IF EXISTS `t_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_comment` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `comment_content` text NOT NULL,
  `comment_author` varchar(255) NOT NULL,
  `comment_author_name` varchar(45) NOT NULL,
  `comment_target` int(11) NOT NULL,
  `comment_datetime` datetime NOT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `fk_t_comment_1_idx` (`comment_author`),
  KEY `fk_t_comment_2_idx` (`comment_target`),
  CONSTRAINT `fk_t_comment_1` FOREIGN KEY (`comment_target`) REFERENCES `t_item` (`item_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_comment`
--

LOCK TABLES `t_comment` WRITE;
/*!40000 ALTER TABLE `t_comment` DISABLE KEYS */;
INSERT INTO `t_comment` VALUES (1,'good','3','root',10,'2019-02-14 02:32:05'),(2,'asdf','3','root',10,'2019-02-14 02:32:19'),(3,'Exploit                                              Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.','3','root',10,'2019-02-14 03:14:41'),(4,'perfect!!!!','5','manager',9,'2019-02-14 06:38:15'),(5,'02151616','3','root',10,'2019-02-15 08:16:55'),(6,'hey yo!!','6','user1',19,'2019-02-18 07:01:13');
/*!40000 ALTER TABLE `t_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_item`
--

DROP TABLE IF EXISTS `t_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_item` (
  `item_id` int(11) NOT NULL AUTO_INCREMENT,
  `item_title` varchar(255) NOT NULL,
  `item_content` text NOT NULL,
  `item_category` int(11) NOT NULL,
  `item_datetime` datetime DEFAULT NULL,
  `item_author` int(11) NOT NULL,
  `item_read` tinyint(4) NOT NULL DEFAULT '0',
  `item_accept` tinyint(4) NOT NULL DEFAULT '0',
  `item_delete` tinyint(4) NOT NULL DEFAULT '0',
  `item_attachment` varchar(255) DEFAULT NULL,
  `item_stars` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`item_id`),
  KEY `fk_t_item_1_idx` (`item_author`),
  CONSTRAINT `fk_item_user` FOREIGN KEY (`item_author`) REFERENCES `t_user` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_item`
--

LOCK TABLES `t_item` WRITE;
/*!40000 ALTER TABLE `t_item` DISABLE KEYS */;
INSERT INTO `t_item` VALUES (1,'asdf','asdf',1,'2019-01-25 03:36:59',3,0,0,0,NULL,3),(2,'01251145','01251145',2,'2019-01-25 03:41:31',8,0,1,0,NULL,0),(3,'test0128','test0128\r\n',3,'2019-01-28 01:21:34',4,1,1,0,'asdfasdfasdf',0),(4,'test01281020','01281020',4,'2019-01-28 02:24:41',8,1,0,0,NULL,0),(5,'test01281020','01281020',5,'2019-01-28 02:25:02',3,0,1,0,NULL,0),(6,'01290920','01290920\r\n\r\nExploit Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.\r\n\r\nThese are not merely static graphs and tables so you can interact with the data in multiple ways. By using the sliders at the top, you can narrow down your view to a particular range of dates or you can select any of the items in the tables below to filter the data based on platform, port, or author. The various charts can also be interacted with to zoom in or out, select particular points, or draw a custom selection.\r\n\r\nTo change the view back to the default, you will find a ‘Reset’ button at the bottom left or you can choose to ‘Undo’ and ‘Redo’ your selections.\r\n\r\nExploit Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.\r\n\r\nThese are not merely static graphs and tables so you can interact with the data in multiple ways. By using the sliders at the top, you can narrow down your view to a particular range of dates or you can select any of the items in the tables below to filter the data based on platform, port, or author. The various charts can also be interacted with to zoom in or out, select particular points, or draw a custom selection.\r\n\r\nTo change the view back to the default, you will find a ‘Reset’ button at the bottom left or you can choose to ‘Undo’ and ‘Redo’ your selections.',6,'2019-01-29 01:31:41',7,0,1,0,NULL,0),(7,'host','Exploit Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.\r\n\r\nThese are not merely static graphs and tables so you can interact with the data in multiple ways. By using the sliders at the top, you can narrow down your view to a particular range of dates or you can select any of the items in the tables below to filter the data based on platform, port, or author. The various charts can also be interacted with to zoom in or out, select particular points, or draw a custom selection.\r\n\r\nTo change the view back to the default, you will find a ‘Reset’ button at the bottom left or you can choose to ‘Undo’ and ‘Redo’ your selections.\r\n\r\nExploit Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.\r\n\r\nThese are not merely static graphs and tables so you can interact with the data in multiple ways. By using the sliders at the top, you can narrow down your view to a particular range of dates or you can select any of the items in the tables below to filter the data based on platform, port, or author. The various charts can also be interacted with to zoom in or out, select particular points, or draw a custom selection.\r\n\r\nTo change the view back to the default, you will find a ‘Reset’ button at the bottom left or you can choose to ‘Undo’ and ‘Redo’ your selections.',2,'2019-02-01 06:36:18',3,1,1,0,NULL,0),(8,'test02011620','Exploit Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.\r\n\r\nThese are not merely static graphs and tables so you can interact with the data in multiple ways. By using the sliders at the top, you can narrow down your view to a particular range of dates or you can select any of the items in the tables below to filter the data based on platform, port, or author. The various charts can also be interacted with to zoom in or out, select particular points, or draw a custom selection.\r\n\r\nTo change the view back to the default, you will find a ‘Reset’ button at the bottom left or you can choose to ‘Undo’ and ‘Redo’ your selections.',2,'2019-02-01 08:30:48',3,1,0,0,'',0),(9,'test02011620','Exploit Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.\r\n\r\nThese are not merely static graphs and tables so you can interact with the data in multiple ways. By using the sliders at the top, you can narrow down your view to a particular range of dates or you can select any of the items in the tables below to filter the data based on platform, port, or author. The various charts can also be interacted with to zoom in or out, select particular points, or draw a custom selection.\r\n\r\nTo change the view back to the default, you will find a ‘Reset’ button at the bottom left or you can choose to ‘Undo’ and ‘Redo’ your selections.',6,'2019-02-01 08:31:25',3,1,0,0,'flasky-master.zip',0),(10,'test02011640','Exploit                                              Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.\r\n\r\nThese are not merely static graphs and tables so you can interact with the data in multiple ways. By using the sliders at the top, you can narrow down your view to a particular range of dates or you can select any of the items in the tables below to filter the data based on platform, port, or author. The various charts can also be interacted with to zoom in or out, select particular points, or draw a custom selection.\r\n\r\nTo change the view back to the default, you will find a ‘Reset’ button at the bottom left or you can choose to ‘Undo’ and ‘Redo’ your selections.\r\n\r\nasdfasdfasdfasdf',1,'2019-02-01 08:34:51',3,0,1,0,'美团-机器学习-实践_最新AI算法实践真知.pdf.zip',0),(11,'02151650','02151650',3,'2019-02-15 08:54:40',5,1,0,0,NULL,0),(12,'02151700','02151700',1,'2019-02-15 09:08:00',5,1,0,0,NULL,0),(13,'02151701','02151701',5,'2019-02-15 09:09:48',5,1,0,0,NULL,0),(14,'02151702','02151702',2,'2019-02-15 09:10:41',5,1,0,0,NULL,0),(15,'02180807','02180807',4,'2019-02-18 00:08:00',3,0,0,0,NULL,0),(16,'02180814','02180814',1,'2019-02-18 00:14:38',3,0,0,0,NULL,0),(17,'02180823','02180823',3,'2019-02-18 00:23:35',3,1,1,0,NULL,0),(18,'02180829','02180829\r\n\r\n123\r\n',2,'2019-02-18 00:29:09',3,1,1,0,NULL,0),(19,'02180934','02180934',3,'2019-02-18 01:34:55',3,1,0,0,'celery.pdf',0),(20,'test02181451','Exploit                                              Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.\r\n\r\nThese are not merely static graphs and tables so you can interact with the data in multiple ways. By using the sliders at the top, you can narrow down your view to a particular range of dates or you can select any of the items in the tables below to filter the data based on platform, port, or author. The various charts can also be interacted with to zoom in or out, select particular points, or draw a custom selection.\r\n\r\nTo change the view back to the default, you will find a ‘Reset’ button at the bottom left or you can choose to ‘Undo’ and ‘Redo’ your selections.\r\n\r\nasdfasdfasdfasdf\r\n\r\n\r\nExploit                                              Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.\r\n\r\nThese are not merely static graphs and tables so you can interact with the data in multiple ways. By using the sliders at the top, you can narrow down your view to a particular range of dates or you can select any of the items in the tables below to filter the data based on platform, port, or author. The various charts can also be interacted with to zoom in or out, select particular points, or draw a custom selection.\r\n\r\nTo change the view back to the default, you will find a ‘Reset’ button at the bottom left or you can choose to ‘Undo’ and ‘Redo’ your selections.\r\n\r\nasdfasdfasdfasdf\r\n\r\n',1,'2019-02-18 06:51:21',6,0,0,0,NULL,0),(21,'test02181455','Exploit                                              Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.\r\n\r\nThese are not merely static graphs and tables so you can interact with the data in multiple ways. By using the sliders at the top, you can narrow down your view to a particular range of dates or you can select any of the items in the tables below to filter the data based on platform, port, or author. The various charts can also be interacted with to zoom in or out, select particular points, or draw a custom selection.\r\n\r\nTo change the view back to the default, you will find a ‘Reset’ button at the bottom left or you can choose to ‘Undo’ and ‘Redo’ your selections.\r\n\r\nasdfasdfasdfasdf\r\n\r\nExploit                                              Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.\r\n\r\nThese are not merely static graphs and tables so you can interact with the data in multiple ways. By using the sliders at the top, you can narrow down your view to a particular range of dates or you can select any of the items in the tables below to filter the data based on platform, port, or author. The various charts can also be interacted with to zoom in or out, select particular points, or draw a custom selection.\r\n\r\nTo change the view back to the default, you will find a ‘Reset’ button at the bottom left or you can choose to ‘Undo’ and ‘Redo’ your selections.\r\n\r\nasdfasdfasdfasdf\r\n\r\nExploit                                              Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.\r\n\r\nThese are not merely static graphs and tables so you can interact with the data in multiple ways. By using the sliders at the top, you can narrow down your view to a particular range of dates or you can select any of the items in the tables below to filter the data based on platform, port, or author. The various charts can also be interacted with to zoom in or out, select particular points, or draw a custom selection.\r\n\r\nTo change the view back to the default, you will find a ‘Reset’ button at the bottom left or you can choose to ‘Undo’ and ‘Redo’ your selections.\r\n\r\nasdfasdfasdfasdf\r\n\r\nExploit                                              Database Statistics\r\nThe following graphs and statistics provide you with a glimpse of the entries that have been added to the Exploit Database over the years. They will be re-generated, at minimum, on a monthly basis and will help you visualize how the exploit landscape is changing over time.\r\n\r\nThese are not merely static graphs and tables so you can interact with the data in multiple ways. By using the sliders at the top, you can narrow down your view to a particular range of dates or you can select any of the items in the tables below to filter the data based on platform, port, or author. The various charts can also be interacted with to zoom in or out, select particular points, or draw a custom selection.\r\n\r\nTo change the view back to the default, you will find a ‘Reset’ button at the bottom left or you can choose to ‘Undo’ and ‘Redo’ your selections.\r\n\r\nasdfasdfasdfasdf\r\n\r\n',2,'2019-02-18 06:51:53',6,0,0,0,NULL,0),(22,'test02181456',' or current_user.user_role == 3 or current_user.user_role == 3 or current_user.user_role == 3 or current_user.user_role == 3 or current_user.user_role == 3\r\n\r\n or current_user.user_role == 3\r\n\r\n\r\n\r\n\r\n or current_user.user_role == 3 or current_user.user_role == 3 or current_user.user_role == 3\r\n\r\n\r\n\r\n or current_user.user_role == 3',3,'2019-02-18 06:54:43',6,1,0,0,NULL,0),(23,'02211117','02211117',1,'2019-02-21 03:17:24',3,0,0,0,NULL,0),(24,'02211120','02211120',4,'2019-02-21 03:19:42',3,0,0,0,NULL,0),(25,'02211637','02211673',3,'2019-02-21 08:37:15',3,0,0,0,NULL,0),(26,'02221533','02221533',3,'2019-02-22 07:29:57',3,0,0,0,NULL,0),(27,'02221540','02221540',1,'2019-02-22 07:39:55',3,0,0,0,NULL,0);
/*!40000 ALTER TABLE `t_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_notification`
--

DROP TABLE IF EXISTS `t_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_notification` (
  `notification_id` int(11) NOT NULL AUTO_INCREMENT,
  `notification_content` text NOT NULL,
  `notification_author` int(11) NOT NULL,
  `notification_reader` int(11) NOT NULL,
  `notification_target` text,
  `notification_datetime` datetime NOT NULL,
  `notification_read` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`notification_id`),
  KEY `fk_t_notification_1_idx` (`notification_author`),
  KEY `fk_t_notification_2_idx` (`notification_reader`),
  CONSTRAINT `fk_t_notification_1` FOREIGN KEY (`notification_author`) REFERENCES `t_user` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_notification_2` FOREIGN KEY (`notification_reader`) REFERENCES `t_user` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_notification`
--

LOCK TABLES `t_notification` WRITE;
/*!40000 ALTER TABLE `t_notification` DISABLE KEYS */;
INSERT INTO `t_notification` VALUES (1,' submited a new item.',3,10,'/post/6','2019-02-15 03:32:38',0),(2,' submited a new item.',3,9,'/post/6','2019-02-15 03:32:38',0),(3,' submited a new item.',3,8,'/post/6','2019-02-15 03:32:38',0),(4,' submited a new item.',3,7,'/post/6','2019-02-15 03:32:38',0),(5,' submited a new item.',3,6,'/post/6','2019-02-15 03:32:38',1),(6,' submited a new item.',3,5,'/post/6','2019-02-15 03:32:38',1),(7,' submited a new item.',3,3,'/post/6','2019-02-15 03:32:38',1),(8,'root post a new broadcast.',3,10,'/post/7','2019-02-15 03:37:27',0),(9,'root post a new broadcast.',3,9,'/post/7','2019-02-15 03:37:27',0),(10,'root post a new broadcast.',3,8,'/post/7','2019-02-15 03:37:27',0),(11,'root post a new broadcast.',3,7,'/post/7','2019-02-15 03:37:27',0),(12,'root post a new broadcast.',3,6,'/post/7','2019-02-15 03:37:27',0),(13,'root post a new broadcast.',3,5,'/post/7','2019-02-15 03:37:27',1),(14,'root post a new broadcast.',3,3,'/post/7','2019-02-15 03:37:27',1),(15,'root submited a new item.',3,5,'/item/18','2019-02-18 00:29:09',1),(16,'manager accepted your item.',5,3,'/item/17','2019-02-18 00:33:37',1),(17,'manager accepted your item.',5,3,'/item/18','2019-02-18 00:37:39',1),(18,'root modified an item',3,5,'/item/18','2019-02-18 00:45:10',1),(19,'manager modified your item.',5,3,'/item/18','2019-02-18 00:45:35',1),(20,'root post a new broadcast.',3,5,'/item/1','2019-02-18 00:55:48',0),(21,'user3 post a new broadcast.',8,5,'/item/2','2019-02-18 00:55:48',0),(22,'root post a new broadcast.',3,5,'/item/5','2019-02-18 00:55:48',0),(23,'user2 post a new broadcast.',7,5,'/item/6','2019-02-18 00:55:48',0),(24,'root post a new broadcast.',3,5,'/item/10','2019-02-18 00:55:48',0),(25,'manager post a new broadcast.',5,5,'/item/12','2019-02-18 00:55:48',1),(26,'root post a new broadcast.',3,5,'/item/15','2019-02-18 00:55:48',0),(27,'root post a new broadcast.',3,5,'/item/16','2019-02-18 00:55:48',0),(28,'root post a new broadcast.',3,5,'/item/1','2019-02-18 00:55:50',0),(29,'user3 post a new broadcast.',8,5,'/item/2','2019-02-18 00:55:50',0),(30,'root post a new broadcast.',3,5,'/item/5','2019-02-18 00:55:50',0),(31,'user2 post a new broadcast.',7,5,'/item/6','2019-02-18 00:55:50',0),(32,'root post a new broadcast.',3,5,'/item/10','2019-02-18 00:55:50',0),(33,'manager post a new broadcast.',5,5,'/item/12','2019-02-18 00:55:50',0),(34,'root post a new broadcast.',3,5,'/item/15','2019-02-18 00:55:50',0),(35,'root post a new broadcast.',3,5,'/item/16','2019-02-18 00:55:50',0),(36,'root submited a new item.',3,5,'/item/19','2019-02-18 01:34:55',0),(37,'root post a new broadcast.',3,10,'/post/8','2019-02-18 01:59:21',0),(38,'root post a new broadcast.',3,9,'/post/8','2019-02-18 01:59:21',0),(39,'root post a new broadcast.',3,8,'/post/8','2019-02-18 01:59:21',0),(40,'root post a new broadcast.',3,7,'/post/8','2019-02-18 01:59:21',0),(41,'root post a new broadcast.',3,6,'/post/8','2019-02-18 01:59:21',0),(42,'root post a new broadcast.',3,5,'/post/8','2019-02-18 01:59:21',0),(43,'root post a new broadcast.',3,3,'/post/8','2019-02-18 01:59:21',0),(44,'user1 submited a new item.',6,5,'/item/20','2019-02-18 06:51:21',0),(45,'user1 submited a new item.',6,5,'/item/21','2019-02-18 06:51:53',0),(46,'user1 submited a new item.',6,5,'/item/22','2019-02-18 06:54:43',0),(47,'manager post a new broadcast.',5,10,'/post/9','2019-02-18 07:25:10',0),(48,'manager post a new broadcast.',5,9,'/post/9','2019-02-18 07:25:10',0),(49,'manager post a new broadcast.',5,8,'/post/9','2019-02-18 07:25:10',0),(50,'manager post a new broadcast.',5,7,'/post/9','2019-02-18 07:25:10',0),(51,'manager post a new broadcast.',5,6,'/post/9','2019-02-18 07:25:10',0),(52,'manager post a new broadcast.',5,5,'/post/9','2019-02-18 07:25:10',0),(53,'manager post a new broadcast.',5,3,'/post/9','2019-02-18 07:25:10',0),(54,'manager post a new broadcast.',5,10,'/post/10','2019-02-18 07:34:50',0),(55,'manager post a new broadcast.',5,9,'/post/10','2019-02-18 07:34:50',0),(56,'manager post a new broadcast.',5,8,'/post/10','2019-02-18 07:34:50',0),(57,'manager post a new broadcast.',5,7,'/post/10','2019-02-18 07:34:50',0),(58,'manager post a new broadcast.',5,6,'/post/10','2019-02-18 07:34:50',0),(59,'manager post a new broadcast.',5,5,'/post/10','2019-02-18 07:34:50',0),(60,'manager post a new broadcast.',5,3,'/post/10','2019-02-18 07:34:50',0),(61,'root submited a new item.',3,5,'/item/23','2019-02-21 03:17:24',0),(62,'root submited a new item.',3,5,'/item/24','2019-02-21 03:19:42',0),(63,'root submited a new item.',3,5,'/item/25','2019-02-21 08:37:15',0),(64,'root submited a new item.',3,5,'/item/26','2019-02-22 07:29:57',0),(65,'root submited a new item.',3,5,'/item/27','2019-02-22 07:39:55',0);
/*!40000 ALTER TABLE `t_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_post`
--

DROP TABLE IF EXISTS `t_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_post` (
  `post_id` int(11) NOT NULL AUTO_INCREMENT,
  `post_title` text NOT NULL,
  `post_content` text NOT NULL,
  `post_author` int(11) NOT NULL,
  `post_datetime` datetime NOT NULL,
  `post_delete` int(11) NOT NULL DEFAULT '0',
  `post_attachment` text,
  PRIMARY KEY (`post_id`),
  KEY `fk_t_post_1_idx` (`post_author`),
  CONSTRAINT `fk_t_post_1` FOREIGN KEY (`post_author`) REFERENCES `t_user` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_post`
--

LOCK TABLES `t_post` WRITE;
/*!40000 ALTER TABLE `t_post` DISABLE KEYS */;
INSERT INTO `t_post` VALUES (1,'test02011620','123',3,'2019-02-14 08:41:18',0,NULL),(2,'test02011620','123',3,'2019-02-14 08:42:35',0,NULL),(3,'02150813','asd02150813',3,'2019-02-15 00:13:11',0,NULL),(4,'02151129','02151129',3,'2019-02-15 03:29:36',0,NULL),(5,'02151131','02151131',3,'2019-02-15 03:31:54',0,NULL),(6,'02151131','02151131',3,'2019-02-15 03:32:38',0,NULL),(7,'02151140','02151140',3,'2019-02-15 03:37:27',0,NULL),(8,'02180959','02180959',3,'2019-02-18 01:59:21',0,'celery.pdf'),(9,'test02181525','posts = Post.query.order_by(Post.post_datetime.desc()).all()\r\n    return render_template(\'/post/post_manage.html\',posts=posts)\r\nposts = Post.query.order_by(Post.post_datetime.desc()).all()\r\n    return render_template(\'/post/post_manage.html\',posts=posts)',5,'2019-02-18 07:25:10',0,NULL),(10,'2019.02.18 发布','2019.02.18 发布',5,'2019-02-18 07:34:50',0,'路由器分析基础要点1.pdf');
/*!40000 ALTER TABLE `t_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user`
--

DROP TABLE IF EXISTS `t_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) NOT NULL,
  `user_password` varchar(128) NOT NULL,
  `user_available` int(11) NOT NULL DEFAULT '1',
  `user_department` int(11) NOT NULL,
  `user_role` int(11) NOT NULL,
  `user_regtime` datetime DEFAULT NULL,
  `user_lastlogtime` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user`
--

LOCK TABLES `t_user` WRITE;
/*!40000 ALTER TABLE `t_user` DISABLE KEYS */;
INSERT INTO `t_user` VALUES (1,'admin','admin',0,0,0,'2019-01-24 09:11:24',NULL),(2,'admin1','pbkdf2:sha256:50000$2IeoRkKR$4eb2fc7e4006e9b1d86d61ceb04cb34936e2912e1486224e315709824c47f886',0,0,0,'2019-01-24 09:15:01',NULL),(3,'root','pbkdf2:sha256:50000$OkxFKXqU$cedb3d9eed3a4e5c152b5dbc1e8c75c3fb3b9f13944c680b74f707b928777b20',1,0,3,'2019-01-24 09:18:35','2019-01-28 01:19:33'),(4,'root1','pbkdf2:sha256:50000$1wrjb312$a2a776b20c74558c3b8e02ef2c2f7ad0c29b17f107aacc64a8f778b233ab795a',0,0,1,'2019-01-25 01:25:22',NULL),(5,'manager','pbkdf2:sha256:50000$ELl8nTcZ$80f54d1088decff5546feb03ece4da132d66d7116f1176cce89c782d512818b8',1,0,2,'2019-02-03 00:41:40',NULL),(6,'user1','pbkdf2:sha256:50000$TEJwOwKw$40cd94e58a45058e731b5b477082dc248ee75ddbbbd77b63413ac84331fda2aa',1,0,1,'2019-02-11 00:41:12',NULL),(7,'user2','pbkdf2:sha256:50000$0aHfQAE1$d7039353893508d35603e24f82e4e88d69a75e5d7ef2fb69d187284b5f55d529',1,0,1,'2019-02-11 00:41:22',NULL),(8,'user3','pbkdf2:sha256:50000$icFAe2mW$5716f13ab95311e22dda1f7ec3dafa6e681c33b403a6c38b05211eb092609ff8',1,0,1,'2019-02-11 00:41:32',NULL),(9,'user4','pbkdf2:sha256:50000$pKZjIhLj$921d97f5114afa8a9f832d5a76cea3333c85981266fae6f3ad626839b0bc7f58',1,0,1,'2019-02-11 00:41:44',NULL),(10,'user5','pbkdf2:sha256:50000$9zkrDeHh$4e7e053234ff73877b87c33fb2e0507f9e9ff886c34054e046232b7918b181a6',1,0,1,'2019-02-11 02:52:08',NULL);
/*!40000 ALTER TABLE `t_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-22  5:16:46
