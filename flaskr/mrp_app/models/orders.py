import mysqlx

try:
    from mrp_app import app
except ImportError:
    print("Import app failure, Importing from Substitute Class")
    from mrp_app.models.substitute_App_class import App
    app = App()


def fetch_orders_by_org(org_id):
    session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
    result = session.sql(
        """
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
        WHERE d.`organization_id` = %s
        GROUP BY b.`po_detail_id`, d.`product_id`
        ORDER BY b.`po_detail_id` DESC;
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
        d[res["PO_number"]] = res
    return d
