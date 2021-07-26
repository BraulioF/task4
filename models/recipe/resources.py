from ..auth import odoo

class RecipeList():
    """get recipe list"""

    def get_id(id):
        """get product by id"""
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        recipe = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                        'fraccion.recipe', 'search_read',
            [[['id', '=',id]]],
            { 'fields': ['nombre_medico','img','id','active','create_date','prolongaldo','recipe_line_id','assigned','fecha_receta','posologia'] ,'limit': 1})
        return recipe


class RecipeCreate():
    """Create a new recipe"""

    def post(idcliente):
        """post a new recipe"""

        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        partnerid = models.execute_kw(odoo_client.db, uid, odoo_client.password, 'fraccion.recipe', 'create', 
            [{ 
            'nombre_cliente': idcliente           
            }])
        #name = models.execute_kw(odoo_client.db, uid, odoo_client.password, 'res.partner', 'name_get', [[partnerid]])
        return partnerid