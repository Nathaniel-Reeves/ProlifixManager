

USE `Organizations`;
SET @search = "health";

SELECT
	`organization_id`,
	`organization_name`, 
    sys.LEVENSHTEIN_RATIO(`organization_name`, @search)
FROM `Organizations`.`Organization_Names` 
WHERE 
	sys.LEVENSHTEIN_RATIO(`organization_name`, @search) > 50;



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

SELECT * FROM `Organizations`.`Organizations`;

SELECT 
	CONCAT("PO#", a.`prefix`, LPAD(a.`year`,2,"0"), "~", LPAD(a.`month`,2,"0"), "~", LPAD(a.`sec_number`,3,"0")) AS PO_number,
    a.client_po_num,
    CONCAT(c.`prefix`, " ", LPAD(c.`year`,2,"0"), LPAD(c.`month`,2,"0"), LPAD(c.`sec_number`,3,"0"), " ", c.suffix) AS LOT_number,
    d.product_name,
    d.`type`,
    b.unit_order_qty,
    b.kilos_order_qty,
    c.target_unit_yield
FROM `Orders`.`Purchase_Orders` a
INNER JOIN `Orders`.`Purchase_Orders_Detail` b ON
	a.`prefix` = b.`prefix` AND
    a.`year` = b.`year` AND
    a.`month` = b.`month` AND
    a.`sec_number` = b.`sec_number`
INNER JOIN `Orders`.`Lot_Numbers` c ON
	c.`po_detail_id` = b.`po_detail_id`
INNER JOIN `Products`.`Product_Master` d ON
	c.`product_id` = d.`product_id`
INNER JOIN `Organizations`.`Organizations` e ON
	d.`organization_id` = e.`organization_id`
WHERE e.`organization_id` = 39
ORDER BY b.`po_detail_id` DESC;

SELECT 
	CONCAT("PO#", a.`prefix`, LPAD(a.`year`,2,"0"), "~", LPAD(a.`month`,2,"0"), "~", LPAD(a.`sec_number`,3,"0")) AS PO_number,
    a.`client_po_num`,
    COUNT(CONCAT(c.`prefix`, LPAD(c.`year`,2,"0"), LPAD(c.`month`,2,"0"), LPAD(c.`sec_number`,3,"0"), c.suffix)) AS production_runs_count,
    d.`product_name`,
    d.`type`,
    b.`unit_order_qty`,
    b.`kilos_order_qty`
FROM `Orders`.`Purchase_Orders` a
INNER JOIN `Orders`.`Purchase_Orders_Detail` b ON
	a.`prefix` = b.`prefix` AND
    a.`year` = b.`year` AND
    a.`month` = b.`month` AND
    a.`sec_number` = b.`sec_number`
INNER JOIN `Orders`.`Lot_Numbers` c ON
	c.`po_detail_id` = b.`po_detail_id`
INNER JOIN `Products`.`Product_Master` d ON
	c.`product_id` = d.`product_id`
INNER JOIN `Organizations`.`Organizations` e ON
	d.`organization_id` = e.`organization_id`
WHERE d.`organization_id` = 39
GROUP BY b.`po_detail_id`, d.`product_id`
ORDER BY b.`po_detail_id` DESC;

SELECT * FROM `Products`.`Product_Master` ORDER BY product_id;

SELECT 
	CONCAT(c.`prefix`, LPAD(c.`year`,2,"0"), LPAD(c.`month`,2,"0"), LPAD(c.`sec_number`,3,"0"), c.suffix) AS lot_number,
	CONCAT("PO#", a.`prefix`, LPAD(a.`year`,2,"0"), "~", LPAD(a.`month`,2,"0"), "~", LPAD(a.`sec_number`,3,"0")) AS PO_number,
    d.`product_name`,
	d.`type`,
    f.`organization_name`,
    a.`client_po_num`,
    b.`unit_order_qty`
FROM `Orders`.`Purchase_Orders` a
INNER JOIN `Orders`.`Purchase_Orders_Detail` b ON
	a.`prefix` = b.`prefix` AND
    a.`year` = b.`year` AND
    a.`month` = b.`month` AND
    a.`sec_number` = b.`sec_number`
INNER JOIN `Orders`.`Lot_Numbers` c ON
	c.`po_detail_id` = b.`po_detail_id`
INNER JOIN `Products`.`Product_Master` d ON
	c.`product_id` = d.`product_id`
INNER JOIN `Organizations`.`Organizations` e ON
	d.`organization_id` = e.`organization_id`
INNER JOIN `Organizations`.`Organization_Names` f ON
	e.`organization_id` = f.`organization_id` AND
    f.`primary_name` = 1
ORDER BY c.`year`, c.`month`, c.`sec_number`, c.`prefix` DESC;


SELECT * FROM `Orders`.`Purchase_Orders_Detail`;


	