
-- DROP DATABASE Test;
-- CREATE DATABASE Test;

-- DROP DATABASE Test;
-- CREATE DATABASE Test;


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
  `Sec_Number` SMALLINT,
  `Prolifix_Purchase_Order_Number` VARCHAR(15),
  `Client_ID` INT,
  `Client_Purchase_Order_Number` VARCHAR(30),
  `Order_Date` DATE,
  `Expected_Completion_Date` DATE,
  `Order_Finish_Date` DATE,
  PRIMARY KEY (`Prolifix_Purchase_Order_Number`),
  FOREIGN KEY (`Client_ID`) REFERENCES `Clients_Master`(`Client_ID`)
);

CREATE TABLE `Product_Detail` (
  `Product_ID` INT AUTO_INCREMENT,
  `Client_ID` INT,
  `Product_Name` VARCHAR(200),
  `Type` Enum('Powder',' Capsule', 'Liquid'),
  `Current_Product` BOOL,
  `Date_Created` DATE,
  `Expiration_Timeperiod` INT,
  `Sample_Size` TINYINT,
  `Lab_Size` DOUBLE,
  `Mg_Per_Cap` DOUBLE,
  `Empty_Cap_Mg` DOUBLE,
  `Capsule_Count_per_Unit` INT,
  `Target_Powder_Fill` DOUBLE,
  `Min_Powder_Fill` DOUBLE,
  `Max_Powder_Fill` DOUBLE,
  `Overage_Coefficient` DOUBLE,
  `Screen_Loss_Coefficient` DOUBLE,
  `Blend_Loss_Coefficient` DOUBLE,
  `Fill_Loss_Coefficient` DOUBLE,
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
  `LAB_Salmonella_Count` INT,
  `LAB_Yeast_Count` INT,
  `LAB_Mold_Count` INT,
  `LAB_Moisture_%` DOUBLE,
  `LAB_Mercury_ppm` DOUBLE,
  `LAB_Lead_ppm` DOUBLE,
  `LAB_Cadmium_ppm` DOUBLE,
  `LAB_Arsenic_ppm` DOUBLE,
  PRIMARY KEY (`Product_ID`),
  FOREIGN KEY (`Client_ID`) REFERENCES `Clients_Master`(`Client_ID`)
);

CREATE TABLE `Production_Runs_Detail` (
  `Prefix` VARCHAR(15),
  `Year` TINYINT,
  `Month` TINYINT,
  `Sec_Number` SMALLINT,
  `Suffix` VARCHAR(15),
  `Prolifix_Lot_Number` VARCHAR(20),
  `Prolifix_Purchase_Order_Number` VARCHAR(15),
  `Product_ID` INT,
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
  `LAB_Salmonella_Count` INT,
  `LAB_Yeast_Count` INT,
  `LAB_Mold_Count` INT,
  `LAB_Moisture_%` DOUBLE,
  `LAB_Mercury_ppm` DOUBLE,
  `LAB_Lead_ppm` DOUBLE,
  `LAB_Cadmium_ppm` DOUBLE,
  `LAB_Arsenic_ppm` DOUBLE,
  PRIMARY KEY (`Prolifix_Lot_Number`),
  FOREIGN KEY (`Prolifix_Purchase_Order_Number`) REFERENCES `Purchase_Order_Number_Master`(`Prolifix_Purchase_Order_Number`),
  FOREIGN KEY (`Product_ID`) REFERENCES `Product_Detail`(`Product_ID`)
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
  `Supplier_ID` INT,
  `Stock_Keeping_Unit` VARCHAR(100),
  `Date_Entered` DATE,
  `Item_Name` VARCHAR(100),
  `Brand` VARCHAR(100),
  `Category` Enum('Container', 'Label', 'Lid/Cap', 'Misc', 'Packaging', 'Scoop', 'Shipping', 'ShrinkBand'),
  `Contact` VARCHAR(100),
  `Actual_Inventory` INT,
  `Theoretic_Inventory` INT,
  `Last_Cycle_Count_ID` INT,
  PRIMARY KEY (`Item_ID`),
  FOREIGN KEY (`Supplier_ID`) REFERENCES `Materials_Suppliers_Master`(`Supplier_ID`),
  KEY `Key` (`Actual_Inventory`, `Theoretic_Inventory`)
);

CREATE TABLE `Materials_Allocation_Log` (
  `Allocation_ID` INT AUTO_INCREMENT,
  `Item_ID` INT,
  `Prolifix_Purchase_Order_Number` VARCHAR(15),
  `Prolifix_Lot_Number` VARCHAR(20),
  `Allocation_Date` DATE,
  `Allocation_Amount` INT,
  PRIMARY KEY (`Allocation_ID`),
  FOREIGN KEY (`Prolifix_Purchase_Order_Number`) REFERENCES `Purchase_Order_Number_Master`(`Prolifix_Purchase_Order_Number`),
  FOREIGN KEY (`Prolifix_Lot_Number`) REFERENCES `Production_Runs_Detail`(`Prolifix_Purchase_Order_Number`),
  FOREIGN KEY (`Item_ID`) REFERENCES `Materials_Master`(`Item_ID`)
);

CREATE TABLE `Ingredient_Brand_Master` (
  `Brand_ID` INT AUTO_INCREMENT,
  `Brand_Name` VARCHAR(100),
  `Date_Entered` DATE,
  PRIMARY KEY (`Brand_ID`)
);

CREATE TABLE `Ingredient_Master` (
  `Ingredient_Spec_ID` INT,
  `Ingredient_Name` VARCHAR(100),
  `Brand_ID` INT,
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
  FOREIGN KEY (`Brand_ID`) REFERENCES `Ingredient_Brand_Master`(`Brand_ID`)
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

CREATE TABLE `Ingredient_Order_Log` (
  `Order_Number` INT AUTO_INCREMENT,
  `Ingredient_Spec_ID` INT,
  `Supplier_ID` INT,
  `Cost_Per_Kilo` DOUBLE,
  `Shipping_Cost` DOUBLE,
  `Date_Ordered` DATE,
  `Kilos_Ordered` DOUBLE,
  `Outstanding_Order` BOOL ,
  PRIMARY KEY (`Order_Number`),
  FOREIGN KEY (`Supplier_ID`) REFERENCES `Ingredient_Supplier_Master`(`Supplier_ID`),
  FOREIGN KEY (`Ingredient_Spec_ID`) REFERENCES `Ingredient_Master`(`Ingredient_Spec_ID`)
);

CREATE TABLE `Ingredient_Check-in_Log` (
  `Check-in_ID` INT AUTO_INCREMENT,
  `Order_Number` INT,
  `Ingredient_Lot_Number` VARCHAR(100),
  `Check-in_Date` DATE,
  `Check-in_Kilos` DOUBLE,
  PRIMARY KEY (`Check-in_ID`),
  FOREIGN KEY (`Order_Number`) REFERENCES `Ingredient_Order_Log`(`Order_Number`)
);

CREATE TABLE `Ingredient_Detail` (
  `Ingredient_ID` INT,
  `Ingredient_Spec_ID` INT,
  `Check-in_ID` INT,
  `Supplier_ID` INT,
  `Stock_Keeping_Unit` VARCHAR(100),
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
  `Actual_Inventory` DOUBLE,
  `Theoretical_Inventory` DOUBLE,
  PRIMARY KEY (`Ingredient_ID`),
  FOREIGN KEY (`Ingredient_Spec_ID`) REFERENCES `Ingredient_Master`(`Ingredient_Spec_ID`),
  FOREIGN KEY (`Supplier_ID`) REFERENCES `Ingredient_Supplier_Master`(`Supplier_ID`),
  FOREIGN KEY (`Check-in_ID`) REFERENCES `Ingredient_Check-in_Log`(`Check-in_ID`)
);

CREATE TABLE `Ingredient_Allocation_Log` (
  `Allocation_Number` INT AUTO_INCREMENT,
  `Prolifix_Lot_Number` VARCHAR(20),
  `Ingredient_ID` INT,
  `Kilos_Allocated` DOUBLE,
  `Date_Allocated` DATE,
  PRIMARY KEY (`Allocation_Number`),
  FOREIGN KEY (`Ingredient_ID`) REFERENCES `Ingredient_Detail`(`Ingredient_ID`),
  FOREIGN KEY (`Prolifix_Lot_Number`) REFERENCES `Production_Runs_Detail`(`Prolifix_Lot_Number`)
);

CREATE TABLE `Ingredient_Check-out_Log` (
  `Check-in_ID` INT AUTO_INCREMENT,
  `Allocation_Number` INT,
  `Ingredient_ID` INT,
  `Check-out_Date` DATE,
  `Check-out_Kilos` DOUBLE,
  PRIMARY KEY (`Check-in_ID`),
  FOREIGN KEY (`Allocation_Number`) REFERENCES `Ingredient_Allocation_Log`(`Allocation_Number`),
  FOREIGN KEY (`Ingredient_ID`) REFERENCES `Ingredient_Detail`(`Ingredient_ID`)
);

CREATE TABLE `Ingredient_Cycle_Count_Log` (
  `Ingredient_Cycle_Count_ID` INT AUTO_INCREMENT,
  `Ingredient_ID` INT,
  `Original_Theoretical_Inventory` DOUBLE,
  `Cycle_Count_Date` DATE,
  `Amount_Counted` DOUBLE,
  `Cycle_Count_Grade` BOOL,
  PRIMARY KEY (`Ingredient_Cycle_Count_ID`),
  FOREIGN KEY (`Ingredient_ID`) REFERENCES `Ingredient_Detail`(`Ingredient_ID`)
);

CREATE TABLE `Product_Batch_Master` (
  `Batch_ID` INT AUTO_INCREMENT,
  `Product_ID` INT,
  `Default_Batch` BOOL,
  `Date_Created` DATE,
  PRIMARY KEY (`Batch_ID`),
  FOREIGN KEY (`Product_ID`) REFERENCES `Product_Detail`(`Product_ID`)
);

CREATE TABLE `Client_Product_Check-in_Log` (
  `Item_Check-in_ID` INT AUTO_INCREMENT,
  `Prolifix_Lot_Number` VARCHAR(20),
  `Actual_Inventory_Before_Check-in` INT,
  `Production_Yield` INT,
  `Check-out_Date` DATE,
  PRIMARY KEY (`Item_Check-in_ID`),
  FOREIGN KEY (`Prolifix_Lot_Number`) REFERENCES `Production_Runs_Detail`(`Prolifix_Lot_Number`)
);

CREATE TABLE `Product_Components` (
  `Product_Components_ID` INT AUTO_INCREMENT,
  `Product_ID` INT,
  `Default_Components` BOOL,
  `Date_Created` DATE,
  PRIMARY KEY (`Product_Components_ID`),
  FOREIGN KEY (`Product_ID`) REFERENCES `Product_Detail`(`Product_ID`)
);

CREATE TABLE `Client_Product_Cycle_Counts_Log` (
  `Product_Cycle_Counts_ID` INT AUTO_INCREMENT,
  `Prolifix_Lot_Number` VARCHAR(20),
  `Theoretical_Inventory` INT,
  `Cycle_Count_Date` DATE,
  `Amount_Counted` INT,
  `Cycle_Count_Grade` BOOL,
  PRIMARY KEY (`Product_Cycle_Counts_ID`),
  FOREIGN KEY (`Prolifix_Lot_Number`) REFERENCES `Production_Runs_Detail`(`Prolifix_Lot_Number`)
);

CREATE TABLE `Client_Product_Inventory` (
  `Product_Inventory_ID` INT AUTO_INCREMENT,
  `Prolifix_Lot_Number` VARCHAR(20),
  `Actual_Inventory` INT,
  `Theoretical_Inventory` INT,
  `Recent_Cycle_Count_ID` INT,
  PRIMARY KEY (`Product_Inventory_ID`),
  FOREIGN KEY (`Prolifix_Lot_Number`) REFERENCES `Production_Runs_Detail`(`Prolifix_Lot_Number`)
);

CREATE TABLE `Client_Product_Check-out_Log` (
  `Product_Check-out_ID` INT AUTO_INCREMENT,
  `Prolifix_Lot_Number` VARCHAR(20),
  `Actual_Inventory_Before_Check-out` INT,
  `Products_Shipped` INT,
  `Check-out_Date` DATE,
  PRIMARY KEY (`Product_Check-out_ID`),
  FOREIGN KEY (`Prolifix_Lot_Number`) REFERENCES `Production_Runs_Detail`(`Prolifix_Lot_Number`)
);

CREATE TABLE `Product_In_Process_Specs_Master` (
  `In_Process_Spec_ID` INT AUTO_INCREMENT,
  `Product_ID` INT,
  `Default_Process` BOOL,
  `Date_Created` DATE,
  PRIMARY KEY (`In_Process_Spec_ID`),
  FOREIGN KEY (`Product_ID`) REFERENCES `Product_Detail`(`Product_ID`)
);

CREATE TABLE `Product_In_Processed_Spec_Detail` (
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
  `Item_ID` INT,
  `Allocation_ID` INT,
  `Check-out_Date` DATE,
  `Check-out_Amount` INT,
  PRIMARY KEY (`Item_Check-out_ID`),
  FOREIGN KEY (`Allocation_ID`) REFERENCES `Materials_Allocation_Log`(`Allocation_ID`),
  FOREIGN KEY (`Item_ID`) REFERENCES `Materials_Master`(`Item_ID`)
);

CREATE TABLE `Client_Purchase_Order_Detail` (
  `Purchase_Order_Number_Detail_ID` INT AUTO_INCREMENT,
  `Prolifix_Purchase_Order_Number` VARCHAR(15),
  `Product_ID` INT,
  `Unit_Order_Qty` INT,
  `Kilos_Order_Qty` DOUBLE,
  PRIMARY KEY (`Purchase_Order_Number_Detail_ID`),
  FOREIGN KEY (`Prolifix_Purchase_Order_Number`) REFERENCES `Purchase_Order_Number_Master`(`Prolifix_Purchase_Order_Number`)
);

CREATE TABLE `Materials_Order_List` (
  `Order_Number` INT AUTO_INCREMENT,
  `Item_ID` INT,
  `Supplier_ID` INT,
  `Cost_Per_Unit` DOUBLE,
  `Shipping_Cost` DOUBLE,
  `Date_Ordered` DATE,
  `Amount_Ordered` INT,
  `Outstanding_Order` BOOL,
  PRIMARY KEY (`Order_Number`),
  FOREIGN KEY (`Item_ID`) REFERENCES `Materials_Master`(`Item_ID`),
  FOREIGN KEY (`Supplier_ID`) REFERENCES `Materials_Suppliers_Master`(`Supplier_ID`)
);

CREATE TABLE `Product_Individual_Components` (
  `Product_Individual_Components_ID` INT AUTO_INCREMENT,
  `Item_ID` INT,
  `Product_Components_ID` INT,
  `Component_Qty_Per_Unit` INT,
  PRIMARY KEY (`Product_Individual_Components_ID`),
  FOREIGN KEY (`Item_ID`) REFERENCES `Materials_Master`(`Item_ID`),
  FOREIGN KEY (`Product_Components_ID`) REFERENCES `Product_Components`(`Product_Components_ID`)
);

CREATE TABLE `Product_Batch_Detail` (
  `Ingredient_ID` INT AUTO_INCREMENT,
  `Batch_ID` INT,
  `Ingredient_Spec_ID` INT,
  `Prefered_Brand` DATE,
  `Percent` DOUBLE,
  PRIMARY KEY (`Ingredient_ID`),
  FOREIGN KEY (`Ingredient_Spec_ID`) REFERENCES `Ingredient_Master`(`Ingredient_Spec_ID`),
  FOREIGN KEY (`Batch_ID`) REFERENCES `Product_Batch_Master`(`Batch_ID`)
);

CREATE TABLE `Materials_Inventory_Cycle_Count_Log` (
  `Cycle_Count_ID` INT AUTO_INCREMENT,
  `Item_ID` INT,
  `Original_theoretical_Inventory` INT,
  `Cycle_Count_Date` DATE,
  `Amount_Counted` INT,
  `Cycle_Count_Grade` BOOL,
  PRIMARY KEY (`Cycle_Count_ID`),
  FOREIGN KEY (`Item_ID`) REFERENCES `Materials_Master`(`Item_ID`)
);

CREATE TABLE `Materials_Check-in_Log` (
  `Item_Check-in_ID` INT AUTO_INCREMENT,
  `Order_Number` INT,
  `Item_ID` INT,
  `Check-in_Date` DATE,
  `Check-in_Amount` INT,
  `Date_Ordered` DATE,
  `Amount_Ordered` INT,
  `Outstanding_Order` BOOL,
  PRIMARY KEY (`Item_Check-in_ID`),
  FOREIGN KEY (`Item_ID`) REFERENCES `Materials_Master`(`Item_ID`),
  FOREIGN KEY (`Order_Number`) REFERENCES `Materials_Order_List`(`Order_Number`)
);
