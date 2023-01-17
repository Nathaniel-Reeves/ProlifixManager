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
    `Organizations`.`organization_id`,
    `Organizations`.`organization_name`,
    `Organizations`.`organization_initial`,
    `Organizations`.`date_entered`,
    `Organizations`.`website`,
    `Organizations`.`date_vetted`,
    `Organizations`.`risk_level`,
    `Organizations`.`hq_street_address`,
    `Organizations`.`hq_unit_apt`,
    `Organizations`.`hq_city`,
    `Organizations`.`hq_country`,
    `Organizations`.`hq_zip_code`,
    `Organizations`.`ship_time`,
    `Organizations`.`ship_time_unit`,
    `Organizations`.`ship_time_in_days`,
    `Organizations`.`prolifix`,
    `Organizations`.`supplier`,
    `Organizations`.`client`,
    `Organizations`.`doc`,
    `Organizations`.`notes`
FROM `Organizations`
LEFT JOIN `People` ON `Organizations`.`organization_id` = `People`.`organization_id`;

SELECT * FROM `Organizations`.`org_and_people_detail`;