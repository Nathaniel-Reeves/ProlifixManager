DELIMITER //
CREATE PROCEDURE `Organizations`.`ORG_EXISTS`(IN s1 VARCHAR(200))
BEGIN
	SELECT
		`organization_id`,
		`organization_name`, 
        GREATEST(
			sys.LEVENSHTEIN_RATIO(`organization_name`, s1),
			sys.LEVENSHTEIN_RATIO(`alias_name_1`, s1),
			sys.LEVENSHTEIN_RATIO(`alias_name_2`, s1),
			sys.LEVENSHTEIN_RATIO(`alias_name_3`, s1)
            ) AS `max_duplicate_percent`
	FROM `Organizations`.`Organizations` 
	WHERE 
		sys.LEVENSHTEIN_RATIO(`organization_name`, s1) > 50 OR
		sys.LEVENSHTEIN_RATIO(`alias_name_1`, s1) > 50 OR
		sys.LEVENSHTEIN_RATIO(`alias_name_2`, s1) > 50 OR
		sys.LEVENSHTEIN_RATIO(`alias_name_3`, s1) > 50 OR
		s1 LIKE `organization_name`;
END//
