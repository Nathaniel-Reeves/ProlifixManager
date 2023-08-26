SELECT
	JSON_OBJECT(
		'organization_id', a.`organization_id`, 
		'date_entered', a.`date_entered`,
		'website_url', a.`website_url`,
		'vetted', a.`vetted`,
		'date_vetted', a.`date_vetted`,
        'risk_level', a.`risk_level`,
        'supplier', a.`supplier`,
        'client', a.`client`,
        'lab', a.`lab`,
        'other', a.`other`,
        'doc', a.`doc`,
        'notes', a.`notes`,
        'organization_name', b.`organization_name`
		)
AS organization_objects
FROM `Organizations`.`Organizations` a
INNER JOIN `Organizations`.`Organization_Names` b ON 
	a.`organization_id` = b.`organization_id`
WHERE b.`primary_name` = true;