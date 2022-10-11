-- Refresh Databases
DROP TABLE IF EXISTS `Inventory`.`Check-in_Log`;
DROP TABLE IF EXISTS `Inventory`.`Check-out_Log`;
DROP TABLE IF EXISTS `Inventory`.`Cycle_Counts_Log`;
DROP TABLE IF EXISTS `Organizations`.`User`;
DROP TABLE IF EXISTS `Organizations`.`People`;
DROP TABLE IF EXISTS `Products`.`Components`;
DROP DATABASE IF EXISTS `Inventory`;
DROP DATABASE IF EXISTS `Orders`;
DROP DATABASE IF EXISTS `Products`;
DROP DATABASE IF EXISTS `Manufacturing`;
DROP DATABASE IF EXISTS `Organizations`;


CREATE DATABASE `Organizations`;
CREATE DATABASE `Inventory`;
CREATE DATABASE `Products`;
CREATE DATABASE `Manufacturing`;
CREATE DATABASE `Orders`;

CREATE TABLE `Organizations`.`Organizations` (
  `Organization_ID` INT AUTO_INCREMENT,
  `Organization_Name` VARCHAR(200) NOT NULL,
  `Organization_Initial` VARCHAR(10) NOT NULL,
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Website` VARCHAR(200),
  `Vetted` BOOL,
  `Date_Vetted` DATE,
  `Risk_Level` INT,
  `HQ_Street_Address` VARCHAR(500),
  `HQ_Unit-Apt` VARCHAR(20),
  `HQ_City` VARCHAR(300),
  `HQ_Region` VARCHAR(300),
  `HQ_Country` VARCHAR(300),
  `HQ_Zip_Code` VARCHAR(20),
  `Country_Origin` VARCHAR(300),
  `Ship_Time_In_Days` INT,
  `Roll` ENUM('Prolifix', 'Client', 'Supplier'),
  `Documents` JSON,
  PRIMARY KEY (`Organization_ID`)
);

CREATE TABLE `Products`.`Product_Master` (
  `Product_ID` VARCHAR(250),
  `Organization_ID` INT,
  `Product_Name` VARCHAR(300) NOT NULL,
  `Type` ENUM('Powder',' Capsule', 'Liquid','NS'),
  `Current_Product` BOOL,
  `Label_ID` VARCHAR(250),
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Spec_Issue_Date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Spec_Revise_Date` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `Products_Collection` JSON,
  `Exp_Time_Frame` SMALLINT,
  `Exp_Unit` ENUM('Years','Months','Days'),
  `Exp_Type` ENUM('Best By', 'Exp'),
  PRIMARY KEY (`Product_ID`),
  FOREIGN KEY (`Organization_ID`) REFERENCES `Organizations`.`Organizations`(`Organization_ID`)
);

CREATE TABLE `Inventory`.`Components` (
  `Component_ID` VARCHAR(250),
  `Component_Name` VARCHAR(300),
  `Brand_ID` INT,
  `Category` Enum('Organic Powder', 'Non-Organic Powder', 'Jar/Container', 'Bag', 'Shrink Band', 'Lid/Cap', 'Label', 'Capsule', 'MISC', 'Scoop', 'Desicant', 'Box/Carton', 'Packaging Material'),
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Client_Owned` INT,
  `Supplier_ID` INT,
  `Component_Collection` JSON,
  PRIMARY KEY (`Component_ID`),
  FOREIGN KEY (`Supplier_ID`) REFERENCES `Organizations`.`Organizations`(`Organization_ID`),
  FOREIGN KEY (`Client_Owned`) REFERENCES `Organizations`.`Organizations`(`Organization_ID`),
  FOREIGN KEY (`Brand_ID`) REFERENCES `Organizations`.`Organizations`(`Organization_ID`)
);

CREATE TABLE `Inventory`.`Inventory` (
  `Inv_ID` INT AUTO_INCREMENT,
  `Item_ID` VARCHAR(250),
  `Actual_Inventory` DECIMAL(16,4),
  `Theoretical_Inventory` DECIMAL(16,4),
  `Recent_Cycle_Count_ID` INT,
  PRIMARY KEY (`Inv_ID`),
  FOREIGN KEY (`Item_ID`) REFERENCES `Products`.`Product_Master`(`Product_ID`),
  FOREIGN KEY (`Item_ID`) REFERENCES `Inventory`.`Components`(`Component_ID`)
);

CREATE TABLE `Organizations`.`User` (
  `User_ID` INT AUTO_INCREMENT,
  `Person_ID` INT,
  `Username` VARCHAR(100) UNIQUE NOT NULL,
  `Encrypted_Password` VARCHAR(250) NOT NULL,
  `Access_Privileges` ENUM('Dev', 'Owner', 'Manager', 'Client', 'Staff'),
  PRIMARY KEY (`User_ID`)
);

CREATE TABLE `Inventory`.`Check-in_Log` (
  `CheckIN_ID` INT AUTO_INCREMENT,
  `Inv_ID` INT,
  `Amount` DECIMAL(16,4),
  `Status` JSON,
  `User_ID` INT,
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Date_Modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`CheckIN_ID`),
  FOREIGN KEY (`Inv_ID`) REFERENCES `Inventory`.`Inventory`(`Inv_ID`),
  FOREIGN KEY (`User_ID`) REFERENCES `Organizations`.`User`(`User_ID`)
);

CREATE TABLE `Inventory`.`Cycle_Counts_Log` (
  `Cycle_Count_ID` INT AUTO_INCREMENT,
  `Inv_ID` INT,
  `Actual_Inventory_Precheck` DECIMAL(16,4),
  `Cycle_Count_Date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Amount_Counted` DECIMAL(16,4),
  `Cycle_Count_Grade` BOOL NOT NULL,
  `User_ID` INT,
  `Fixed_Actual_Inventory` DECIMAL(16,4) NOT NULL,
  `Notes` VARCHAR(2000),
  PRIMARY KEY (`Cycle_Count_ID`),
  FOREIGN KEY (`Inv_ID`) REFERENCES `Inventory`.`Inventory`(`Inv_ID`),
  FOREIGN KEY (`User_ID`) REFERENCES `Organizations`.`User`(`User_ID`)
);

CREATE TABLE `Inventory`.`Check-out_Log` (
  `CheckOUT_ID` INT AUTO_INCREMENT,
  `Inv_ID` INT,
  `Amount` DECIMAL(16,4),
  `Status` JSON,
  `User_ID` INT,
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Date_Modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`CheckOUT_ID`),
  FOREIGN KEY (`Inv_ID`) REFERENCES `Inventory`.`Inventory`(`Inv_ID`),
  FOREIGN KEY (`User_ID`) REFERENCES `Organizations`.`User`(`User_ID`)
);

CREATE TABLE `Products`.`Manufacturing_Process` (
  `Process_Spec_ID` INT AUTO_INCREMENT,
  `Product_ID` VARCHAR(250),
  `Processes_Collection` JSON,
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Date_Modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `Current_Default_Process` BOOL,
  PRIMARY KEY (`Process_Spec_ID`),
  FOREIGN KEY (`Product_ID`) REFERENCES `Products`.`Product_Master`(`Product_ID`)
);

CREATE TABLE `Manufacturing`.`Processes` (
  `Process_ID` INT AUTO_INCREMENT,
  `Process_Name` VARCHAR(100) NOT NULL,
  `Number_Of_Operators` TINYINT NOT NULL,
  `Process_SOP` VARCHAR(30),
  `Process_Record_Template` JSON,
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Date_Modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`Process_ID`)
);

CREATE TABLE `Organizations`.`People` (
  `Person_ID` INT AUTO_INCREMENT,
  `Organization_ID` INT,
  `First_Name` VARCHAR(100),
  `Last_Name` VARCHAR(100),
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Job_Title` VARCHAR(100),
  `Phone_Number` VARCHAR(500),
  `Email_Address` VARCHAR(100),
  `Is_Employee` BOOL,
  `Wage` INT,
  `Contract_Date` DATE,
  `Termination_Date` DATE,
  PRIMARY KEY (`Person_ID`),
  FOREIGN KEY (`Organization_ID`) REFERENCES `Organizations`.`Organizations`(`Organization_ID`)
);

CREATE TABLE `Orders`.`Purchase_Orders` (
  `Prefix` VARCHAR(10),
  `Year` TINYINT,
  `Month` TINYINT,
  `Sec_Number` SMALLINT,
  `Prolifix_Purchase_Order_ID` VARCHAR(15),
  `Organization_ID` INT,
  `Client_Purchase_Order_Number` VARCHAR(30),
  `Order_Date` DATE,
  `Expected_Completion_Date` DATE,
  `Order_Finish_Date` DATE,
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Prolifix_Purchase_Order_ID`),
  FOREIGN KEY (`Organization_ID`) REFERENCES `Organizations`.`Organizations`(`Organization_ID`)
);

CREATE TABLE `Orders`.`Purchase_Orders_Detail` (
  `PO_Detail_ID` INT AUTO_INCREMENT,
  `Prolifix_Purchase_Order_ID` VARCHAR(15),
  `Product_ID` VARCHAR(250),
  `Unit_Order_Qty` INT,
  `Kilos_Order_Qty` DECIMAL(16,4),
  `Special_Instructions` VARCHAR(2000),
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`PO_Detail_ID`),
  FOREIGN KEY (`Product_ID`) REFERENCES `Products`.`Product_Master`(`Product_ID`),
  FOREIGN KEY (`Prolifix_Purchase_Order_ID`) REFERENCES `Orders`.`Purchase_Orders`(`Prolifix_Purchase_Order_ID`)
);

CREATE TABLE `Orders`.`Lot_Numbers` (
  `Prefix` VARCHAR(15),
  `Year` TINYINT,
  `Month` TINYINT,
  `Sec_Number` SMALLINT,
  `Suffix` VARCHAR(15),
  `Product_ID` VARCHAR(250),
  `Prolifix_Lot_Number` VARCHAR(20),
  `PO_Detail_ID` INT,
  `Target_Unit_Yield` INT,
  `Actual_Unit_Yield` INT,
  `Production_Runs_Collection` JSON,
  `Batch_Printed` BOOL,
  `BPR_Printed` BOOL,
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Exp_Date` DATE,
  `Exp_Type` ENUM('Best By', 'Exp'),
  PRIMARY KEY (`Prolifix_Lot_Number`),
  FOREIGN KEY (`PO_Detail_ID`) REFERENCES `Orders`.`Purchase_Orders_Detail`(`PO_Detail_ID`),
  FOREIGN KEY (`Product_ID`) REFERENCES `Products`.`Product_Master`(`Product_ID`)
);

CREATE TABLE `Products`.`Components` (
  `Component_ID` INT AUTO_INCREMENT,
  `Materials_ID` VARCHAR(250),
  `Product_ID` VARCHAR(250),
  `Material_Qty_Per_Unit` INT NOT NULL,
  `Current_Default_Component` BOOL NOT NULL,
  `Component_List_Version` SMALLINT NOT NULL,
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Component_ID`),
  FOREIGN KEY (`Product_ID`) REFERENCES `Products`.`Product_Master`(`Product_ID`),
  FOREIGN KEY (`Materials_ID`) REFERENCES `Inventory`.`Components`(`Component_ID`)
);

CREATE TABLE `Products`.`Formula` (
  `Formula_ID` INT AUTO_INCREMENT,
  `Product_ID` VARCHAR(250),
  `Ingredient&Brand` JSON,
  `Percent` DOUBLE,
  `Mg_Per_Capsule` DOUBLE,
  `Gram_Per_Unit` DOUBLE,
  `FluOz_Per_Unit` DOUBLE,
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Formulation_Version` SMALLINT,
  `Current_Default_Formula` BOOL,
  PRIMARY KEY (`Formula_ID`),
  FOREIGN KEY (`Product_ID`) REFERENCES `Products`.`Product_Master`(`Product_ID`)
);

CREATE TABLE `Manufacturing`.`Equipment` (
  `Equipment_ID` INT AUTO_INCREMENT,
  `Process_ID` INT,
  `Equipment_SN` VARCHAR(50),
  `Status` ENUM('Working Order', 'Broken', 'Removed'),
  `Date_Entered` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Date_Modified` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  `Equipment_History` JSON,
  PRIMARY KEY (`Equipment_ID`),
  FOREIGN KEY (`Process_ID`) REFERENCES `Manufacturing`.`Processes`(`Process_ID`)
);




