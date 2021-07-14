from ..auth import odoo


class ProductList():
    """get list product"""

    def get_default_code(data):
        """get product for default_code"""
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        product = data["producto"]
        default_code = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                        'product.template', 'search_read',
            [[['default_code', '=', product["default_code"]]]],
            { 'fields': ['default_code'] ,'limit': 1})
        return default_code


class ProductCreate():
    """product create in odoo"""

    def post(data,id_name_categ,id_display_uom,id_display_uom_po):
        """ create parnter """
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()

        product_id = models.execute_kw(odoo_client.db, uid, odoo_client.password, 'product.product', 'create', 
            [{ 
            "default_code": data["default_code"],
            "type":data["type"],
            "name":data["name"],
            "barcode":data["barcode"],
            "categ_id":id_name_categ,
            "list_price":data["list_price"],
            "standard_price":data["standard_price"],
            "uom_id":id_display_uom,
            "uom_po_id":id_display_uom_po,
            "sale_ok":data["sale_ok"],
            "purchase_ok":data["purchase_ok"]
            }])
       
        return product_id

 