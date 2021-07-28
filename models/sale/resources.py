from ..auth import odoo 

class SaleOrderCreate():
    """Odoo model: sale.order create"""

    def post(data,partner_id,team_id):
        """create order in odoo"""

        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        id = models.execute_kw(odoo_client.db, uid, odoo_client.password, 'sale.order', 'create',             
            [{
            'partner_id': partner_id,
            'team_id' : team_id,
            'client_order_ref' : data['client_order_ref'],
            'partner_invoice_id' : data['partner_invoice_id'],
            'partner_shipping_id' : data['partner_shipping_id'],
            'payment_acquirer_id' : data['payment_acquirer_id'],
            'pricelist_id' : data['pricelist_id'],                              
            }])
        #name = models.execute_kw(odoo_client.db, uid, odoo_client.password, 'sale.order', 'name_get', [[id]])
        
        return id


class SaleOrderList():
    """get list sale order"""

    def get_order_ref_team (venta,team_id):
        """get list order for client_order_ref and team_id """
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        team_details = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                            'sale.order', 'search_read',
            [[['client_order_ref', '=', venta["client_order_ref"]],['team_id', '=', team_id]]],
            { 'fields': ['name'],'limit': 1})
        return team_details 

    def get_id (id):
        """get list order for id """
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        
        team_details = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                            'sale.order', 'search_read',
                            
            [[['id', '=', id]]],
            { 'fields': ['name', 'id','company_id','partner_id'],'limit': 1})
            #['id', '=', id]
            #'fields': ['name', 'id','company_id','partner_id'],
        return team_details
