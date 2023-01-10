USE `Organizations`;
CREATE OR REPLACE VIEW `org_and_people_detail` AS
SELECT 
	`People`.`person_id`,
    `People`.`first_name`,
    `People`.`last_name`,
    `People`.`job_title`,
    `People`.`phone_number`,
    `People`.`email_address`,
    `People`.`is_employee`,
    `People`.`hourly_wage`,
    `People`.`contract_date`,
    `People`.`termination_date`,
    `Organizations`.*
FROM `Organizations`
LEFT JOIN `People` ON `Organizations`.`organization_id` = `People`.`organization_id`;