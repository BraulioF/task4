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


    
