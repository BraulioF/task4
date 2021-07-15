from ..auth import odoo


class ProductList():
    """get list product"""

    def get(product):
        """get product for default_code"""
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        
        default_code = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                        'product.template', 'search_read',
            [[['default_code', '=', product["default_code"]]]],
            { 'fields': ['default_code','id'] ,'limit': 1})
        return default_code
    
    def get_barcode(product):
        """get product for default_code"""
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        
        default_code = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                        'product.template', 'search_read',
            [[['barcode', '=', product["barcode"]]]],
            { 'fields': ['barcode'] ,'limit': 1})
        return default_code

class ProductDelete():
    """delete product by id"""

    def delete(id):
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        models.execute_kw(odoo_client.db, uid, odoo_client.password, 'product.template', 'unlink', [[int(id)]])
        
        check = models.execute_kw(odoo_client.db, uid, odoo_client.password,
            'product.product', 'search', [[['id', '=', id]]])
        return check
 