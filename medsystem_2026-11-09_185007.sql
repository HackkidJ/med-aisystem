-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: medsystem
-- ------------------------------------------------------
-- Server version	8.3.0

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
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  `id` varchar(255) NOT NULL COMMENT '医生id',
  `identity_id` varchar(255) NOT NULL COMMENT '医生身份证号',
  `phone` varchar(255) NOT NULL COMMENT '电话',
  `passwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '密码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='账号信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES ('17af15d3-1e2d-46a1-ae96-7eefc61bcfca','537222199402042970','11561237700','$2a$10$KqkSDhNcwVcq59gicD704Onc05693suE16HDe/hMY7JaTQthLDOKC');
/*!40000 ALTER TABLE `account` ENABLE KEYS */;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `id` varchar(255) NOT NULL COMMENT 'user_id',
  `identity_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '身份证号',
  `name` varchar(255) NOT NULL COMMENT '姓名',
  `gender` enum('男','女') NOT NULL COMMENT '性别',
  `phone` varchar(255) DEFAULT NULL COMMENT '电话号码',
  `mail` varchar(255) DEFAULT NULL COMMENT '邮箱',
  `address` varchar(255) DEFAULT NULL COMMENT '家庭住址',
  `department` enum('急诊科','重症医学科','健康教育科','内一科','内二科','皮肤科','眼耳鼻咽喉科','感染性疾病科','口腔科','外一科','外二科','中医科','麻醉科','妇产科','儿科') DEFAULT NULL COMMENT '科室',
  `level` enum('医士','医师','主治医师','副主任医师','主任医师') DEFAULT NULL COMMENT '级别',
  `picture` blob COMMENT '照片',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='医生信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES ('17af15d3-1e2d-46a1-ae96-7eefc61bcfca','537222199402042970','hackkid','男','1232132132',NULL,NULL,NULL,NULL,NULL),('testid','232130512','tester','男','123456','321@121.com','heaven','口腔科','主治医师',NULL);
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;

--
-- Table structure for table `logger`
--

DROP TABLE IF EXISTS `logger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logger` (
  `id` varchar(255) NOT NULL,
  `execute_time` datetime NOT NULL COMMENT '操作时间',
  `content` text NOT NULL COMMENT '操作内容',
  `user_id` varchar(255) NOT NULL COMMENT '提交用户id',
  `is_AI` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否ai操作',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据库操作记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logger`
--

/*!40000 ALTER TABLE `logger` DISABLE KEYS */;
INSERT INTO `logger` VALUES ('03fd9edf-7108-4fa9-8749-fe2ef9c82220','2025-10-10 08:44:05','向patients表添加了patient\nId:b8ff9c67-d06d-4485-b817-cc4529fba930\nIdentity:123456789012345678\nname:小明\ngender:男\nphone:\naddress\nPMH:\nPI:无其他异常现象\nCC:发烧头痛持续三天\nupdateTime:Fri Oct 10 08:44:05 CST 2025\ndoc_id:17af15d3-1e2d-46a1-ae96-7eefc61bcfca\n','17af15d3-1e2d-46a1-ae96-7eefc61bcfca',1),('13567f2e-e12d-4be9-91c4-f7d83e67e66c','2025-10-17 18:20:15','向patients表添加了patient\nId:2d7c23d5-3b9f-48de-9a6e-5f64d66f9be7\nIdentity:542132100505012312\nname:黄五\ngender:男\nphone:12214564455\naddressxxx街道\nPMH:三年吸烟史，甲型糖尿病\nPI:\nCC:头痛发热三天无减退\nupdateTime:Fri Oct 17 18:20:15 CST 2025\ndoc_id:17af15d3-1e2d-46a1-ae96-7eefc61bcfca\n','17af15d3-1e2d-46a1-ae96-7eefc61bcfca',1),('14eaf2db-b80b-4960-8f50-1936de0fc69d','2025-10-10 11:09:51','向patients表添加了patient\nId:c061d2b5-68a7-4c22-a4a8-fad708d855e4\nIdentity:512302200156401201\nname:黄天\ngender:男\nphone:\naddress\nPMH:对阿片类药物过敏\nPI:头疼发烧持续三天，没有减退\nCC:头疼发烧持续三天\nupdateTime:Fri Oct 10 11:09:51 CST 2025\ndoc_id:17af15d3-1e2d-46a1-ae96-7eefc61bcfca\n','17af15d3-1e2d-46a1-ae96-7eefc61bcfca',1),('1b3b58c5-b7dd-4c54-85e8-3bd5f6b54a08','2025-10-01 01:09:48','向patients表添加了patient\nId:584e1643-0ac8-4ec7-98a1-705288c347de\nIdentity:123456789\nname:da\ngender:男\nphone:35135\naddress \nPMH: \nPI: \nCC: \nupdateTime:Wed Oct 01 01:09:48 CST 2025\ndoc_id:2asd\n','2asd',1),('1deeaa59-2b6e-47ca-83a1-85bba30a034a','2025-10-09 22:02:55','向patients表添加了patient\nId:38542d17-30cf-4f6b-bb93-12730451b173\nIdentity:500230200408042330\nname:大明\ngender:男\nphone:\naddress饭都花园\nPMH:\nPI:\nCC:\nupdateTime:Thu Oct 09 22:02:54 CST 2025\ndoc_id:17af15d3-1e2d-46a1-ae96-7eefc61bcfca\n','17af15d3-1e2d-46a1-ae96-7eefc61bcfca',1),('21847fbd-989d-402d-a593-7ad27a934782','2025-10-10 10:30:04','修改了patients表中的患者信息\nId: 75887fc4-d356-4ba0-a8fd-2e03ba87b42e\nIdentity: 123230200408040456\nname: 张三\ngender: 男\nphone: 138-1234-5678\naddress: 河北省石家庄市桥西区XX街道12号\nPMH: 否认高血压、糖尿病；幼年曾患肺结核，已治愈。否认慢性支气管炎、哮喘等病史。\nPI: 患者近2个月来持续干咳，偶有白色泡沫痰，1周前发现痰中带血丝，无发热。近3天出现左侧胸部隐痛，深呼吸时加重。体重下降约3公斤。未就诊过专科医院。\nCC: 咳嗽伴痰中带血2个月，近期出现胸痛\nupdateTime: Fri Oct 10 10:30:04 CST 2025\ndoc_id: 1\n','1',1),('3cc93e05-e64d-4266-b5b3-d94a979d0433','2025-10-01 01:09:00','向patients表添加了patient\nId:3d40ea04-f5ad-458b-b2f7-eba84d8557fc\nIdentity:123456789\nname:da\ngender:男\nphone:35135\naddress \nPMH: \nPI: \nCC: \nupdateTime:Wed Oct 01 01:09:00 CST 2025\ndoc_id:2asd\n','2asd',1),('46778dba-af6b-4a70-ba82-e99c5153d9a3','2025-10-15 01:24:41','向patients表添加了patient\nId:8c9fb037-74cd-4c5c-a2dc-ceee3e01fd2d\nIdentity:530103211405041123\nname:张三\ngender:男\nphone:123123123\naddress翻斗花园\nPMH:甲型糖尿病，六年吸烟史\nPI:\nCC:发烧三天不减退，轻微头晕\nupdateTime:Wed Oct 15 01:24:40 CST 2025\ndoc_id:17af15d3-1e2d-46a1-ae96-7eefc61bcfca\n','17af15d3-1e2d-46a1-ae96-7eefc61bcfca',1),('504abe43-6a38-4395-9ce8-a9f50c34b41e','2025-10-09 21:38:13','向patients表添加了patient\nId:75887fc4-d356-4ba0-a8fd-2e03ba87b42e\nIdentity:123230200408040456\nname:张三\ngender:男\nphone:13800138000\naddress\nPMH:\nPI:\nCC:\nupdateTime:Thu Oct 09 21:38:12 CST 2025\ndoc_id:1\n','1',1),('5bdcda2b-de6d-4ee7-b744-d3c94940e98b','2026-10-29 16:46:15','向patients表添加了patient\nId:2d1c8e30-e699-41ab-8d93-39749f044903\nIdentity:17af15d3-1e2d-46a1-ae96-7eefc61bcfca\nname:李明华\ngender:男\nphone:\naddress\nPMH:胆囊结石病史\nPI:患者昨晚聚餐后突发上腹部持续性剧痛，阵发性加剧，疼痛向左肩及后背放射，伴有恶心、呕吐，呕吐物为胃内容物，呕吐后腹痛不缓解。查体：上腹部压痛明显，无肌紧张及反跳痛。既往有胆囊结石病史。\nCC:上腹部持续性剧痛，向左肩及后背放射，伴恶心呕吐，呕吐后不缓解\nupdateTime:Thu Oct 29 16:46:15 CST 2026\ndoc_id:17af15d3-1e2d-46a1-ae96-7eefc61bcfca\n','17af15d3-1e2d-46a1-ae96-7eefc61bcfca',1),('6b2848c4-565f-4de5-a4ca-e158852131cb','2025-10-10 10:58:43','向patients表添加了patient\nId:2c1239ef-6bb1-4d13-9174-7635656eecbd\nIdentity:512302200102301201\nname:黄新锋\ngender:男\nphone:\naddress\nPMH:对阿片类药物过敏\nPI:患者11岁，近三天出现持续性头痛、发热（最高达39.2℃），伴有乏力、食欲减退。已接种流感疫苗，否认近期接触传染病史。既往无慢性病史，但对阿片类药物过敏（曾因服用可待因后出现呼吸抑制）。目前无咳嗽、咳痰、胸痛或呼吸困难。查体：体温38.9℃，咽部轻度充血，心肺听诊未闻及异常，神经系统查体正常。\nCC:头疼发烧持续三天，无缓解\nupdateTime:Fri Oct 10 10:58:42 CST 2025\ndoc_id:17af15d3-1e2d-46a1-ae96-7eefc61bcfca\n','17af15d3-1e2d-46a1-ae96-7eefc61bcfca',1),('6fd19489-8924-4bc2-a709-7c770322cad3','2025-10-09 21:52:43','向patients表添加了patient\nId:9a929011-ab66-4558-aa3b-66450e2ce8c7\nIdentity:500230200408042130\nname:小明\ngender:男\nphone:\naddress\nPMH:\nPI:\nCC:\nupdateTime:Thu Oct 09 21:52:43 CST 2025\ndoc_id:17af15d3-1e2d-46a1-ae96-7eefc61bcfca\n','17af15d3-1e2d-46a1-ae96-7eefc61bcfca',1),('71677e8b-e5ec-4786-a078-b9c9c3ca5765','2026-11-03 11:09:47','向patients表添加了patient\nId:41aeb751-0182-48a5-9013-72008d03154c\nIdentity:513211100501561012\nname:张三\ngender:男\nphone:\naddress\nPMH:\nPI:患者男性，28岁，主诉发热伴咳嗽、咳黄痰3天。体温最高38.5℃，伴有轻微胸闷和咽痛，无咯血及呼吸困难。听诊双肺呼吸音粗，未闻及明显干湿啰音。\nCC:发热伴咳嗽、咳黄痰3天\nupdateTime:Tue Nov 03 11:09:47 CST 2026\ndoc_id:17af15d3-1e2d-46a1-ae96-7eefc61bcfca\n','17af15d3-1e2d-46a1-ae96-7eefc61bcfca',1),('88ddffcc-5548-412f-96ee-fbd5c6bd2144','2025-10-10 08:52:26','向patients表添加了patient\nId:308b873f-aeb0-4466-9963-c9add1b44ef8\nIdentity:512300402104062701\nname:小明\ngender:男\nphone:\naddress\nPMH:\nPI:发热、头痛，无其他明显症状，初步评估为轻型病毒感染\nCC:发烧头痛持续三天\nupdateTime:Fri Oct 10 08:52:26 CST 2025\ndoc_id:17af15d3-1e2d-46a1-ae96-7eefc61bcfca\n','17af15d3-1e2d-46a1-ae96-7eefc61bcfca',1),('908ccb42-6a35-4e54-a179-00fed823c798','2025-10-09 20:31:13','向patients表添加了patient\nId:961aa142-4d6b-4931-b72b-dcdb1a9df881\nIdentity:512230200450021130\nname:ak\ngender:男\nphone:4231313\naddressasdld\nPMH:\nPI:\nCC:\nupdateTime:Thu Oct 09 20:31:12 CST 2025\ndoc_id:asd123sad\n','asd123sad',1),('da8dbb9a-be3e-44ed-a7ff-87c58481d41f','2025-10-10 10:49:42','修改了patients表中的患者信息\nId: b8ff9c67-d06d-4485-b817-cc4529fba930\nIdentity: 123456789012345678\nname: 小明\ngender: 男\nphone: \naddress: \nPMH: 长年吸烟，慢性支气管炎病史（疑似）\nPI: 主诉：呼吸困难，肺部肿胀。现病史：患者近一周出现进行性加重的呼吸困难，伴有胸闷、咳嗽，咳少量白色黏痰。查体发现双肺呼吸音减弱，可闻及散在干湿啰音，胸部X线提示双肺纹理增粗、肺部阴影，考虑存在肺部感染或慢性阻塞性肺疾病急性加重。既往有长年吸烟史，无其他基础疾病。\nCC: 发烧头痛持续三天\nupdateTime: Fri Oct 10 10:49:42 CST 2025\ndoc_id: 17af15d3-1e2d-46a1-ae96-7eefc61bcfca\n','17af15d3-1e2d-46a1-ae96-7eefc61bcfca',1),('e69acae5-1ad3-4142-8c56-1f38f9f3da52','2025-10-10 11:10:40','向patients表添加了patient\nId:93bb68a3-fe53-4e85-8238-90975dc9f0d8\nIdentity:512302200156401201\nname:黄天\ngender:男\nphone:\naddress\nPMH:对阿片类药物过敏\nPI:头疼、发烧持续三天，无减退\nCC:头疼发烧持续三天\nupdateTime:Fri Oct 10 11:10:39 CST 2025\ndoc_id:17af15d3-1e2d-46a1-ae96-7eefc61bcfca\n','17af15d3-1e2d-46a1-ae96-7eefc61bcfca',1);
/*!40000 ALTER TABLE `logger` ENABLE KEYS */;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `id` varchar(255) NOT NULL COMMENT 'user_id',
  `identity_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '身份证号',
  `name` varchar(255) NOT NULL COMMENT '姓名',
  `gender` enum('男','女') NOT NULL COMMENT '性别',
  `phone` varchar(255) DEFAULT NULL COMMENT '电话号码',
  `address` varchar(255) DEFAULT NULL COMMENT '家庭住址',
  `PMH` text COMMENT '既往病史',
  `PI` text COMMENT '现病史',
  `CC` text COMMENT '主诉',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `doc_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '主治医生id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='患者信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES ('2d1c8e30-e699-41ab-8d93-39749f044903','17af15d3-1e2d-46a1-ae96-7eefc61bcfca','李明华','男','','','胆囊结石病史','患者昨晚聚餐后突发上腹部持续性剧痛，阵发性加剧，疼痛向左肩及后背放射，伴有恶心、呕吐，呕吐物为胃内容物，呕吐后腹痛不缓解。查体：上腹部压痛明显，无肌紧张及反跳痛。既往有胆囊结石病史。','上腹部持续性剧痛，向左肩及后背放射，伴恶心呕吐，呕吐后不缓解','2026-10-29 16:46:15','17af15d3-1e2d-46a1-ae96-7eefc61bcfca'),('2d7c23d5-3b9f-48de-9a6e-5f64d66f9be7','542132100505012312','黄五','男','12214564455','xxx街道','三年吸烟史，甲型糖尿病','','头痛发热三天无减退','2025-10-17 18:20:15','17af15d3-1e2d-46a1-ae96-7eefc61bcfca'),('308b873f-aeb0-4466-9963-c9add1b44ef8','512300402104062701','小明','男','','','','发热、头痛，无其他明显症状，初步评估为轻型病毒感染','发烧头痛持续三天','2025-10-10 08:52:26','17af15d3-1e2d-46a1-ae96-7eefc61bcfca'),('38542d17-30cf-4f6b-bb93-12730451b173','500230200408042330','大明','男','','饭都花园','','','','2025-10-09 22:02:55','17af15d3-1e2d-46a1-ae96-7eefc61bcfca'),('41aeb751-0182-48a5-9013-72008d03154c','513211100501561012','张三','男','','','','患者男性，28岁，主诉发热伴咳嗽、咳黄痰3天。体温最高38.5℃，伴有轻微胸闷和咽痛，无咯血及呼吸困难。听诊双肺呼吸音粗，未闻及明显干湿啰音。','发热伴咳嗽、咳黄痰3天','2026-11-03 11:09:47','17af15d3-1e2d-46a1-ae96-7eefc61bcfca'),('75887fc4-d356-4ba0-a8fd-2e03ba87b42e','123230200408040456','张三','男','138-1234-5678','河北省石家庄市桥西区XX街道12号','否认高血压、糖尿病；幼年曾患肺结核，已治愈。否认慢性支气管炎、哮喘等病史。','患者近2个月来持续干咳，偶有白色泡沫痰，1周前发现痰中带血丝，无发热。近3天出现左侧胸部隐痛，深呼吸时加重。体重下降约3公斤。未就诊过专科医院。','咳嗽伴痰中带血2个月，近期出现胸痛','2025-10-10 10:30:04','1'),('8c9fb037-74cd-4c5c-a2dc-ceee3e01fd2d','530103211405041123','张三','男','123123123','翻斗花园','甲型糖尿病，六年吸烟史','','发烧三天不减退，轻微头晕','2025-10-15 01:24:41','17af15d3-1e2d-46a1-ae96-7eefc61bcfca'),('93bb68a3-fe53-4e85-8238-90975dc9f0d8','512302200156401201','黄天','男','','','对阿片类药物过敏','头疼、发烧持续三天，无减退','头疼发烧持续三天','2025-10-10 11:10:40','17af15d3-1e2d-46a1-ae96-7eefc61bcfca'),('961aa142-4d6b-4931-b72b-dcdb1a9df881','512230200450021130','ak','男','4231313','asdld','','','','2025-10-09 20:31:12','asd123sad'),('b8ff9c67-d06d-4485-b817-cc4529fba930','123456789012345678','小明','男','','','长年吸烟，慢性支气管炎病史（疑似）','主诉：呼吸困难，肺部肿胀。现病史：患者近一周出现进行性加重的呼吸困难，伴有胸闷、咳嗽，咳少量白色黏痰。查体发现双肺呼吸音减弱，可闻及散在干湿啰音，胸部X线提示双肺纹理增粗、肺部阴影，考虑存在肺部感染或慢性阻塞性肺疾病急性加重。既往有长年吸烟史，无其他基础疾病。','发烧头痛持续三天','2025-10-10 10:49:42','17af15d3-1e2d-46a1-ae96-7eefc61bcfca'),('c061d2b5-68a7-4c22-a4a8-fad708d855e4','512302200156401201','黄天','男','','','对阿片类药物过敏','头疼发烧持续三天，没有减退','头疼发烧持续三天','2025-10-10 11:09:51','17af15d3-1e2d-46a1-ae96-7eefc61bcfca');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;

--
-- Table structure for table `prescription`
--

DROP TABLE IF EXISTS `prescription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescription` (
  `id` varchar(255) NOT NULL,
  `patientid` varchar(255) NOT NULL COMMENT '患者id',
  `docid` varchar(255) NOT NULL COMMENT '医生id',
  `content` text NOT NULL COMMENT '处方内容',
  `createTime` datetime NOT NULL COMMENT '开方时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='处方表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescription`
--

/*!40000 ALTER TABLE `prescription` DISABLE KEYS */;
/*!40000 ALTER TABLE `prescription` ENABLE KEYS */;

--
-- Dumping routines for database 'medsystem'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-09 18:50:12
