-- MySQL dump 10.14  Distrib 5.5.68-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: db_crm
-- ------------------------------------------------------
-- Server version	5.5.68-MariaDB

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('ekum2mhlwk6uz6qnu9i6vt8rpnli82i7','.eJzVW11vqzgQ_S887WpbBUMAU612_8K-b1cRYEdFTZOIj1bVVf_72hCMBzxAU1rIS9Tc9g7nnJkzntjOL6vMebZLj_uT9fDLSpn14NxZxzR5PkYv3HqwHsuQMPJY0pA5j6UXOsFjGbg0tj7urDPPXtI8T0_HXZkddoc0L3bP_F0GyuIoechOB179axPa395ZRVoc6sB1SOoEMrBDRGBKfWrdWSKY-IONjLGRMTYyxkb84iyDHMvDQfy4uwRq3tZ4m3dVCPlGwGyxRIwpKJ4OxWf7WIKIbB2WCYoIoZBIOgrHEKEGXVcWhbRPFuDmLG019HXgwZ744jH7kIwBlzE2v_39z5_n578eH9kfv_88DcYPikWgs_AcRwgf-v52jIUIsRyJF34sYT1TUM8uS8TDXM8bqGcZY456rrDo9Ryi9axgmaCAeqYdDTFCUMNWlq6GGlmAW6_nwEbreRD4QD3_FA2tngOC1vMgC7yef4BEzpPTke26pRQ4WCltORUgAh4FA7zqqG11SXrVI1K2MEdQdi5Wdp8muWwl6gT1gtxiBflpfovWqDZj6CWKrt5-sHUlU8_uMGoDqarUpVukODVyoDbRJX4Ku2XLUaOkVyO63E9htGgBvpSHIt21aHLFCSz-vhOEclZO9uLnbcKEz_ZeMsCviquxzL86EHRxAv1DDOukXPSxoikJOimZpEsnPT3Fe2nqa9fIwETysjQuC27KGQXDRotB6mD7EueWdbi3AedJVl5E2fPDG493efJ0Oh3AQEnhGBH7ApNPHWIeKKtQGxFqU4f64lzZQ6Y1XIrOBC3IAWD6lCk56hWCslRVYZZMKwpECBMnvc9SdAaYRApvtMtS1HxP0SlgEkPU5QsRZPwcZYVo0gV0DZgGQptT8erJ12HXtOFmc46GUHePj7mnBTsCEDjIg-qjjA3qdyU0ZqAnDMYRuCnA3DSZ5ICjVkNZdxfF3DWZMe6wZQnLXUG5KQh9BqYIb-tJLIwj2x3to5pgs7lModM8FtroCqWADoIDDgs7_Q3jalAfSmfUviOImZvurZCgK9U0cgPOWgFVzVOhg65Y05jijloB0YznvNid39qqBSOIGJOZTK_PO_DiRCQ8oLZxsVZPrqJvzlGev50ytjoVklOZ5fBAIIQHAvFeEA8iOx7rKHWo2frJBZneTfDjAQVyAJjeS8LuzjTG0qC4LplRbyCEiRPoIvjRwRRSeA9ZlqLePfBjhSkM0d6xFMGD8HJ1rAZMA8aOwOWs2c4bMU0TbT7fKHy6ddCTiBbqMDzgns5-AkrXpDyUzyx-RxSEn24jYqNHFlMZDlhpHXw1TxEbPduYShf31aJsy7w4vfBsdy5jYDBiwyGE-NWGlR3KlThy5KaWO-62S_SNiD6f4XTImueI7aLTrxH9KGLdg5UeYGiYoogpZT3FzVnrS4erAJ25Refk62TAjbpqUYB9PXSivk4T1M2rliTjiRiKd68pf2ul8af4nDK2l2XEYrnwx9JTe8_4IQQAqh94a0pl6WunF8JtnTAhX-mFIvw3NEMJGnRDio4gRvzjmGE7DDqr1hRRBpOnVB_JXivfgBKwI4borHKlFEMtcd3C6F2R2OhQc6UuA21xdbKcjnl5KC4tEdidkCl2_0RL1B9VY5EiKSq9c_e1q6X3GYKeis0tXHNl4XZ1A12JoCdvcwunulVfuZs0K-hh6One3Co2ve1mRTxH7_Kow9jxwHy85YxKndxwTCEQ8jY7G1QFdDb0xPJagW6xg0F9kieePHdqB-43xpHES116vUzVQ-a7yFGUrHtaTgg8tqyO7gOP7EcvmdTBZgcHVwZ0Xm2BDoEbmE5JZ7MJZW66tKALaSwmqE7nXsYp46bW49j9TNQXkcau-6iAbeNpIPZ9tQriendxCLpbpTQY460uca6Pdr2hb0y4g513-Y7nCliuT8ZX5ja6tuzInc6-CIuezJgyj-5TXimAWlbWyx_0NwfdobxSgHbAhQqs6hxLl0OfYB10b_JKNURwXvCb0iMqCn5k0THhrSxwX9IhTLyGiQTlyoJpxRn3h4qOiXLhcUGzpIPgVwqrW9qXrxNS-WK-uBtUQ1ewrVaMVHxsEX-xj-6rOeo-SbNE_J87K3lKDyzj4pf_zvFVxI-7Ob4A1kSZ_yZ5E3nG-84f_4n0eJ081Bc-XTdC81Ae01ee5WnxbsrCLPedG7KzXCZRwWY6ZG_izTR1V1kIYBbqswPP3VM8C6If5MYEzHV1VlXcPHcEK55-h6f2ERDh-RQdWf4UPfP7k4ntdx3sqiR_12FJW0Xf-oFTqP7x8T-O2ECG:1ks9Q4:MvFSF4NIZWeZx5r_o1nTdypi5R93qz73SF2P56dg9N4','2021-01-06 19:03:32.321342');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rbac_menu`
--

DROP TABLE IF EXISTS `rbac_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rbac_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  `icon` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rbac_menu`
--

LOCK TABLES `rbac_menu` WRITE;
/*!40000 ALTER TABLE `rbac_menu` DISABLE KEYS */;
INSERT INTO `rbac_menu` VALUES (5,'校区管理','fa-university'),(6,'客户管理','fa-handshake-o'),(7,'公司管理','fa-users'),(8,'权限管理','fa-check-circle');
/*!40000 ALTER TABLE `rbac_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rbac_permission`
--

DROP TABLE IF EXISTS `rbac_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rbac_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  `url` varchar(128) NOT NULL,
  `name` varchar(64) DEFAULT NULL,
  `menu_id` int(11) DEFAULT NULL,
  `pid_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `rbac_permission_menu_id_3dcc68be_fk_rbac_menu_id` (`menu_id`),
  KEY `rbac_permission_pid_id_6939354d_fk_rbac_permission_id` (`pid_id`),
  CONSTRAINT `rbac_permission_pid_id_6939354d_fk_rbac_permission_id` FOREIGN KEY (`pid_id`) REFERENCES `rbac_permission` (`id`),
  CONSTRAINT `rbac_permission_menu_id_3dcc68be_fk_rbac_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `rbac_menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rbac_permission`
--

LOCK TABLES `rbac_permission` WRITE;
/*!40000 ALTER TABLE `rbac_permission` DISABLE KEYS */;
INSERT INTO `rbac_permission` VALUES (64,'角色列表','/rbac/role/list/','rbac:role_list',8,NULL),(65,'添加角色','/rbac/role/add/','rbac:role_add',NULL,64),(66,'编辑角色','/rbac/role/edit/(?P<pk>\\d+)/','rbac:role_edit',NULL,64),(67,'删除角色','/rbac/role/del/(?P<pk>\\d+)/','rbac:role_del',NULL,64),(68,'菜单列表','/rbac/menu/list/','rbac:menu_list',8,NULL),(69,'添加菜单','/rbac/menu/add/','rbac:menu_add',NULL,68),(70,'编辑菜单','/rbac/menu/edit/(?P<pk>\\d+)/','rbac:menu_edit',NULL,68),(71,'删除菜单','/rbac/menu/del/(?P<pk>\\d+)/','rbac:menu_del',NULL,68),(72,'添加二级菜单','/rbac/second/menu/add/(?P<menu_id>\\d+)/','rbac:second_menu_add',NULL,68),(73,'编辑二级菜单','/rbac/second/menu/edit/(?P<pk>\\d+)/','rbac:second_menu_edit',NULL,68),(74,'删除二级菜单','/rbac/second/menu/del/(?P<pk>\\d+)/','rbac:second_menu_del',NULL,68),(75,'添加权限','/rbac/permission/add/(?P<second_menu_id>\\d+)/','rbac:permission_add',NULL,68),(76,'编辑权限','/rbac/permission/edit/(?P<pk>\\d+)/','rbac:permission_edit',NULL,68),(77,'删除权限','/rbac/permission/del/(?P<pk>\\d+)/','rbac:permission_del',NULL,68),(78,'批量操作权限','/rbac/multi/permissions/','rbac:multi_permissions',8,NULL),(79,'批量删除权限','/rbac/multi/permissions/del/(?P<pk>\\d+)/','rbac:multi_permissions_del',NULL,78),(80,'权限分配','/rbac/distribute/permissions/','rbac:distribute_permissions',8,NULL),(81,'学校列表','/stark/web/school/list/','stark:web_school_list',5,NULL),(82,'添加学校','/stark/web/school/add/','stark:web_school_add',NULL,81),(83,'编辑学校','/stark/web/school/edit/(?P<pk>\\d+)/','stark:web_school_edit',NULL,81),(84,'删除学校','/stark/web/school/del/(?P<pk>\\d+)/','stark:web_school_del',NULL,81),(85,'部门列表','/stark/web/department/list/','stark:web_department_list',7,NULL),(86,'添加部门','/stark/web/department/add/','stark:web_department_add',NULL,85),(87,'编辑部门','/stark/web/department/edit/(?P<pk>\\d+)/','stark:web_department_edit',NULL,85),(88,'删除部门','/stark/web/department/del/(?P<pk>\\d+)/','stark:web_department_del',NULL,85),(89,'员工列表','/stark/web/userinfo/list/','stark:web_userinfo_list',7,NULL),(90,'添加员工','/stark/web/userinfo/add/','stark:web_userinfo_add',NULL,89),(91,'编辑员工','/stark/web/userinfo/edit/(?P<pk>\\d+)/','stark:web_userinfo_edit',NULL,89),(92,'删除员工','/stark/web/userinfo/del/(?P<pk>\\d+)/','stark:web_userinfo_del',NULL,89),(93,'重置员工密码','/stark/web/userinfo/reset/password/(?P<pk>\\d+)/','stark:web_userinfo_reset_pwd',NULL,89),(94,'课程列表','/stark/web/course/list/','stark:web_course_list',5,NULL),(95,'添加课程','/stark/web/course/add/','stark:web_course_add',NULL,94),(96,'编辑课程','/stark/web/course/edit/(?P<pk>\\d+)/','stark:web_course_edit',NULL,94),(97,'删除课程','/stark/web/course/del/(?P<pk>\\d+)/','stark:web_course_del',NULL,94),(98,'班级列表','/stark/web/classlist/list/','stark:web_classlist_list',5,NULL),(99,'添加班级','/stark/web/classlist/add/','stark:web_classlist_add',NULL,98),(100,'编辑班级','/stark/web/classlist/edit/(?P<pk>\\d+)/','stark:web_classlist_edit',NULL,98),(101,'删除班级','/stark/web/classlist/del/(?P<pk>\\d+)/','stark:web_classlist_del',NULL,98),(102,'公有客户列表','/stark/web/customer/pub/list/','stark:web_customer_pub_list',6,NULL),(103,'添加公有客户','/stark/web/customer/pub/add/','stark:web_customer_pub_add',NULL,102),(104,'编辑公有客户','/stark/web/customer/pub/edit/(?P<pk>\\d+)/','stark:web_customer_pub_edit',NULL,102),(105,'删除公有客户','/stark/web/customer/pub/del/(?P<pk>\\d+)/','stark:web_customer_pub_del',NULL,102),(106,'公有客户跟进记录','/stark/web/customer/pub/record/(?P<pk>\\d+)/','stark:web_customer_pub_record_view',NULL,102),(107,'私有客户列表','/stark/web/customer/priv/list/','stark:web_customer_priv_list',6,NULL),(108,'添加私有客户','/stark/web/customer/priv/add/','stark:web_customer_priv_add',NULL,107),(109,'编辑私有客户','/stark/web/customer/priv/edit/(?P<pk>\\d+)/','stark:web_customer_priv_edit',NULL,107),(110,'删除私有客户','/stark/web/customer/priv/del/(?P<pk>\\d+)/','stark:web_customer_priv_del',NULL,107),(111,'私有客户跟进记录','/stark/web/consultrecord/list/(?P<customer_id>\\d+)/','stark:web_consultrecord_list',NULL,107),(112,'添加私有客户跟进记录','/stark/web/consultrecord/add/(?P<customer_id>\\d+)/','stark:web_consultrecord_add',NULL,107),(113,'编辑私有客户跟进记录','/stark/web/consultrecord/edit/(?P<customer_id>\\d+)/(?P<pk>\\d+)/','stark:web_consultrecord_edit',NULL,107),(114,'删除私有客户跟进记录','/stark/web/consultrecord/del/(?P<customer_id>\\d+)/(?P<pk>\\d+)/','stark:web_consultrecord_del',NULL,107),(115,'付费记录','/stark/web/paymentrecord/list/(?P<customer_id>\\d+)/','stark:web_paymentrecord_list',NULL,107),(116,'添加付费记录','/stark/web/paymentrecord/add/(?P<customer_id>\\d+)/','stark:web_paymentrecord_add',NULL,107),(117,'审核付费记录','/stark/web/paymentrecord/check/list/','stark:web_paymentrecord_check_list',6,NULL),(118,'学生列表','/stark/web/student/list/','stark:web_student_list',5,NULL),(119,'编辑学生','/stark/web/student/edit/(?P<pk>\\d+)/','stark:web_student_edit',NULL,118),(120,'学分列表','/stark/web/scorerecord/list/(?P<student_id>\\d+)/','stark:web_scorerecord_list',NULL,118),(121,'添加学分','/stark/web/scorerecord/add/(?P<student_id>\\d+)/','stark:web_scorerecord_add',NULL,118),(122,'课程打卡记录','/stark/web/courserecord/list/(?P<class_id>\\d+)/','stark:web_courserecord_list',NULL,94),(123,'添加打卡记录','/stark/web/courserecord/add/(?P<class_id>\\d+)/','stark:web_courserecord_add',NULL,94),(124,'编辑打卡记录','/stark/web/courserecord/edit/(?P<class_id>\\d+)/(?P<pk>\\d+)/','stark:web_courserecord_edit',NULL,94),(125,'删除打卡记录','/stark/web/courserecord/delete/(?P<class_id>\\d+)/(?P<pk>\\d+)/','stark:web_courserecord_del',NULL,94),(126,'初始化打卡','/stark/web/courserecord/attendance/(?P<class_id>\\d+)/(?P<course_record_id>\\d+)/','stark:web_courserecord_attendance',NULL,94);
/*!40000 ALTER TABLE `rbac_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rbac_role`
--

DROP TABLE IF EXISTS `rbac_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rbac_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rbac_role`
--

LOCK TABLES `rbac_role` WRITE;
/*!40000 ALTER TABLE `rbac_role` DISABLE KEYS */;
INSERT INTO `rbac_role` VALUES (7,'CEO');
/*!40000 ALTER TABLE `rbac_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rbac_role_permissions`
--

DROP TABLE IF EXISTS `rbac_role_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rbac_role_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rbac_role_permissions_role_id_permission_id_d01303da_uniq` (`role_id`,`permission_id`),
  KEY `rbac_role_permission_permission_id_f5e1e866_fk_rbac_perm` (`permission_id`),
  CONSTRAINT `rbac_role_permission_permission_id_f5e1e866_fk_rbac_perm` FOREIGN KEY (`permission_id`) REFERENCES `rbac_permission` (`id`),
  CONSTRAINT `rbac_role_permissions_role_id_d10416cb_fk_rbac_role_id` FOREIGN KEY (`role_id`) REFERENCES `rbac_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=124 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rbac_role_permissions`
--

LOCK TABLES `rbac_role_permissions` WRITE;
/*!40000 ALTER TABLE `rbac_role_permissions` DISABLE KEYS */;
INSERT INTO `rbac_role_permissions` VALUES (61,7,64),(62,7,65),(63,7,66),(64,7,67),(65,7,68),(66,7,69),(67,7,70),(68,7,71),(69,7,72),(70,7,73),(71,7,74),(72,7,75),(73,7,76),(74,7,77),(75,7,78),(76,7,79),(77,7,80),(78,7,81),(79,7,82),(80,7,83),(81,7,84),(82,7,85),(83,7,86),(84,7,87),(85,7,88),(86,7,89),(87,7,90),(88,7,91),(89,7,92),(90,7,93),(91,7,94),(92,7,95),(93,7,96),(94,7,97),(95,7,98),(96,7,99),(97,7,100),(98,7,101),(99,7,102),(100,7,103),(101,7,104),(102,7,105),(103,7,106),(104,7,107),(105,7,108),(106,7,109),(107,7,110),(108,7,111),(109,7,112),(110,7,113),(111,7,114),(112,7,115),(113,7,116),(114,7,117),(115,7,118),(116,7,119),(117,7,120),(118,7,121),(119,7,122),(120,7,123),(121,7,124),(122,7,125),(123,7,126);
/*!40000 ALTER TABLE `rbac_role_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_classlist`
--

DROP TABLE IF EXISTS `web_classlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_classlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `semester` int(10) unsigned NOT NULL,
  `price` int(10) unsigned NOT NULL,
  `start_date` date NOT NULL,
  `graduate_date` date DEFAULT NULL,
  `memo` longtext,
  `class_teacher_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `school_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `web_classlist_course_id_0d0bb3df_fk_web_course_id` (`course_id`),
  KEY `web_classlist_school_id_cc9a49ba_fk_web_school_id` (`school_id`),
  KEY `web_classlist_class_teacher_id_adda1501_fk_web_userinfo_id` (`class_teacher_id`),
  CONSTRAINT `web_classlist_class_teacher_id_adda1501_fk_web_userinfo_id` FOREIGN KEY (`class_teacher_id`) REFERENCES `web_userinfo` (`id`),
  CONSTRAINT `web_classlist_course_id_0d0bb3df_fk_web_course_id` FOREIGN KEY (`course_id`) REFERENCES `web_course` (`id`),
  CONSTRAINT `web_classlist_school_id_cc9a49ba_fk_web_school_id` FOREIGN KEY (`school_id`) REFERENCES `web_school` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_classlist`
--

LOCK TABLES `web_classlist` WRITE;
/*!40000 ALTER TABLE `web_classlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_classlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_classlist_tech_teachers`
--

DROP TABLE IF EXISTS `web_classlist_tech_teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_classlist_tech_teachers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classlist_id` int(11) NOT NULL,
  `userinfo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `web_classlist_tech_teach_classlist_id_userinfo_id_b70ec689_uniq` (`classlist_id`,`userinfo_id`),
  KEY `web_classlist_tech_t_userinfo_id_7d6dfc5e_fk_web_useri` (`userinfo_id`),
  CONSTRAINT `web_classlist_tech_t_classlist_id_c24729e2_fk_web_class` FOREIGN KEY (`classlist_id`) REFERENCES `web_classlist` (`id`),
  CONSTRAINT `web_classlist_tech_t_userinfo_id_7d6dfc5e_fk_web_useri` FOREIGN KEY (`userinfo_id`) REFERENCES `web_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_classlist_tech_teachers`
--

LOCK TABLES `web_classlist_tech_teachers` WRITE;
/*!40000 ALTER TABLE `web_classlist_tech_teachers` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_classlist_tech_teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_consultrecord`
--

DROP TABLE IF EXISTS `web_consultrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_consultrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `note` longtext NOT NULL,
  `date` date NOT NULL,
  `consultant_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `web_consultrecord_consultant_id_914c38fa_fk_web_userinfo_id` (`consultant_id`),
  KEY `web_consultrecord_customer_id_befb7f7f_fk_web_customer_id` (`customer_id`),
  CONSTRAINT `web_consultrecord_customer_id_befb7f7f_fk_web_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `web_customer` (`id`),
  CONSTRAINT `web_consultrecord_consultant_id_914c38fa_fk_web_userinfo_id` FOREIGN KEY (`consultant_id`) REFERENCES `web_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_consultrecord`
--

LOCK TABLES `web_consultrecord` WRITE;
/*!40000 ALTER TABLE `web_consultrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_consultrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_course`
--

DROP TABLE IF EXISTS `web_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_course`
--

LOCK TABLES `web_course` WRITE;
/*!40000 ALTER TABLE `web_course` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_courserecord`
--

DROP TABLE IF EXISTS `web_courserecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_courserecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `day_num` int(11) NOT NULL,
  `date` date NOT NULL,
  `class_object_id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `web_courserecord_class_object_id_e107b311_fk_web_classlist_id` (`class_object_id`),
  KEY `web_courserecord_teacher_id_3d847927_fk_web_userinfo_id` (`teacher_id`),
  CONSTRAINT `web_courserecord_teacher_id_3d847927_fk_web_userinfo_id` FOREIGN KEY (`teacher_id`) REFERENCES `web_userinfo` (`id`),
  CONSTRAINT `web_courserecord_class_object_id_e107b311_fk_web_classlist_id` FOREIGN KEY (`class_object_id`) REFERENCES `web_classlist` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_courserecord`
--

LOCK TABLES `web_courserecord` WRITE;
/*!40000 ALTER TABLE `web_courserecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_courserecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_customer`
--

DROP TABLE IF EXISTS `web_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `qq` varchar(64) NOT NULL,
  `status` int(11) NOT NULL,
  `gender` smallint(6) NOT NULL,
  `source` smallint(6) NOT NULL,
  `education` int(11) DEFAULT NULL,
  `graduation_school` varchar(64) DEFAULT NULL,
  `major` varchar(64) DEFAULT NULL,
  `experience` int(11) DEFAULT NULL,
  `work_status` int(11) DEFAULT NULL,
  `company` varchar(64) DEFAULT NULL,
  `salary` varchar(64) DEFAULT NULL,
  `date` date NOT NULL,
  `last_consult_date` date NOT NULL,
  `consultant_id` int(11) DEFAULT NULL,
  `referral_from_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `qq` (`qq`),
  KEY `web_customer_consultant_id_e3c377b3_fk_web_userinfo_id` (`consultant_id`),
  KEY `web_customer_referral_from_id_cba5a965_fk_web_customer_id` (`referral_from_id`),
  CONSTRAINT `web_customer_referral_from_id_cba5a965_fk_web_customer_id` FOREIGN KEY (`referral_from_id`) REFERENCES `web_customer` (`id`),
  CONSTRAINT `web_customer_consultant_id_e3c377b3_fk_web_userinfo_id` FOREIGN KEY (`consultant_id`) REFERENCES `web_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_customer`
--

LOCK TABLES `web_customer` WRITE;
/*!40000 ALTER TABLE `web_customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_customer_course`
--

DROP TABLE IF EXISTS `web_customer_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_customer_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `web_customer_course_customer_id_course_id_4c572199_uniq` (`customer_id`,`course_id`),
  KEY `web_customer_course_course_id_7f7b8902_fk_web_course_id` (`course_id`),
  CONSTRAINT `web_customer_course_course_id_7f7b8902_fk_web_course_id` FOREIGN KEY (`course_id`) REFERENCES `web_course` (`id`),
  CONSTRAINT `web_customer_course_customer_id_8ce5dbc5_fk_web_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `web_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_customer_course`
--

LOCK TABLES `web_customer_course` WRITE;
/*!40000 ALTER TABLE `web_customer_course` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_customer_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_department`
--

DROP TABLE IF EXISTS `web_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(16) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_department`
--

LOCK TABLES `web_department` WRITE;
/*!40000 ALTER TABLE `web_department` DISABLE KEYS */;
INSERT INTO `web_department` VALUES (2,'总裁办');
/*!40000 ALTER TABLE `web_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_paymentrecord`
--

DROP TABLE IF EXISTS `web_paymentrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_paymentrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pay_type` int(11) NOT NULL,
  `paid_fee` int(11) NOT NULL,
  `apply_date` datetime(6) NOT NULL,
  `confirm_status` int(11) NOT NULL,
  `confirm_date` datetime(6) DEFAULT NULL,
  `note` longtext,
  `class_list_id` int(11) NOT NULL,
  `confirm_user_id` int(11) DEFAULT NULL,
  `consultant_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `web_paymentrecord_class_list_id_9f0826ec_fk_web_classlist_id` (`class_list_id`),
  KEY `web_paymentrecord_confirm_user_id_1668de5d_fk_web_userinfo_id` (`confirm_user_id`),
  KEY `web_paymentrecord_consultant_id_3a7e9446_fk_web_userinfo_id` (`consultant_id`),
  KEY `web_paymentrecord_customer_id_da57a16c_fk_web_customer_id` (`customer_id`),
  CONSTRAINT `web_paymentrecord_customer_id_da57a16c_fk_web_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `web_customer` (`id`),
  CONSTRAINT `web_paymentrecord_class_list_id_9f0826ec_fk_web_classlist_id` FOREIGN KEY (`class_list_id`) REFERENCES `web_classlist` (`id`),
  CONSTRAINT `web_paymentrecord_confirm_user_id_1668de5d_fk_web_userinfo_id` FOREIGN KEY (`confirm_user_id`) REFERENCES `web_userinfo` (`id`),
  CONSTRAINT `web_paymentrecord_consultant_id_3a7e9446_fk_web_userinfo_id` FOREIGN KEY (`consultant_id`) REFERENCES `web_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_paymentrecord`
--

LOCK TABLES `web_paymentrecord` WRITE;
/*!40000 ALTER TABLE `web_paymentrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_paymentrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_school`
--

DROP TABLE IF EXISTS `web_school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_school` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_school`
--

LOCK TABLES `web_school` WRITE;
/*!40000 ALTER TABLE `web_school` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_school` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_scorerecord`
--

DROP TABLE IF EXISTS `web_scorerecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_scorerecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `score` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `web_scorerecord_student_id_f8f7a771_fk_web_student_id` (`student_id`),
  KEY `web_scorerecord_user_id_179a77da_fk_web_userinfo_id` (`user_id`),
  CONSTRAINT `web_scorerecord_user_id_179a77da_fk_web_userinfo_id` FOREIGN KEY (`user_id`) REFERENCES `web_userinfo` (`id`),
  CONSTRAINT `web_scorerecord_student_id_f8f7a771_fk_web_student_id` FOREIGN KEY (`student_id`) REFERENCES `web_student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_scorerecord`
--

LOCK TABLES `web_scorerecord` WRITE;
/*!40000 ALTER TABLE `web_scorerecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_scorerecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_student`
--

DROP TABLE IF EXISTS `web_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qq` varchar(32) NOT NULL,
  `mobile` varchar(32) NOT NULL,
  `emergency_contract` varchar(32) NOT NULL,
  `student_status` int(11) NOT NULL,
  `memo` varchar(255) DEFAULT NULL,
  `customer_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customer_id` (`customer_id`),
  CONSTRAINT `web_student_customer_id_10f0afe4_fk_web_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `web_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_student`
--

LOCK TABLES `web_student` WRITE;
/*!40000 ALTER TABLE `web_student` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_student_class_list`
--

DROP TABLE IF EXISTS `web_student_class_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_student_class_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `classlist_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `web_student_class_list_student_id_classlist_id_7937e885_uniq` (`student_id`,`classlist_id`),
  KEY `web_student_class_list_classlist_id_c9c47794_fk_web_classlist_id` (`classlist_id`),
  CONSTRAINT `web_student_class_list_classlist_id_c9c47794_fk_web_classlist_id` FOREIGN KEY (`classlist_id`) REFERENCES `web_classlist` (`id`),
  CONSTRAINT `web_student_class_list_student_id_76222b07_fk_web_student_id` FOREIGN KEY (`student_id`) REFERENCES `web_student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_student_class_list`
--

LOCK TABLES `web_student_class_list` WRITE;
/*!40000 ALTER TABLE `web_student_class_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_student_class_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_studyrecord`
--

DROP TABLE IF EXISTS `web_studyrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_studyrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `record` varchar(64) NOT NULL,
  `course_record_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `web_studyrecord_course_record_id_a3162b0f_fk_web_courserecord_id` (`course_record_id`),
  KEY `web_studyrecord_student_id_a81eb429_fk_web_student_id` (`student_id`),
  CONSTRAINT `web_studyrecord_student_id_a81eb429_fk_web_student_id` FOREIGN KEY (`student_id`) REFERENCES `web_student` (`id`),
  CONSTRAINT `web_studyrecord_course_record_id_a3162b0f_fk_web_courserecord_id` FOREIGN KEY (`course_record_id`) REFERENCES `web_courserecord` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_studyrecord`
--

LOCK TABLES `web_studyrecord` WRITE;
/*!40000 ALTER TABLE `web_studyrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_studyrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_userinfo`
--

DROP TABLE IF EXISTS `web_userinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_userinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `password` varchar(64) NOT NULL,
  `email` varchar(32) DEFAULT NULL,
  `nickname` varchar(16) NOT NULL,
  `phone` varchar(32) NOT NULL,
  `gender` int(11) NOT NULL,
  `depart_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `web_userinfo_depart_id_4df860bd_fk_web_department_id` (`depart_id`),
  CONSTRAINT `web_userinfo_depart_id_4df860bd_fk_web_department_id` FOREIGN KEY (`depart_id`) REFERENCES `web_department` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_userinfo`
--

LOCK TABLES `web_userinfo` WRITE;
/*!40000 ALTER TABLE `web_userinfo` DISABLE KEYS */;
INSERT INTO `web_userinfo` VALUES (2,'alex','e36660c2858bb244e0b124931d00d5a0','123@qq.com','金角大王','123',1,2);
/*!40000 ALTER TABLE `web_userinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_userinfo_roles`
--

DROP TABLE IF EXISTS `web_userinfo_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_userinfo_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userinfo_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `web_userinfo_roles_userinfo_id_role_id_e0435f62_uniq` (`userinfo_id`,`role_id`),
  KEY `web_userinfo_roles_role_id_c9cdbf1d_fk_rbac_role_id` (`role_id`),
  CONSTRAINT `web_userinfo_roles_role_id_c9cdbf1d_fk_rbac_role_id` FOREIGN KEY (`role_id`) REFERENCES `rbac_role` (`id`),
  CONSTRAINT `web_userinfo_roles_userinfo_id_090d779f_fk_web_userinfo_id` FOREIGN KEY (`userinfo_id`) REFERENCES `web_userinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_userinfo_roles`
--

LOCK TABLES `web_userinfo_roles` WRITE;
/*!40000 ALTER TABLE `web_userinfo_roles` DISABLE KEYS */;
INSERT INTO `web_userinfo_roles` VALUES (2,2,7);
/*!40000 ALTER TABLE `web_userinfo_roles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-24  3:04:28
