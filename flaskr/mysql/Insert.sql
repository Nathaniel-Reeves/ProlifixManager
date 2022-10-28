
-- Insert Prolifix Nutrition Information
INSERT INTO `Organizations`.`Organizations` (`Organization_Name`, `Organization_Initial`, `Website`, `HQ_Street_Address`, `HQ_Unit_Apt`, 
	`HQ_City`, `HQ_Region`, `HQ_Country`, `HQ_Zip_Code`, `Country_Origin`, `Ship_Time_In_Days`, `Roll`) VALUES (
    "Prolifix Nutrition", "PLX", "https://www.prolifixnutrition.com/", "696 South 5300 W", "#1", "Hurricane", "Utah", "United States", "84737", "United States", 0, "Prolifix");

-- Some Client Information
INSERT INTO `Organizations`.`Organizations` (`Organization_Name`, `Organization_Initial`, `Roll`) VALUES ("Markus", "MK", 'Client');
INSERT INTO `Organizations`.`Organizations` (`Organization_Name`, `Organization_Initial`, `Roll`) VALUES ("Maju", "MJ", 'Client');
INSERT INTO `Organizations`.`Organizations` (`Organization_Name`, `Organization_Initial`, `Roll`) VALUES ("Herbally Grounded", "MG", 'Client');

-- Some Supplier Information
INSERT INTO `Organizations`.`Organizations` (`Organization_Name`, `Organization_Initial`, `Roll`) VALUES ("Equadorian Rainforest", "ER", 'Supplier');
INSERT INTO `Organizations`.`Organizations` (`Organization_Name`, `Organization_Initial`, `Roll`) VALUES ("Stryka", "SK", 'Supplier');
INSERT INTO `Organizations`.`Organizations` (`Organization_Name`, `Organization_Initial`, `Roll`) VALUES ("Ingredients Online", "IO", 'Supplier');

-- Insert Nathaniel Reeves Person Info
INSERT INTO `Organizations`.`People` (`Organization_ID`, `First_Name`, `Last_Name`, `Job_Title`, `Phone_Number`, `Email_Address`, `Is_Employee`, `Wage`, `Contract_Date`) VALUES 
	(1, "Nathaniel", "Reeves", "Developer", "8013801953", "nathaniel.jacob.reeves@gmail.com", true, 18.50, '2020-6-16');

-- Insert Nathaniel Reeves User Info  (Password = Newspaper5)
INSERT INTO `Organizations`.`User` (`Person_ID`, `Username`, `Encrypted_Password`, `Access_Privileges`) VALUES (1, "nathanielr", "pbkdf2:sha256:150000$sOQU7umo$0bfe5482ab1c01c17fbd0296dc9372e8d949eaea60a45264463da86005a036d0", "Dev");

-- Insert Kathy Jensen Person Info
INSERT INTO `Organizations`.`People` (`Organization_ID`, `First_Name`, `Last_Name`, `Job_Title`, `Phone_Number`, `Email_Address`, `Is_Employee`, `Wage`, `Contract_Date`) VALUES 
	(1, "Kathy", "Jensen", "Owner", "8016025244 ", "Info@holisticlifesupplements.com", true, 0, '2016-1-1');

-- Insert Kathy Jensen User Info  (Password = password)
INSERT INTO `Organizations`.`User` (`Person_ID`, `Username`, `Encrypted_Password`, `Access_Privileges`) VALUES (2, "kathyj", "pbkdf2:sha256:260000$D8qPhRKS15pNXdWb$7bd4d1a2603d4365d0711b7342a1a59f67fad6354b8424e574d0654cf276ec5c", "Owner");

-- Insert Ian Bull Person Info
INSERT INTO `Organizations`.`People` (`Organization_ID`, `First_Name`, `Last_Name`, `Job_Title`, `Phone_Number`, `Email_Address`, `Is_Employee`, `Wage`, `Contract_Date`) VALUES 
	(1, "Ian", "Bull", "Manager", "9285645378", "ianbullpn@gmail.com", true, 0, '2017-11-01');

-- Insert Ian Bull User Info  (Password = password)
INSERT INTO `Organizations`.`User` (`Person_ID`, `Username`, `Encrypted_Password`, `Access_Privileges`) VALUES (3, "Ianb", "pbkdf2:sha256:260000$D8qPhRKS15pNXdWb$7bd4d1a2603d4365d0711b7342a1a59f67fad6354b8424e574d0654cf276ec5c", "Manager");


SELECT * FROM `Organizations`.`People`;