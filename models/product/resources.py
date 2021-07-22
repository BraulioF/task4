from ..auth import odoo

class ProductList():
    """get list product"""

    def get_id(product):
        """get product by id"""
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        default_code = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                        'product.product', 'search_read',
            [[['id', '=', product]]],
            { 'fields': ['default_code','name','categ_id','price'] ,'limit': 1})
        return default_code
