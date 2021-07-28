from ..auth import odoo 

class DteOrderLineList():
    """get list dte order line """

    def get_dteorder (id):
        """get list dteorder line """
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        order = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                            'adnet.dte.order.line', 'search_read',
            [[['id', '=', id]]],
            {'limit': 5})
        return order 

class DteOrderLineCreate():
    """create dte order line"""

    def post():
        """create a new dte order line"""
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        id = models.execute_kw(odoo_client.db, uid, odoo_client.password, 'adnet.dte.order.line', 'create',             
            [{
               "discount" : 200,
               "dte_id" : 7,
               "price_subtotal" : 500.0,
               "price_unit" : 100.0,
               "product_id" : 1,
               "qty": 2,
               "qty_delivered_method" : 2,
               "tax_id" : 2,
               "uom_id" : 1,
            }])
        #name = models.execute_kw(odoo_client.db, uid, odoo_client.password, 'sale.order', 'name_get', [[id]])
        
        return id


class DteOrderLineDelete():
    """delete order line by id"""

    def delete(id):
        """delete order line by id and check it"""

        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        models.execute_kw(odoo_client.db, uid, odoo_client.password, 'adnet.dte.order.line', 'unlink', [[int(id)]])
        
        check = models.execute_kw(odoo_client.db, uid, odoo_client.password,
            'adnet.dte.order', 'search', [[['id', '=', id]]])
        return check

class DteOrderUpdate():
    """update dte.line by id"""

    def put(data,id,id_name_categ,id_display_uom,id_display_uom_po):
        """put dte.line by id"""

        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()

        models.execute_kw(odoo_client.db, uid, odoo_client.password, 'adnet.dte.order.line', 'write', [[int(id)], 
        {            
            "discount" : 200,
            "dte_id" : 7,
            "price_subtotal" : 500.0,
            "price_unit" : 100.0,
            "product_id" : 1,
            "qty": 2,
            "qty_delivered_method" : 2,
            "tax_id" : 2,
            "uom_id" : 1,
        }])