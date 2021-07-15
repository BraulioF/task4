""" views models"""
from flask import Flask, json, jsonify, request
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

#CREATE PARTNER
@app.route("/partner", methods=["GET"])

def get():
   
    data = request.get_json()
    cliente = data["cliente"]
    partners = rs_partner.ResPartnerList.get_rut(cliente)
    if(len(partners)== 0):
        logging.error(f'el siguiente rut no existe {cliente["rut"]}')
        return jsonify({"Error 404": "Ese RUT no existe"})
    else:
        return jsonify({"Encontrado": partners})

#CREATE PARTNER
@app.route("/partner/create", methods=["POST"])

def create():
   
    data = request.get_json()
    cliente = data["cliente"]    
    crear = rs_partner.ResPartnerCreate.post(cliente)
    #y lo mando a su resource
    return jsonify({"Creado": crear})

#UPDATE PARTNER
@app.route("/partner/update", methods=["PUT"])
def update_partner():
    data = request.get_json()
    cliente = data["cliente"]
    partners = rs_partner.ResPartnerList.get_rut(cliente)
    if(len(partners)== 0):
        logging.error(f'el siguiente rut no existe {cliente["rut"]}')
        return jsonify({"Error 404": "Ese RUT no existe"})
    else:
        id = partners[0]['id']
        logging.info(id)
        rs_partner.ResPartnerUpdate.put(cliente,id)
        return jsonify(partners)

#Delete PARTNER
@app.route("/partner/drop", methods=["DELETE"])

def drop_partner():

    data = request.get_json()
    cliente = data["cliente"]
    partners = rs_partner.ResPartnerList.get_rut(cliente)
    if(len(partners)== 0):
        logging.error(f'el siguiente rut no existe {cliente["rut"]}')
        return jsonify({"Error 404": "Ese RUT no existe"})
        
    else:
        id = partners[0]['id']
        logging.info(id)
        verificar =rs_partner.ResPartnerDelete.delete(id)
        return jsonify({cliente["name"]:"Eliminado con exito"})


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

## CREATE PARTNER
@app.route("/product/create", methods=["POST"])

def createproduct():

    data = request.get_json()
    product = data["create_prod"]
    checkprod = rs_product.ProductList.get(product)
    if(len(checkprod) != 0):
        return jsonify({"Error" : "Ya existe un producto con ese defaultcode"})
    if(len(rs_product.ProductList.get_barcode(product)) != 0):
        return jsonify({"Error" : "Ya existe un producto con ese barcode"})
    verif = rs_product_categ.ProductCategList.getCateg(data)    
    if(len(verif)==0):        
        val = product["categ_name"]
        return "No existe la categoria :"+ val
    check = rs_uom.UomList.get(data)
    if(len(check)==0):
        val = product["uom_name"]
        return "No existe la unidad de medida :"+ val
    check_po = rs_uom.UomList.get(data)
    verif = verif[0]
    check = check[0]
    check_po = check_po[0]
    id_name_categ = verif['id']
    id_display_uom = check['id']
    id_display_uom_po = check_po['id']
    logging.info(id_name_categ)
    logging.info(id_display_uom)
    logging.info(id_display_uom_po)
    crear = rs_product.ProductCreate.post(product,id_name_categ,id_display_uom,id_display_uom_po)
    
    return jsonify({" Producto creado ":crear})

##delete producto
@app.route("/product/drop", methods=["DELETE"])

def drop_prod():

    data = request.get_json()
    prod = data["delete_producto"]
    check = rs_product.ProductList.get(prod)
    if(len(check)== 0):
        logging.error(f'ese prod no existe {prod["default_code"]}')
        return jsonify({"Error 404": "Ese Producto no existe"})
        
    else:
        id = check[0]["id"]        
        logging.info(id)
        verificar =rs_product.ProductDelete.delete(id)
        return jsonify({len(verificar):" Eliminado con exito" })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)