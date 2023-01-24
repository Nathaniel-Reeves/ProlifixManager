-- Create Owner and Dev Accounts

-- Insert Prolifix Nutrition Information
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `website`, `supplier`, `client`, `risk_level`) VALUES (
--      "1", "Prolifix Nutrition", "PLX", "https://www.prolifixnutrition.com/", True, True, "No Risk" );

-- -- Some Client Information
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `client`) VALUES ("2", "Markus", "MK", True);
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `client`) VALUES ("3", "Maju", "MJ", True);
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `client`) VALUES ("4", "Herbally Grounded", "MG", True);

-- -- Some Supplier Information
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `supplier`) VALUES ("5", "Equadorian Rainforest", "ER", true);
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `supplier`) VALUES ("6", "Stryka", "SK", true);
-- INSERT INTO `Organizations`.`Organizations` (`organization_id`, `organization_name`, `organization_initial`, `supplier`) VALUES ("7", "Ingredients Online", "IO", true);

-- Insert Nathaniel Reeves Person Info
INSERT INTO `Organizations`.`People` (`organization_id`, `first_name`, `last_name`, `job_title`, `phone_number`, `email_address`, `is_employee`, `hourly_wage`, `contract_date`) VALUES 
	(1, "Nathaniel", "Reeves", "Developer", "8013801953", "nathaniel.jacob.reeves@gmail.com", true, 18.50, '2020-6-16');

-- Insert Nathaniel Reeves User Info  (Password = testpassword)
INSERT INTO `Organizations`.`User` (`user_id`, `person_id`, `username`, `encrypted_password`) VALUES (1, 1, "nreeves", "pbkdf2:sha256:260000$xwmRNkYGEsbVxWQk$598deee9e52133d7d3a96eeb060c81f90b06d3ea17fb705b1e834855f5234df6");
UPDATE `Organizations`.`User` SET `doc` = JSON_SET(`doc`, '$.access_privileges', '{human_resources:manager, client_relations:manager, supplier_relations:manager, production:manager, logistics:manager}') WHERE `user_id` = 1;

-- Insert Kathy Jensen Person Info
INSERT INTO `Organizations`.`People` (`organization_id`, `first_name`, `last_name`, `job_title`, `phone_number`, `email_address`, `is_employee`, `hourly_wage`, `contract_date`) VALUES 
	(1, "Kathy", "Jensen", "Owner", "8016025244 ", "Info@holisticlifesupplements.com", true, 0, '2016-1-1');

-- Insert Kathy Jensen User Info  (Password = password)
INSERT INTO `Organizations`.`User` (`user_id`, `person_id`, `username`, `encrypted_password`) VALUES (2, 2, "kathyj", "pbkdf2:sha256:260000$D8qPhRKS15pNXdWb$7bd4d1a2603d4365d0711b7342a1a59f67fad6354b8424e574d0654cf276ec5c");
UPDATE `Organizations`.`User` SET `doc` = JSON_SET(`doc`, '$.access_privileges', '{human_resources:manager, client_relations:manager, supplier_relations:manager, production:manager, logistics:manager}') WHERE `user_id` = 2;