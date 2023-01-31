
-- USE `Organizations`;
CALL ORG_EXISTS("Health");

SET @org_name = "Health";
SELECT
	`organization_id`,
	`organization_name`, 
	GREATEST(
		sys.LEVENSHTEIN_RATIO(`organization_name`, @org_name),
        sys.LEVENSHTEIN_RATIO(`alias_name_1`, @org_name),
        sys.LEVENSHTEIN_RATIO(`alias_name_2`, @org_name),
        sys.LEVENSHTEIN_RATIO(`alias_name_3`, @org_name) ) AS `max_duplicate_percent`
FROM `Organizations`.`Organizations` 
WHERE 
	sys.LEVENSHTEIN_RATIO(`organization_name`, @org_name) > 50 OR
	sys.LEVENSHTEIN_RATIO(`alias_name_1`, @org_name) > 50 OR
	sys.LEVENSHTEIN_RATIO(`alias_name_2`, @org_name) > 50 OR
	sys.LEVENSHTEIN_RATIO(`alias_name_3`, @org_name) > 50 OR
	@org_name LIKE `organization_name`;