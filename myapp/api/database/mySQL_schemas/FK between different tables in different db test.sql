DROP DATABASE Production_History;
DROP DATABASE Manufacturing_Processes;
DROP DATABASE Purchase_Orders;
CREATE DATABASE Manufacturing_Processes;

CREATE TABLE Manufacturing_Processes.Manufacturing_Process_Master (
  `Process_ID` INT AUTO_INCREMENT,
  `Process_Name` VARCHAR(100),
  `Number_Of_Operators` TINYINT,
  `Process_SOP` VARCHAR(30),
  PRIMARY KEY (`Process_ID`)
);

CREATE DATABASE Purchase_Orders;

CREATE TABLE Purchase_Orders.Production_Runs_Master (
  `Prolifix_Lot_Number` VARCHAR(20),
  `Target_Unit_Yield` INT,
  `Lab_Sample_Sent_Date` DATE,
  `Has_Certificate-Of-Analysis` BOOL,
  PRIMARY KEY (`Prolifix_Lot_Number`)
);

CREATE DATABASE Production_History;

CREATE TABLE Production_History.Production_Runs_Process_Master (
  `Production_Runs_Process_ID` INT AUTO_INCREMENT,
  `Prolifix_Lot_Number` VARCHAR(20),
  `Process_ID` INT,
  `Start_Date` DATE,
  `Finish_Date` DATE,
  PRIMARY KEY (`Production_Runs_Process_ID`),
  FOREIGN KEY (`Prolifix_Lot_Number`) REFERENCES Purchase_Orders.Production_Runs_Master(`Prolifix_Lot_Number`),
  FOREIGN KEY (`Process_ID`) REFERENCES Manufacturing_Processes.Manufacturing_Process_Master(`Process_ID`)
);
