from ..auth import odoo 

class SaleOrderLineCreate():
    """Odoo model: sale.order.line create"""

    def post(order_line,order_id):
        """create order line in odoo"""
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        id = models.execute_kw(odoo_client.db, uid, odoo_client.password, 'sale.order.line', 'create',
            [{
                "order_id" : int(order_id),           
                "product_id" : int(order_line["product_id"]),
                "product_uom_qty": order_line["product_uom_qty"],
                "price_unit": order_line["price_unit"],  
            }])
            
        return id

class SaleOrderLineList():
    """get sale.order.line by sale_id"""

    def get_id(sale_id):
        """get order line in odoo"""
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        id = sale_id

        partner = models.execute_kw(odoo_client.db, uid, odoo_client.password,
            'sale.order.line', 'search_read',
            [[['order_id', '=', id]]],
            {'fields': ['id','product_id','product_uom_qty','display_name','other_discounts','partner_liquidator_id','price_reduce','price_reduce_taxexcl','price_reduce_taxinc','price_subtotal','price_tax','price_total','price_unit']}) 

            #,'limit': 2
            #['id', '=', id]
            #'fields': ['name', 'id', 'phone', 'email', 'rut']
        return partner
    
