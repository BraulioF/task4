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

#GET PARTNER
@app.route("/partner/get", methods=["GET"])
def get():
    logging.info(f'Vista = /partner/get')
    data = request.get_json()
    logging.info(f'Se obtuvo {data}')
    cliente = data["cliente"]
    partners = rs_partner.ResPartnerList.get_rut(cliente)
    if(len(partners)== 0):
        logging.error(f'el siguiente rut no existe {cliente["rut"]}')
        return jsonify({"Error 404": "Ese RUT no existe"})
    else:
        logging.info(f'Se retorno {partners}')
        return jsonify({"Encontrado": partners})

#CREATE PARTNER
@app.route("/partner/create", methods=["POST"])
def create():
    logging.info(f'Vista = /partner/create')
    data = request.get_json()
    logging.info(f'Se obtuvo {data}')
    cliente = data["cliente"]
    partners = rs_partner.ResPartnerList.get_rut(cliente)
    if(len(partners)!= 0):
        logging.error(f'el siguiente rut ya existe {cliente["rut"]}')
        return jsonify({"Error": "Ese RUT ya existe"})
    else:  
        crear = rs_partner.ResPartnerCreate.post(cliente)
        logging.info(f'Se retorno {crear}')
        return jsonify({"Creado": crear})

#UPDATE PARTNER
@app.route("/partner/update", methods=["PUT"])
def update_partner():
    logging.info(f'Vista = /partner/update')
    data = request.get_json()
    logging.info(f'Se obtuvo {data}')
    cliente = data["cliente"]
    partners = rs_partner.ResPartnerList.get_rut(cliente)
    if(len(partners)== 0):
        logging.error(f'el siguiente rut no existe {cliente["rut"]}')
        return jsonify({"Error 404": "Ese RUT no existe"})
    else:
        id = partners[0]['id']
        rs_partner.ResPartnerUpdate.put(cliente,id)
        logging.info(f'Se modifico el partner con id {id}')
        return jsonify({partners:"Modificado"})

#Delete PARTNER
@app.route("/partner/drop", methods=["DELETE"])
def drop_partner():
    logging.info(f'Vista = /partner/drop')
    data = request.get_json()
    logging.info(f'Se obtuvo {data}')
    cliente = data["cliente"]
    partners = rs_partner.ResPartnerList.get_rut(cliente)
    if(len(partners)== 0):
        logging.error(f'el siguiente rut no existe {cliente["rut"]}')
        return jsonify({"Error 404": "Ese RUT no existe"})
        
    else:
        id = partners[0]['id']
        rs_partner.ResPartnerDelete.delete(id)
        logging.info(f'Se elimino el partner con id {id}')
        return jsonify({cliente["rut"]:"Eliminado con exito"})


#POST A VENTAS
@app.route("/sale", methods=["POST"])
def sale_create():
    data = request.get_json()
    dat = data["venta"]
    team = rs_team.TeamList.get_name(dat)
    if(len(team) == 0):
        valor = data['venta']
        valoresp = valor['name']
        return (f'{valoresp} No existe en la Base de Datos')
    else:
        sales = data["venta"] 
        value = team[0]
        team_id = value['id']
        get_team_repeticion = rs_sale.SaleOrderList.get_order_ref_team(sales,team_id)
        if(len(get_team_repeticion) != 0):
            val = get_team_repeticion[0]
            idventa = val['name']
            return jsonify("Esa venta ya existe "+idventa)
        else:       
            cliente = data["cliente"] 
            partner = rs_partner.ResPartnerList.get_rut(cliente)
            if (partner == []):           
                partner_id = rs_partner.ResPartnerCreate.post(cliente)
            else:                
                partner_id = partner[0]['id']

            valoressale = data['venta']
            product = rs_product_template.ProductList.get_default_code(valoressale)
            if(len(product)== 0):
                return"No existe ese Producto"       
            else:
                order = data["venta"] 
                order_id = rs_sale.SaleOrderCreate.post(order,partner_id,team_id)
                order_line = data["producto"]               
                rs_sale_line.SaleOrderLineCreate.post(order_line,order_id)
            
            return jsonify({"creado":order_line})

##GET PRODUCT
@app.route("/product/get", methods=["GET"])
def get_prod():
   
    data = request.get_json()
    product = data["get_producto"]
    checkprod = rs_product_template.ProductList.get_default_code(product)
    if(len(checkprod) == 0):
        return jsonify({"Error" : "No existe un producto con ese defaultcode"})
    return jsonify({"producto encontrado ": checkprod})

## CREATE PRODUCT
@app.route("/product/create", methods=["POST"])
def createproduct():

    data = request.get_json()
    product = data["create_prod"]
    checkprod = rs_product_template.ProductList.get_default_code(product)
    if(len(checkprod) != 0):
        return jsonify({"Error" : "Ya existe un producto con ese defaultcode"})
    if(len(rs_product_template.ProductList.get_barcode(product)) != 0):
        return jsonify({"Error" : "Ya existe un producto con ese barcode"})
    
    verif = rs_product_categ.ProductCategList.get_name(product)    
    if(len(verif)==0):        
        val = product["categ_name"]
        return "No existe la categoria :"+ val

    check = rs_uom.UomList.get_uom(product)
    if(len(check)==0):
        val = product["uom_name"]
        return "No existe la unidad de medida :"+ val
    check_po = rs_uom.UomList.get_uom(product)
    verif = verif[0]
    check = check[0]
    check_po = check_po[0]
    id_name_categ = verif['id']
    id_display_uom = check['id']
    id_display_uom_po = check_po['id']
    logging.info(id_name_categ)
    logging.info(id_display_uom)
    logging.info(id_display_uom_po)
    crear = rs_product_template.ProductCreate.post(product,id_name_categ,id_display_uom,id_display_uom_po)
    
    return jsonify({" Producto creado ":crear})

#UPDATE PRODUCT
@app.route("/product/update", methods=["PUT"])
def update_product():
    data = request.get_json()
    product = data["update_prod"]
    checkprod = rs_product_template.ProductList.get_default_code(product)
    if(len(checkprod) == 0):
        return jsonify({"Error" : "No existe un producto con ese defaultcode"})
    else:
        ###
        #canal = data["get_canal"]
        verif = rs_product_categ.ProductCategList.get_name(product)    
        if(len(verif)==0):        
            val = product["categ_name"]
            return "No existe la categoria :"+ val
        check = rs_uom.UomList.get_uom(product)
        if(len(check)==0):
            val = product["uom_name"]
            return "No existe la unidad de medida :"+ val
        check_po = rs_uom.UomList.get_uom(product)
        verif = verif[0]
        check = check[0]
        check_po = check_po[0]
        id_name_categ = verif['id']
        id_display_uom = check['id']
        id_display_uom_po = check_po['id']
        logging.info(id_name_categ)
        logging.info(id_display_uom)
        logging.info(id_display_uom_po)
        ###
        id = checkprod[0]["id"]
        logging.info(id)
        rs_product_template.ProductUpdate.put(product,id,id_name_categ,id_display_uom,id_display_uom_po)
        return jsonify({"Actualizado":""})

##delete PRODUCT
@app.route("/product/drop", methods=["DELETE"])
def drop_prod():

    data = request.get_json()
    prod = data["delete_producto"]
    check = rs_product_template.ProductList.get_default_code(prod)
    if(len(check)== 0):
        logging.error(f'ese prod no existe {prod["default_code"]}')
        return jsonify({"Error 404": "Ese Producto no existe"})
        
    else:
        id = check[0]["id"]        
        logging.info(id)
        verificar =rs_product_template.ProductDelete.delete(id)
        return jsonify({"Exito":" Eliminado con exito" })


##GET CATEGORIA
@app.route("/canal", methods=["GET"])
def get_channel():
   
    data = request.get_json()
    canal = data["get_canal"]
    checkprod = rs_team.TeamList.get_name(canal)
    if(len(checkprod) == 0):
        return jsonify({"Error" : "No existe ese con ese canal"})
    return jsonify({"canal encontrado ": checkprod})


@app.route("/sermecoop/authorize", methods=["GET"])
def srmc_authorize():
    return "xD"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)