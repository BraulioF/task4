from ..auth import odoo


class TeamList():
    """get team odoo"""

    def get_name(data):
        """get team for name"""
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        venta = data["venta"]

        team_id = models.execute_kw(odoo_client.db, uid, odoo_client.password,
            'crm.team', 'search_read',
            [[['name', '=', venta['name']]]],
            { 'fields': ['id'] ,'limit': 1})
            
        return team_id 

     


