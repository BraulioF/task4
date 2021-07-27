from ..auth import odoo 

class DteOrderList():
    """get list dte order"""

    def get_dteorder (id):
        """get list dteorder"""
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        order = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                            'adnet.dte.order', 'search_read',
            [[['sale_id', '=', 'SO7265']]],
            {'limit': 4})
        return order 
