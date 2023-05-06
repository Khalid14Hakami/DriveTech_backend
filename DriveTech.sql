-- DriveTech.CAR definition

CREATE TABLE `CAR` (
  `car_id` int NOT NULL AUTO_INCREMENT,
  `VIN` varchar(45) NOT NULL,
  `color` varchar(45) NOT NULL,
  `arrival_date` datetime NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `FL` double DEFAULT NULL COMMENT 'Front Left PSI',
  `FR` double DEFAULT NULL COMMENT 'Front Right PSI',
  `RR` double DEFAULT NULL,
  `RL` double DEFAULT NULL,
  `storage_location` varchar(100) DEFAULT NULL,
  `batt_green` tinyint(1) DEFAULT NULL,
  `batt_voltage` double DEFAULT NULL,
  `batt_model` varchar(100) DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`car_id`),
  UNIQUE KEY `CAR_ID_UNIQUE` (`car_id`),
  UNIQUE KEY `VIN_UNIQUE` (`VIN`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- DriveTech.`ROUTINE` definition

CREATE TABLE `ROUTINE` (
  `rtn_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `model` varchar(45) NOT NULL,
  PRIMARY KEY (`rtn_id`),
  UNIQUE KEY `rtn_id_UNIQUE` (`rtn_id`),
  UNIQUE KEY `ROUTINE_UN` (`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- DriveTech.STORAGE definition

CREATE TABLE `STORAGE` (
  `strg_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `location` varchar(45) DEFAULT NULL,
  `proponent` varchar(45) DEFAULT NULL,
  `contact` varchar(13) DEFAULT NULL,
  `capacity` decimal(10,0) NOT NULL,
  PRIMARY KEY (`strg_id`),
  UNIQUE KEY `strg_id_UNIQUE` (`strg_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- DriveTech.TASK definition

CREATE TABLE `TASK` (
  `task_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  `frequency` int NOT NULL COMMENT 'frequency in days ',
  `num_of_attrib` decimal(10,0) DEFAULT NULL,
  `attrib_names` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `req_image` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- DriveTech.CAR_LOG_PICS definition

CREATE TABLE `CAR_LOG_PICS` (
  `log_id` int DEFAULT NULL,
  `image` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- DriveTech.rtn_tsk definition

CREATE TABLE `rtn_tsk` (
  `task_id` int NOT NULL,
  `rtn_id` int NOT NULL,
  PRIMARY KEY (`task_id`,`rtn_id`),
  KEY `routine_idx` (`rtn_id`),
  CONSTRAINT `rtn_tsk_FK` FOREIGN KEY (`rtn_id`) REFERENCES `ROUTINE` (`rtn_id`),
  CONSTRAINT `rtn_tsk_FK_1` FOREIGN KEY (`task_id`) REFERENCES `TASK` (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='table to show the routines and its tasks ';


-- DriveTech.`STORED` definition

CREATE TABLE `STORED` (
  `car_id` int NOT NULL,
  `strg_id` int NOT NULL,
  PRIMARY KEY (`car_id`,`strg_id`),
  KEY `storage_id_idx` (`strg_id`),
  CONSTRAINT `STORED_FK` FOREIGN KEY (`car_id`) REFERENCES `CAR` (`car_id`),
  CONSTRAINT `STORED_FK_1` FOREIGN KEY (`strg_id`) REFERENCES `STORAGE` (`strg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- DriveTech.`USER` definition

CREATE TABLE `USER` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `strg_id` int NOT NULL DEFAULT '0',
  `role` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  KEY `USER_FK` (`strg_id`),
  CONSTRAINT `USER_FK` FOREIGN KEY (`strg_id`) REFERENCES `STORAGE` (`strg_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- DriveTech.CAR_LOG definition

CREATE TABLE `CAR_LOG` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `car_id` int NOT NULL,
  `task_id` int NOT NULL,
  `task_value` varchar(45) NOT NULL,
  `rtn_id` int DEFAULT NULL,
  `task_date` datetime NOT NULL,
  `notes` varchar(45) DEFAULT NULL,
  `user_id` int NOT NULL,
  `task_status` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`log_id`),
  KEY `usr_id_idx` (`user_id`),
  KEY `car_id_idx` (`car_id`),
  KEY `log_task_id_fk_idx` (`task_id`),
  KEY `log_rtn_id_fk_idx` (`rtn_id`),
  CONSTRAINT `CAR_LOG_FK` FOREIGN KEY (`car_id`) REFERENCES `CAR` (`car_id`),
  CONSTRAINT `CAR_LOG_FK_1` FOREIGN KEY (`user_id`) REFERENCES `USER` (`user_id`),
  CONSTRAINT `CAR_LOG_FK_2` FOREIGN KEY (`task_id`) REFERENCES `TASK` (`task_id`),
  CONSTRAINT `CAR_LOG_FK_3` FOREIGN KEY (`rtn_id`) REFERENCES `ROUTINE` (`rtn_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;