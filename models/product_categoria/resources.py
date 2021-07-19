from ..auth import odoo 


class ProductCategList ():
    """get list of product categ"""
    
    def get_name(data):
        """Get categ_name by categ name se le asgina el nombre segun lo que filtramos"""
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        parners_details = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                        'product.category', 'search_read',
                [[['name', '=', data["categ_name"]]]],
                { 'fields': ['id'] ,'limit': 1})
        return parners_details 