
USE `Organizations`;
SET @search = "prolifix";

SELECT
	`organization_id`,
	`organization_name`, 
    sys.LEVENSHTEIN_RATIO(`organization_name`, @search),
	sys.LEVENSHTEIN_RATIO(`alias_name_1`, @search),
    `alias_name_1`,
	sys.LEVENSHTEIN_RATIO(`alias_name_2`, @search),
    `alias_name_2`,
	sys.LEVENSHTEIN_RATIO(`alias_name_3`, @search),
    `alias_name_3`,
	GREATEST(
		sys.LEVENSHTEIN_RATIO(`organization_name`, @search),
		sys.LEVENSHTEIN_RATIO(`alias_name_1`, @search),
		sys.LEVENSHTEIN_RATIO(`alias_name_2`, @search),
		sys.LEVENSHTEIN_RATIO(`alias_name_3`, @search)
		) AS `max_duplicate_percent`
FROM `Organizations`.`Organizations` 
WHERE 
	sys.LEVENSHTEIN_RATIO(`organization_name`, @search) > 50 OR
	sys.LEVENSHTEIN_RATIO(`alias_name_1`, @search) > 50 OR
	sys.LEVENSHTEIN_RATIO(`alias_name_2`, @search) > 50 OR
	sys.LEVENSHTEIN_RATIO(`alias_name_3`, @search) > 50;



SELECT 
	`Organizations`.organization_name, 
    `Product_Master`.product_name, 
    `Product_Master`.`type`,
    `Formula_Master`.total_grams_per_unit,
    `Components`.component_name,
    `Formula_Detail`.percent
FROM `Organizations`.`Organizations`
INNER JOIN `Products`.`Product_Master` ON
	`Organizations`.organization_id = `Product_Master`.organization_id
INNER JOIN `Formulas`.`Formula_Master` ON
	`Product_Master`.product_id = `Formula_Master`.product_id
INNER JOIN `Formulas`.`Formula_Detail` ON
	`Formula_Detail`.formula_id = `Formula_Master`.formula_id
INNER JOIN `Inventory`.`Components` ON
	`Formula_Detail`.ingredient_id = `Components`.component_id

WHERE `Product_Master`.product_name = "vitamin C";



	