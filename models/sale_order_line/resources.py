from ..auth import odoo 

class SaleOrderLineCreate():
    """Odoo model: sale.order.line create"""

    def post(data,order_id):
        """create order line in odoo"""
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        id = models.execute_kw(odoo_client.db, uid, odoo_client.password, 'sale.order.line', 'create', 
            [{
                "order_id" : int(order_id),           
                "product_id" : int(data["product_id"]),
                "product_uom_qty": data["product_uom_qty"],
                "price_unit": data["price_unit"],  
            }])
            
        return id


    
