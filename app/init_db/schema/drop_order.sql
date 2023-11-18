-- drop all tables and databases.
DROP TABLE IF EXISTS `Inventory`.`Component_Names`;
DROP TABLE IF EXISTS `Inventory`.`Inventory_Log`;
DROP TABLE IF EXISTS `Organizations`.`User`;
DROP TABLE IF EXISTS `Organizations`.`People`;
DROP TABLE IF EXISTS `Formulas`.`Primary_Group`;
DROP TABLE IF EXISTS `Formulas`.`Secondary_Group`;
DROP TABLE IF EXISTS `Formulas`.`Tertiary_Group`;
DROP TABLE IF EXISTS `Formulas`.`Quaternary_Group`;
DROP TABLE IF EXISTS `Formulas`.`Formula_Detail`;
DROP TABLE IF EXISTS `Formulas`.`Formula_Master`;
DROP TABLE IF EXISTS `Orders`.`Purchase_Order_Detail`;
DROP TABLE IF EXISTS `Products`.`Components`;
DROP DATABASE IF EXISTS `Inventory`;
DROP DATABASE IF EXISTS `Orders`;
DROP DATABASE IF EXISTS `Products`;
DROP DATABASE IF EXISTS `Manufacturing`;
DROP DATABASE IF EXISTS `Organizations`;
DROP DATABASE IF EXISTS `Formulas`;

-- drop all functions
DROP FUNCTION IF EXISTS `sys`.`LEVENSHTEIN`;
DROP FUNCTION IF EXISTS `sys`.`LEVENSHTEIN_RATIO`;