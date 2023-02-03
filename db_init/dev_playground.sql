
SELECT 
	`Organizations`.organization_name, 
    `Product_Master`.product_name, 
    `Product_Master`.`type`,
    `Formula_Master`.total_grams_per_unit,
    `Components`.component_name
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



	