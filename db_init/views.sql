-- Create Views
USE `Organizations`;
CREATE OR REPLACE VIEW `org_and_people_detail` AS
SELECT 
	`People`.`person_id`,
    `People`.`first_name`,
    `People`.`last_name`,
    `People`.`job_description`,
    `People`.`department`,
    `People`.`phone_number_primary`,
    `People`.`phone_number_secondary`,
    `People`.`email_address_primary`,
    `People`.`email_address_secondary`,
    `People`.`birthday`,
    `People`.`is_employee`,
    `People`.`contract_date`,
    `People`.`termination_date`,
    `People`.`clock_number`,
    `Organizations`.`organization_id`,
    `Organizations`.`organization_name`,
    `Organizations`.`organization_initial`,
    `Organizations`.`alias_name_1`,
    `Organizations`.`alias_name_2`,
    `Organizations`.`alias_name_3`,
    `Organizations`.`date_entered`,
    `Organizations`.`website_url`,
    `Organizations`.`date_vetted`,
    `Organizations`.`risk_level`,
    `Organizations`.`supplier`,
    `Organizations`.`client`,
    `Organizations`.`lab`,
    `Organizations`.`other`,
    `Organizations`.`doc`,
    `Organizations`.`notes`
FROM `Organizations`
LEFT JOIN `People` ON `Organizations`.`organization_id` = `People`.`organization_id`;