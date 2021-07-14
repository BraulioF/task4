""" Module of res.partner odoo model """
from ..auth import odoo


class ResPartnerList():
    """Odoo model: res.partner list for customer and company"""
    
    def get():
        """get all list partner for company and customer"""
        authentic = OdooClient()
        user = authentic.log()
        uid = user[0]
        models = user[1]
        
        s_read = models.execute_kw(db, uid, password,
            'res.partner', 'search_read',
            [[['is_company', '=', True], ['customer', '=', True]]],
            {'fields': ['name', 'country_id', 'comment']})
        
        return s_read


    def get_id(id):
        """get one parnter for id"""
        authentic = OdooClient()
        user = authentic.log()
        uid = user[0]
        models = user[1]
    
        partner = models.execute_kw(db, uid, password,
            'res.partner', 'search_read',
            [[['id', '=', id]]],
            {'fields': ['name', 'id', 'phone', 'email','rut']})

        return partner


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
        authentic = OdooClient()
        user = authentic.log()
        uid = user[0]
        models = user[1]

        hash_partner = data["partner"]
        rut = hash_partner["rut"]
        name = hash_partner["name"]
        phone = hash_partner["phone"]
        email = hash_partner["email"]
        
        ids = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
            'name': name,'phone': phone,'email': email, 'rut': rut}])

        return ids
       

class ResPartnerUpdate():
    """Odoo model: Creat a customer reference ID """

    def put(data, id):
        authentic = OdooClient()
        user = authentic.log()
        uid = user[0]
        models = user[1]
        print(id)
        id = int(id)

        name = data["name"]
        
        models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {"name": name }])
        # get record name after having changed it
        models.execute_kw(db, uid, password, 'res.partner', 'name_get', [[id]])

        s_read = models.execute_kw(db, uid, password,
            'res.partner', 'search_read',
            [[['id', '=', id]]],
            {'fields': ['name', 'id']})
        print("lectura ", s_read, "\n")

        return s_read


class ResPartnerDelete():
    """Odoo model: delete a customer reference ID """

    def delete(id):
        authentic = OdooClient()
        user = authentic.log()
        uid = user[0]
        models = user[1]
        id = int(id)
        print("cual id eliminare: ", id)
        delet = models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[id]])
        # check if the deleted record is still in the database
        models.execute_kw(db, uid, password,
        'res.partner', 'search', [[['id', '=', id]]])

        return delet