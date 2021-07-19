""" Module of res.partner odoo model """
from ..auth import odoo


class ResPartnerList():
    """Odoo model: res.partner list for customer and company"""

    def get_rut(data):
        """get one parnter for rut"""

        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        rut = data["rut"]

        partner = models.execute_kw(odoo_client.db, uid, odoo_client.password,
            'res.partner', 'search_read',
            [[['rut', '=', rut]]],
            {'fields': ['name', 'id', 'phone', 'email', 'rut']})
 
        return partner
    
    def get_id(data):
        """get one partner by id"""
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        id = data

        partner = models.execute_kw(odoo_client.db, uid, odoo_client.password,
            'res.partner', 'search_read',
            [[['id', '=', id]]],
            {'fields': ['rut'],'limit': 2}) 
            #['id', '=', id]
            #'fields': ['name', 'id', 'phone', 'email', 'rut']
        return partner


class ResPartnerCreate():
    """Odoo model: PostClient creat customer """

    def post(data):
        """post partner"""

        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        partnerid = models.execute_kw(odoo_client.db, uid, odoo_client.password, 'res.partner', 'create', 
            [{ 
            'name': data["name"],
            'rut' : data["rut"],
            'comment' : data["comment"],
            'phone' : data["phone"],
            'email' : data["email"]
            }])
        #name = models.execute_kw(odoo_client.db, uid, odoo_client.password, 'res.partner', 'name_get', [[partnerid]])
        return partnerid
       

class ResPartnerUpdate():
    """Odoo model: Creat a customer reference ID """

    def put(data, id):
        """method update partner"""

        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()

        models.execute_kw(odoo_client.db, uid, odoo_client.password, 'res.partner', 'write', [[int(id)], 
        {
             'name': data['name'],
             'rut' : data['rut'],
             'comment' : data['comment'],
             'phone' : data['phone'],
             'email': data['email']
        }])


class ResPartnerDelete():
    """Odoo model: delete a customer reference ID """

    def delete(id):
        """delte partner by id"""
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        models.execute_kw(odoo_client.db, uid, odoo_client.password, 'res.partner', 'unlink', [[int(id)]])
        # check if the deleted record is still in the database
        check = models.execute_kw(odoo_client.db, uid, odoo_client.password,
            'res.partner', 'search', [[['id', '=', id]]])
        return check