from ..auth import odoo 

class UomList ():

    """get uom list"""
    def get_uom(data):
        """get uom list (id) by uom_name"""
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        
        parners_details = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                        'uom.uom', 'search_read',
                [[['name', '=', data["uom_name"]],['name', '=', data["uom_po_name"]]]],
                { 'fields': ['display_name'] ,'limit': 1})
        return parners_details
 