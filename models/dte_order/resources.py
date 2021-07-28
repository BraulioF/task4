from ..auth import odoo 

class DteOrderList():
    """get list dte order"""

    def get_dteorder (id):
        """get list dteorder"""
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        order = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                            'adnet.dte.order', 'search_read',
            [[['id', '=', id]]],
            {'limit': 5})
        return order 

class DteOrderCreate():
    """create dte order"""

    def post():
        """create a new dte order"""
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        id = models.execute_kw(odoo_client.db, uid, odoo_client.password, 'adnet.dte.order', 'create',             
            [{
                
                #"account_move_id": false,
                "amount_tax": 2.0,
                "amount_total": 2000.0,
                "amount_total_cardinal": 2000,
                "amount_untaxed": 3.0,
                #"company_id": 9,
                #"company_vat": false,
                #"confirmation_date": false,
                #"confirmation_date_sale": false,
                #"date_cancel": false,
                #"date_issued": false,
                "discount_global": 9.0,
                "dte_type": "(39) Boleta Electronica",
                "folio": "3130",
                #"folio_suggested": false,
                #"invoice_payment_term_id": false,
                #"is_fiscal": false,
                #"origin": false,
                #"partner_business_name": false,
                "partner_id": 10,
                #"payment_acquirer_name": false,
                #"state": "draft",
                #"url_document": false,
                #"user_id": false    
                
            # 'dte_type': '(39) Boleta Electronica',
            # 'folio' : 3131,
            # #'date_issued' : data['client_order_ref'],
            # 'partner_id' :10,
            # 'amount_total' :2991,                     
            }])
        #name = models.execute_kw(odoo_client.db, uid, odoo_client.password, 'sale.order', 'name_get', [[id]])
        
        return id


class DteOrderDelete():
    """delete order by id"""

    def delete(id):
        """delete order by id and check it"""

        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        models.execute_kw(odoo_client.db, uid, odoo_client.password, 'adnet.dte.order', 'unlink', [[int(id)]])
        
        check = models.execute_kw(odoo_client.db, uid, odoo_client.password,
            'adnet.dte.order', 'search', [[['id', '=', id]]])
        return check

class DteOrderUpdate():
    """update dte by id"""

    def put(data,id,id_name_categ,id_display_uom,id_display_uom_po):
        """put dte by id"""

        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()

        models.execute_kw(odoo_client.db, uid, odoo_client.password, 'adnet.dte.order', 'write', [[int(id)], 
        {            
           "amount_tax": 2.0,
                "amount_total": 2000.0,
                "amount_total_cardinal": 2000,
                "amount_untaxed": 3.0,
                "discount_global": 9.0,
                "dte_type": "(39) Boleta Electronica",
                "folio": "3130",
                "partner_id": 10,
        }])