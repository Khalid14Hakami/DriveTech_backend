SELECT concat('DROP TABLE IF EXISTS `', table_name, '`;')
FROM information_schema.tables
WHERE table_schema = 'k14h$DriveTech';

SET FOREIGN_KEY_CHECKS = 0