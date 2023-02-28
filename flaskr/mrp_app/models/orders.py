import mysqlx

try:
    from mrp_app import app
except ImportError:
    print("Import app failure, Importing from Substitute Class")
    from mrp_app.models.substitute_App_class import App
    app = App()


def fetch_sales_by_org(org_id):
    session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
    result = session.sql(
        """
        SELECT 
            CONCAT(a.`organization_id`, "-", "SO", "-", a.`prefix`, LPAD(a.`year`,2,"0"), "-", LPAD(a.`month`,2,"0"), "-", LPAD(a.`sec_number`,3,"0")) AS SO_number,
            `client_po_num`,
            COUNT(CONCAT(c.`prefix`, LPAD(c.`year`,2,"0"), LPAD(c.`month`,2,"0"), LPAD(c.`sec_number`,3,"0"), c.suffix)) AS production_runs_count
        FROM `Orders`.`Sales_Orders` a
        LEFT JOIN `Orders`.`Sale_Order_Detail` b ON
            a.`prefix` = b.`prefix` AND
            a.`year` = b.`year` AND
            a.`month` = b.`month` AND
            a.`sec_number` = b.`sec_number`
        LEFT JOIN `Orders`.`Lot_Numbers` c ON
            c.`so_detail_id` = b.`so_detail_id`
        WHERE a.`organization_id` = %s
        GROUP BY 
            a.`prefix`,
            a.`year`,
            a.`month`,
            a.`sec_number`
        ORDER BY
            a.`year` DESC,
            a.`month` DESC,
            a.`sec_number` DESC;
        """ % org_id
    ).execute()
    order_data = result.fetch_all()
    session.close()
    columns = result.get_columns()
    d = {}
    for data in order_data:
        res = {}
        for i in range(len(list(data))):
            res[columns[i].get_column_name()] = data[i]
        d[res["SO_number"]] = res
    return d


def fetch_qc(lot_number):
    session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
    schema = session.get_schema("Orders")

    collection = schema.get_collection('Lot_Numbers')
    result = collection.find("'microbiological' IN $**.test_type AND _id == :lot_number") \
        .bind("lot_number", lot_number) \
        .execute()
    # result = collection.find("'microbiological' IN $**.test_type AND _id == :lot_number") \
    #     .fields("$**.tests") \
    #     .bind("lot_number", lot_number) \
    #     .execute()
    data = dict(result.fetch_one())
    print(data)




# "test_type": "microbiological"
