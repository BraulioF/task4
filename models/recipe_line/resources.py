from ..auth import odoo

class RecipeLinesList():
    """get list recipe_lines"""

    def get_lines_id(data):
        """get product recipe_lines"""
        
        odoo_client = odoo.OdooClient()
        uid, models = odoo_client.logging()
        recipe_lines = models.execute_kw(odoo_client.db, uid, odoo_client.password,
                        'fraccion.recipe.line', 'search_read',
            [[['id', '=',data]]],
            { 'fields': ['default_code','product_id','demand','reservation'] ,'limit': 1})
        return recipe_lines