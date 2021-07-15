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
 
        if partner == []:
            return partner
        ids = partner[0]["id"]
        return ids


class ResPartnerCreate():
    """Odoo model: PostClient creat customer """

    def post(data):
        authentic = odoo.OdooClient()
        user = authentic.logging()
        uid = user[0]
        models = user[1]

        hash_partner = data["partner"]
        rut = hash_partner["rut"]
        name = hash_partner["name"]
        phone = hash_partner["phone"]
        email = hash_partner["email"]
        
        ids = models.execute_kw(authentic.db, uid, authentic, 'res.partner', 'create', [{
            'name': name,'phone': phone,'email': email, 'rut': rut}])

        return ids
       

class ResPartnerUpdate():
    """Odoo model: Creat a customer reference ID """

    def put(data, id):
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        #12148 frank
        #12165  don cangrejo
        #12170  ??????

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
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        models.execute_kw(odoo_client.db, uid, odoo_client.password, 'res.partner', 'unlink', [[int(id)]])
        # check if the deleted record is still in the database
        check = models.execute_kw(odoo_client.db, uid, odoo_client.password,
            'res.partner', 'search', [[['id', '=', id]]])
        return check