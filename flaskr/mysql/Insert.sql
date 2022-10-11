
-- Insert Prolifix Nutrition Information
INSERT INTO `Organizations`.`Organizations` (`Organization_Name`, `Organization_Initial`, `Website`, `HQ_Street_Address`, `HQ_Unit-Apt`, 
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

-- Insert Nathaniel Reeves User Info  (Password = testpassword)
INSERT INTO `Organizations`.`User` (`Person_ID`, `Username`, `Encrypted_Password`, `Access_Privileges`) VALUES (1, "nreeves", "pbkdf2:sha256:260000$xwmRNkYGEsbVxWQk$598deee9e52133d7d3a96eeb060c81f90b06d3ea17fb705b1e834855f5234df6", "Dev");

-- Insert Kathy Jensen Person Info
INSERT INTO `Organizations`.`People` (`Organization_ID`, `First_Name`, `Last_Name`, `Job_Title`, `Phone_Number`, `Email_Address`, `Is_Employee`, `Wage`, `Contract_Date`) VALUES 
	(1, "Kathy", "Jensen", "Owner", "8016025244 ", "Info@holisticlifesupplements.com", true, 0, '2016-1-1');

-- Insert Kathy Jensen User Info  (Password = password)
INSERT INTO `Organizations`.`User` (`Person_ID`, `Username`, `Encrypted_Password`, `Access_Privileges`) VALUES (2, "kathyj", "pbkdf2:sha256:260000$D8qPhRKS15pNXdWb$7bd4d1a2603d4365d0711b7342a1a59f67fad6354b8424e574d0654cf276ec5c", "Owner");


