from ..auth import odoo 


class UomList ():

    """get uom list"""
    def get(data):
        """get uom list (id) by uom_name"""
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        product = data["create_prod"]
        parners_details = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                        'uom.uom', 'search_read',
                [[['name', '=', product["uom_name"]],['name', '=', product["uom_po_name"]]]],
                { 'fields': ['display_name'] ,'limit': 1})
        return parners_details
 