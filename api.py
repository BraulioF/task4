""" views models"""
from flask import Flask, jsonify, request
from models import *
from models import odoo

""" import librery"""
import datetime
import time
import config as cg
import logging


#Global varial
#HOST = cg.server['host']
logging.basicConfig(filename='odoo.log', level = logging.DEBUG, 
    format='%(asctime)s:%(levelname)s:%(message)s')

#Declare app
app = Flask(__name__)

#POST A VENTAS
@app.route("/sale", methods=["POST"])
def sale_create():
    #Usar el metodo ya creado donde creamos un partner
    data = request.get_json()

    team = rs_team.TeamList.get_name(data)
    if(len(team) == 0):
        valor = data['venta']
        valoresp = valor['name']
        return "'" + valoresp +"'" + " No existe en la Base de Datos"
    else:
        value = team[0]
        team_id = value['id']
        get_team_repeticion = rs_sale.SaleOrderList.get_order_ref_team(data,team_id)
        if(len(get_team_repeticion) != 0):
            val = get_team_repeticion[0]
            idventa = val['name']
            return jsonify("Esa venta ya existe "+idventa)
        else:       
            cliente = data["cliente"] 
            partner = rs_partner.ResPartnerList.get_rut(cliente)
            if (partner == []):           
                partner_id = rs_partner.ResPartnerCreate.post(cliente)
                print("se creo con ", partner_id)
            else:
                partner_id = partner
            
            product = rs_product.ProductList.get_default_code(data)
            if(len(product)== 0):
                return"No existe ese Producto"       
            else:
                order = data["venta"] 
                order_id = rs_sale.SaleOrderCreate.post(order,partner_id,team_id)
                order_line = data["producto"]
                rs_sale_line.SaleOrderLineCreate.post(order_line,order_id)
            
            return jsonify({"creado":order_line})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)