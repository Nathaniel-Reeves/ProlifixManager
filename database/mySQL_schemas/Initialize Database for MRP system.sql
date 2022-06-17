-- SET autocommit = 0;
-- DROP DATABASE Test;
-- CREATE DATABASE Test;
START TRANSACTION;
CREATE TABLE `Clients_Master` (
  `Client_ID` INT AUTO_INCREMENT,
  `Client_Name` VARCHAR(200),
  `Client_Initial` VARCHAR(10),
  PRIMARY KEY (`Client_ID`)
);

CREATE TABLE `Purchase_Order_Number_Master` (
  `Prefix` VARCHAR(10),
  `Year` TINYINT,
  `Month` TINYINT,
  `Sec_number` SMALLINT,
  `CONCAT_PO` VARCHAR(15),
  `Client_ID` INT,
  `Client_Purchase_Order_Number` VARCHAR(30),
  `Order_Date` DATE,
  `Expected_Completion_Date` DATE,
  `Order_Finish_Date` DATE,
  PRIMARY KEY (`Prefix`, `Year`, `Month`, `Sec_number`),
  FOREIGN KEY (`Client_ID`) REFERENCES `Clients_Master`(`Client_ID`)
);

CREATE TABLE `Products_Master` (
  `Product_ID` INT AUTO_INCREMENT,
  `Client_ID` INT,
  `Product_Name` VARCHAR(200),
  `Type` Enum('Powder',' Capsule', 'Liquid'),
  `Current_Product` BOOL,
  `Date_Created` DATE,
  PRIMARY KEY (`Product_ID`),
  FOREIGN KEY (`Client_ID`) REFERENCES `Clients_Master`(`Client_ID`)
);

CREATE TABLE `Production_Runs_Detail` (
  `Prolifix_Lot` INT,
  `Target_Unit_Yield` INT,
  `Batch_Date` DATE,
  `Target_Kilo_Yield` DOUBLE,
  `Batch_Actual` DOUBLE,
  `Additional_Ingredient_Added` DOUBLE,
  `Screen_Date` DATE,
  `Screen_Yield` DOUBLE,
  `Blend_Date` DATE,
  `Blend_Yield` DOUBLE,
  `Lab_Sample_Sent_Date` DATE,
  `Has_Certificate-Of-Analysis` BOOL,
  `Encapsulation_Date` DATE,
  `Ave_Gross_Cap_Weight` DOUBLE,
  `Ave_Empty_Cap_Weight` DOUBLE,
  `Sort_Date` DATE,
  `Fill_Date` DATE,
  `Capsules_Per_Unit` INT,
  `Grams_Per_Unit` DOUBLE,
  `Liquid_Fill_Start_Date` DATE,
  `Liquid_Fill_Finish_Date` DATE,
  `Labeled_Date` DATE,
  `Total_Production_Yield` INT,
  `Retention_in_Grams` DOUBLE,
  `Retention_in_Units` INT,
  `Production_Notes` VARCHAR(1000),
  `QC_Visual` VARCHAR(50),
  `QC_Odor` VARCHAR(50),
  `QC_Taste` VARCHAR(50),
  `QC_Taste_Dissolved` VARCHAR(50),
  `QC_Texture` VARCHAR(50),
  `LAB_Total_Plate_Count` INT,
  `LAB_Coliform_Count` INT,
  `LAB_EColi_Count` INT,
  `LAB_Staph_Count` INT,
  `LAB_Samonella_Count` INT,
  `LAB_Yeast_Count` INT,
  `LAB_Mold_Count` INT,
  `LAB_Moisture_%` DOUBLE,
  `LAB_Mercury_ppm` DOUBLE,
  `LAB_Lead_ppm` DOUBLE,
  `LAB_Cadmium_ppm` DOUBLE,
  `LAB_Arsenic_ppm` DOUBLE,
  PRIMARY KEY (`Prolifix_Lot`),
  FOREIGN KEY (`LAB_Moisture_%`) REFERENCES `Products_Master`(`Product_Name`)
);

CREATE TABLE `Production_Runs_Master` (
  `Prefix` VARCHAR(15),
  `Year` TINYINT,
  `Month` TINYINT,
  `Sec_number` SMALLINT AUTO_INCREMENT,
  `Suffix` VARCHAR(15),
  `CONCAT_Prolifix_Lot` VARCHAR(40),
  `Purchase_Order_Number` VARCHAR(15),
  `Product_ID` INT,
  PRIMARY KEY (`Prefix`, `Year`, `Month`, `Sec_number`, `Suffix`),
  FOREIGN KEY (`Purchase_Order_Number`) REFERENCES `Purchase_Order_Number_Master`(`CONCAT_PO`),
  FOREIGN KEY (`Product_ID`) REFERENCES `Production_Runs_Detail`(`LAB_Arsenic_ppm`)
);

CREATE TABLE `Materials_Suppliers_Master` (
  `Supplier_ID` INT AUTO_INCREMENT,
  `Supplier_Name` VARCHAR(200),
  `Supplier_Initial` VARCHAR(20),
  `Date_Entered` DATE,
  `Sale_Person` VARCHAR(100),
  `Website` VARCHAR(500),
  `Contact` VARCHAR(100),
  PRIMARY KEY (`Supplier_ID`)
);

CREATE TABLE `Materials_Master` (
  `Item_ID` INT AUTO_INCREMENT,
  `Item_Initial` VARCHAR(50),
  `Supplier_Initial` VARCHAR(5),
  `CONCAT_stock_keeping_unit` VARCHAR(100),
  `Date_Entered` DATE,
  `Item_Name` VARCHAR(100),
  `Brand` VARCHAR(100),
  `Category` Enum('Container', 'Label', 'Lid/Cap', 'Misc', 'Packaging', 'Scoop', 'Shipping', 'ShrinkBand'),
  `Contact` VARCHAR(100),
  PRIMARY KEY (`Item_ID`),
  FOREIGN KEY (`Supplier_Initial`) REFERENCES `Materials_Suppliers_Master`(`Supplier_Initial`)
);

CREATE TABLE `Materials_Allocation_Log` (
  `Allocation_ID` INT AUTO_INCREMENT,
  `stock_keeping_unit` VARCHAR(100),
  `Prolifix_Purchase_Order_Number_number` VARCHAR(20),
  `Prolifix_Lot_number` VARCHAR(20),
  `Allocation_Date` DATE,
  `Allocation_Amount` INT,
  PRIMARY KEY (`Allocation_ID`),
  FOREIGN KEY (`Prolifix_Purchase_Order_Number_number`) REFERENCES `Purchase_Order_Number_Master`(`CONCAT_PO`),
  FOREIGN KEY (`Prolifix_Lot_number`) REFERENCES `Production_Runs_Master`(`Purchase_Order_Number`),
  FOREIGN KEY (`stock_keeping_unit`) REFERENCES `Materials_Master`(`CONCAT_stock_keeping_unit`)
);

CREATE TABLE `Raw_Ingredient_Brand_Master` (
  `Brand_ID` INT AUTO_INCREMENT,
  `Brand_Name` VARCHAR(100),
  `Date_Entered` DATE,
  PRIMARY KEY (`Brand_ID`)
);

CREATE TABLE `Raw_Ingredient_Master` (
  `Ingredient_Spec_ID` INT,
  `Ingredient_Name` VARCHAR(100),
  `Brand_ID` VARCHAR(100),
  `Category` Enum('Organic', 'Non-Organic', 'Vitamin&Mineral'),
  `Date_Entered` DATE,
  `Ingredient_Notes` VARCHAR(1000),
  `QC_Visual` VARCHAR(50),
  `QC_Odor` VARCHAR(50),
  `QC_Taste` VARCHAR(50),
  `QC_Taste_Dissolved` VARCHAR(50),
  `QC_Texture` VARCHAR(50),
  `LAB_Total_Plate_Count` INT,
  `LAB_Coliform_Count` INT,
  `LAB_EColi_Count` INT,
  `LAB_Staph_Count` INT,
  `LAB_Samonella_Count` INT,
  `LAB_Yeast_Count` INT,
  `LAB_Mold_Count` INT,
  `LAB_Moisture_%` DOUBLE,
  `LAB_Mercury_ppm` DOUBLE,
  `LAB_Lead_ppm` DOUBLE,
  `LAB_Cadmium_ppm` DOUBLE,
  `LAB_Arsenic_ppm` DOUBLE,
  PRIMARY KEY (`Ingredient_Spec_ID`),
  FOREIGN KEY (`Brand_ID`) REFERENCES `Raw_Ingredient_Brand_Master`(`Brand_ID`)
);

CREATE TABLE `Ingredient_Supplier_Master` (
  `Supplier_ID` INT AUTO_INCREMENT,
  `Supplier_Name` VARCHAR(200),
  `Supplier_Initial` VARCHAR(10),
  `Date_Entered` DATE,
  `Sales_Person` VARCHAR(100),
  `Website` VARCHAR(200),
  `Contact` VARCHAR(100),
  `Vetted` BOOL,
  `Date_Vetted` DATE,
  PRIMARY KEY (`Supplier_ID`)
);

CREATE TABLE `Raw_Ingredient_Order_Log` (
  `Order_number` INT AUTO_INCREMENT,
  `Ingredient_Name` VARCHAR(100),
  `Supplier_ID` INT,
  `Cost_Per_Kilo` DOUBLE,
  `Shipping_Cost` DOUBLE,
  `Date_Ordered` DATE,
  `Kilos_Ordered` DOUBLE,
  `Outstanding_Order` BOOL ,
  PRIMARY KEY (`Order_number`),
  FOREIGN KEY (`Supplier_ID`) REFERENCES `Ingredient_Supplier_Master`(`Supplier_ID`),
  FOREIGN KEY (`Ingredient_Name`) REFERENCES `Raw_Ingredient_Master`(`Ingredient_Spec_ID`)
);

CREATE TABLE `Raw_Ingredient_Check-in_Log` (
  `Check-in_ID` INT AUTO_INCREMENT,
  `Order_number` VARCHAR(100),
  `Lot_number` VARCHAR(100),
  `Check-in_Date` DATE,
  `Check-in_Kilos` DOUBLE,
  PRIMARY KEY (`Check-in_ID`),
  FOREIGN KEY (`Order_number`) REFERENCES `Raw_Ingredient_Order_Log`(`Order_number`)
);

CREATE TABLE `Raw_Ingredient_Detail` (
  `Ingredient_ID` VARCHAR(100),
  `Ingredient_Spec_ID` INT,
  `Lot_number` VARCHAR(100),
  `Supplier_ID` INT,
  `CONCAT_stock_keeping_unit` VARCHAR(100),
  `Has_Certificate-Of-Analysis` BOOL,
  `Ingredient_Notes` VARCHAR(1000),
  `QC_Visual` VARCHAR(50),
  `QC_Odor` VARCHAR(50),
  `QC_Taste` VARCHAR(50),
  `QC_Taste_Dissolved` VARCHAR(50),
  `QC_Texture` VARCHAR(50),
  `LAB_Total_Plate_Count` INT,
  `LAB_Coliform_Count` INT,
  `LAB_EColi_Count` INT,
  `LAB_Staph_Count` INT,
  `LAB_Samonella_Count` INT,
  `LAB_Yeast_Count` INT,
  `LAB_Mold_Count` INT,
  `LAB_Moisture_%` DOUBLE,
  `LAB_Mercury_ppm` DOUBLE,
  `LAB_Lead_ppm` DOUBLE,
  `LAB_Cadmium_ppm` DOUBLE,
  `LAB_Arsenic_ppm` DOUBLE,
  `Floor_Inventory` DOUBLE,
  `Theoretical_Inventory` DOUBLE,
  `Cycle_Count_ID` INT,
  PRIMARY KEY (`Ingredient_ID`),
  FOREIGN KEY (`Ingredient_Spec_ID`) REFERENCES `Raw_Ingredient_Master`(`Ingredient_Spec_ID`),
  FOREIGN KEY (`Supplier_ID`) REFERENCES `Ingredient_Supplier_Master`(`Supplier_ID`),
  FOREIGN KEY (`Lot_number`) REFERENCES `Raw_Ingredient_Check-in_Log`(`Lot_number`)
);

CREATE TABLE `Raw_Ingredient_Allocation_Log` (
  `Allocation_number` INT AUTO_INCREMENT,
  `Prolifix_Lot_number` VARCHAR(100),
  `stock_keeping_unit` VARCHAR(100),
  `Kilos_Allocated` DOUBLE,
  `Date_Allocated` DATE,
  PRIMARY KEY (`Allocation_number`),
  FOREIGN KEY (`stock_keeping_unit`) REFERENCES `Raw_Ingredient_Detail`(`CONCAT_stock_keeping_unit`),
  FOREIGN KEY (`Prolifix_Lot_number`) REFERENCES `Production_Runs_Master`(`CONCAT_Prolifix_Lot`)
);

CREATE TABLE `Raw_Ingredient_Check-out_Log` (
  `Check-in_ID` INT AUTO_INCREMENT,
  `Allocation_number` VARCHAR(100),
  `stock_keeping_unit` VARCHAR(100),
  `Check-out_Date` DATE,
  `Check-out_Kilos` DOUBLE,
  PRIMARY KEY (`Check-in_ID`),
  FOREIGN KEY (`Allocation_number`) REFERENCES `Raw_Ingredient_Allocation_Log`(`Allocation_number`),
  FOREIGN KEY (`stock_keeping_unit`) REFERENCES `Raw_Ingredient_Detail`(`CONCAT_stock_keeping_unit`)
);

CREATE TABLE `Raw_Ingredient_Cycle_Count_Log` (
  `Raw_Ingredient_Cycle_Count_ID` INT AUTO_INCREMENT,
  `stock_keeping_unit` VARCHAR(100),
  `Original_Theoretical_Inventory` DOUBLE,
  `Cycle_Count_Date` DATE,
  `Amount_Counted` DOUBLE,
  `Cycle_Count_Grade` BOOL,
  PRIMARY KEY (`Raw_Ingredient_Cycle_Count_ID`),
  FOREIGN KEY (`stock_keeping_unit`) REFERENCES `Raw_Ingredient_Detail`(`CONCAT_stock_keeping_unit`)
);

CREATE TABLE `Product_Batch_Master` (
  `Batch_ID` INT AUTO_INCREMENT,
  `Product_ID` INT,
  `Default_Batch` BOOL,
  `Date_Created` DATE,
  PRIMARY KEY (`Batch_ID`),
  FOREIGN KEY (`Product_ID`) REFERENCES `Products_Master`(`Product_ID`)
);

CREATE TABLE `Client_Product_Check-in_Log` (
  `Item_Check-in_ID` INT AUTO_INCREMENT,
  `Prolifix_Lot` VARCHAR(20),
  `Floor_Inventory_Before_Check-in` INT,
  `Production_Yield` INT,
  `Check-out_Date` DATE,
  PRIMARY KEY (`Item_Check-in_ID`),
  FOREIGN KEY (`Prolifix_Lot`) REFERENCES `Production_Runs_Master`(`CONCAT_Prolifix_Lot`)
);

CREATE TABLE `Product_Components` (
  `Product_Components_ID` INT AUTO_INCREMENT,
  `Product_ID` INT,
  `Default_Components` BOOL,
  `Date_Created` DATE,
  PRIMARY KEY (`Product_Components_ID`),
  FOREIGN KEY (`Product_ID`) REFERENCES `Products_Master`(`Product_ID`)
);

CREATE TABLE `Client_Product_Cycle_Counts_Log` (
  `Product_Cycle_Counts_ID` INT AUTO_INCREMENT,
  `Prolifix_Lot` VARCHAR(20),
  `Theoretical_Inventory` INT,
  `Cycle_Count_Date` DATE,
  `Amount_Counted` INT,
  `Cycle_Count_Grade` BOOL,
  PRIMARY KEY (`Product_Cycle_Counts_ID`),
  FOREIGN KEY (`Theoretical_Inventory`) REFERENCES `Production_Runs_Master`(`CONCAT_Prolifix_Lot`)
);

CREATE TABLE `Client_Product_Inventory` (
  `Product_Inventory_ID` INT AUTO_INCREMENT,
  `Prolifix_Lot` VARCHAR(20),
  `Floor_Inventory` INT,
  `Theoretical_Inventory` INT,
  `Recent_Cycle_Count_ID` INT,
  PRIMARY KEY (`Product_Inventory_ID`),
  FOREIGN KEY (`Prolifix_Lot`) REFERENCES `Production_Runs_Master`(`CONCAT_Prolifix_Lot`)
);

CREATE TABLE `Client_Product_Check-out_Log` (
  `Product_Check-out_ID` INT AUTO_INCREMENT,
  `Prolifix_Lot` VARCHAR(20),
  `Floor_Inventory_Before_Check-out` INT,
  `Products_Shipped` INT,
  `Check-out_Date` DATE,
  PRIMARY KEY (`Product_Check-out_ID`),
  FOREIGN KEY (`Prolifix_Lot`) REFERENCES `Production_Runs_Master`(`CONCAT_Prolifix_Lot`)
);

CREATE TABLE `Product_Detail` (
  `Product_ID` INT,
  `Expiration_Timeperiod` INT,
  `Sample_Size` TINYINT,
  `Lab_SIze` DOUBLE,
  `Mg_Per_Cap` DOUBLE,
  `Empty_Cap_Mg` DOUBLE,
  `Capsule_Count_per_Unit` INT,
  `Target_Powder_Fill` DOUBLE,
  `Min_Powder_Fill` DOUBLE,
  `Max_Powder_Fill` DOUBLE,
  `Overage_Coefficient` DOUBLE,
  `Screen_Loss_Coefficient` DOUBLE,
  `Blend_Loss_Coefficient` DOUBLE,
  `FIll_Loss_Coefficient` DOUBLE,
  `Spec_Issue_Date` DATE,
  `Spec_Revise_Date` DATE,
  `QC_Visual` VARCHAR(50),
  `QC_Odor` VARCHAR(50),
  `QC_Taste` VARCHAR(50),
  `QC_Taste_Dissolved` VARCHAR(50),
  `QC_Texture` VARCHAR(50),
  `LAB_Total_Plate_Count` INT,
  `LAB_Coliform_Count` INT,
  `LAB_EColi_Count` INT,
  `LAB_Staph_Count` INT,
  `LAB_Samonella_Count` INT,
  `LAB_Yeast_Count` INT,
  `LAB_Mold_Count` INT,
  `LAB_Moisture_%` DOUBLE,
  `LAB_Mercury_ppm` DOUBLE,
  `LAB_Lead_ppm` DOUBLE,
  `LAB_Cadmium_ppm` DOUBLE,
  `LAB_Arsenic_ppm` DOUBLE,
  PRIMARY KEY (`Product_ID`)
);

CREATE TABLE `Product_In_Process_Specs_Master` (
  `In_Process_Spec_ID` INT AUTO_INCREMENT,
  `Product_ID` INT,
  `Default_Process` BOOL,
  `Date_Created` DATE,
  PRIMARY KEY (`In_Process_Spec_ID`),
  FOREIGN KEY (`Product_ID`) REFERENCES `Products_Master`(`Product_ID`)
);

CREATE TABLE `Product_In_Processd_Spec_Detail` (
  `Process_ID` INT AUTO_INCREMENT,
  `In_Process_Spec_ID` INT,
  `Default_Components` BOOL,
  `Equipment_ID` INT,
  `Date_Created` DATE,
  PRIMARY KEY (`Process_ID`),
  FOREIGN KEY (`In_Process_Spec_ID`) REFERENCES `Product_In_Process_Specs_Master`(`In_Process_Spec_ID`)
);

CREATE TABLE `Materials_Check-out_Log` (
  `Item_Check-out_ID` INT AUTO_INCREMENT,
  `stock_keeping_unit` VARCHAR(100),
  `Allocation_ID` VARCHAR(20),
  `Check-out_Date` DATE,
  `Check-out_Amount` INT,
  PRIMARY KEY (`Item_Check-out_ID`),
  FOREIGN KEY (`stock_keeping_unit`) REFERENCES `Materials_Master`(`CONCAT_stock_keeping_unit`)
);

CREATE TABLE `Client_Purchase_Order_Detail` (
  `Purchase_Order_Number_Detail_ID` INT AUTO_INCREMENT,
  `Prolifix_PO` VARCHAR(15),
  `Product_ID` INT,
  `Unit_Order_Qty` INT,
  `Kilos_Order_Qty` DOUBLE(100,2),
  PRIMARY KEY (`Purchase_Order_Number_Detail_ID`),
  FOREIGN KEY (`Prolifix_PO`) REFERENCES `Purchase_Order_Number_Master`(`CONCAT_PO`)
);

CREATE TABLE `Materials_Order_List` (
  `Order_number` INT AUTO_INCREMENT,
  `Item_ID` VARCHAR(100),
  `Supplier_ID` VARCHAR(200),
  `Cost_Per_Unit` DOUBLE(100,2),
  `Shipping_Cost` DOUBLE(100,2),
  `Date_Ordered` DATE,
  `Amount_Ordered` INT,
  `Outstanding_Order` BOOL,
  PRIMARY KEY (`Order_number`),
  FOREIGN KEY (`Item_ID`) REFERENCES `Materials_Master`(`Item_ID`),
  FOREIGN KEY (`Supplier_ID`) REFERENCES `Materials_Suppliers_Master`(`Supplier_ID`)
);

CREATE TABLE `Materials_Inventory_Detail` (
  `stock_keeping_unit` VARCHAR(100),
  `Floor_Inventory` INT,
  `Theoretic_Inventory` INT,
  `Last_Cycle_Count_ID` INT,
  PRIMARY KEY (`stock_keeping_unit`)
);

CREATE TABLE `Product_Individual_Components` (
  `Product_Individual_Components_ID` INT AUTO_INCREMENT,
  `stock_keeping_unit` VARCHAR(100),
  `Product_Components_ID` INT,
  `Component_Qty_Per_Unit` INT,
  PRIMARY KEY (`Product_Individual_Components_ID`),
  FOREIGN KEY (`stock_keeping_unit`) REFERENCES `Materials_Master`(`CONCAT_stock_keeping_unit`),
  FOREIGN KEY (`Product_Components_ID`) REFERENCES `Product_Components`(`Product_Components_ID`)
);

CREATE TABLE `Product_Batch_Detail` (
  `Ingredient_ID` INT AUTO_INCREMENT,
  `Batch_ID` INT,
  `Ingredient_Spec_ID` BOOL,
  `Prefered_Brand` DATE,
  `Percent` DOUBLE,
  PRIMARY KEY (`Ingredient_ID`),
  FOREIGN KEY (`Ingredient_Spec_ID`) REFERENCES `Raw_Ingredient_Master`(`Ingredient_Spec_ID`),
  FOREIGN KEY (`Batch_ID`) REFERENCES `Product_Batch_Master`(`Batch_ID`)
);

CREATE TABLE `Materials_Inventory_Cycle_Count_Log` (
  `Cycle_Count_ID` INT AUTO_INCREMENT,
  `stock_keeping_unit` VARCHAR(100),
  `Original_theoretical_Inventory` INT,
  `Cycle_Count_Date` DATE,
  `Amount_Counted` INT,
  `Cycle_Count_Grade` BOOL,
  PRIMARY KEY (`Cycle_Count_ID`),
  FOREIGN KEY (`Cycle_Count_ID`) REFERENCES `Materials_Inventory_Detail`(`Last_Cycle_Count_ID`),
  FOREIGN KEY (`stock_keeping_unit`) REFERENCES `Materials_Master`(`CONCAT_stock_keeping_unit`)
);

CREATE TABLE `Materials_Check-in_Log` (
  `Item_Check-in_ID` INT AUTO_INCREMENT,
  `Order_number` INT,
  `stock_keeping_unit` VARCHAR(200),
  `Check-in_Date` DATE,
  `Check-in_Amount` INT,
  `Date_Ordered` DATE,
  `Amount_Ordered` INT,
  `Outstanding_Order` BOOL,
  PRIMARY KEY (`Item_Check-in_ID`),
  FOREIGN KEY (`stock_keeping_unit`) REFERENCES `Materials_Master`(`CONCAT_stock_keeping_unit`),
  FOREIGN KEY (`Order_number`) REFERENCES `Materials_Order_List`(`Order_number`)
);
COMMIT;
