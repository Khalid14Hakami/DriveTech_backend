-- DriveTech.CAR definition

CREATE TABLE `CAR` (
  `car_id` int NOT NULL,
  `VIN` varchar(45) NOT NULL,
  `color` varchar(45) NOT NULL,
  `arraival_date` datetime NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`car_id`),
  UNIQUE KEY `CAR_ID_UNIQUE` (`car_id`),
  UNIQUE KEY `VIN_UNIQUE` (`VIN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- DriveTech.`ROUTINE` definition

CREATE TABLE `ROUTINE` (
  `rtn_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `model` varchar(45) NOT NULL,
  PRIMARY KEY (`rtn_id`),
  UNIQUE KEY `rtn_id_UNIQUE` (`rtn_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- DriveTech.TASK definition

CREATE TABLE `TASK` (
  `task_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  `frequency` int NOT NULL COMMENT 'frequency in days ',
  `num_of_attrib` decimal(10,0) DEFAULT NULL,
  `attrib_names` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `req_image` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- DriveTech.`USER` definition

CREATE TABLE `USER` (
  `user_id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- DriveTech.CAR_LOG definition

CREATE TABLE `CAR_LOG` (
  `log_id` int NOT NULL,
  `car_id` int NOT NULL,
  `task_id` int NOT NULL,
  `task_value` varchar(45) NOT NULL,
  `rtn_id` int DEFAULT NULL,
  `task_date` datetime NOT NULL,
  `notes` varchar(45) DEFAULT NULL,
  `user` int NOT NULL,
  PRIMARY KEY (`log_id`),
  KEY `usr_id_idx` (`user`),
  KEY `car_id_idx` (`car_id`),
  KEY `log_task_id_fk_idx` (`task_id`),
  KEY `log_rtn_id_fk_idx` (`rtn_id`),
  CONSTRAINT `log_car_id_fk` FOREIGN KEY (`car_id`) REFERENCES `CAR` (`car_id`),
  CONSTRAINT `log_usr_id_fk` FOREIGN KEY (`user`) REFERENCES `USER` (`user_id`)
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