""" views models"""
from models.sale.resources import SaleOrderList
from flask import Flask, json, jsonify, request
import requests
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
    logging.info(f'vista -->  /sale')
    data = request.get_json()
    logging.info(f'data recivida {data}')
    dat = data["venta"]
    team = rs_team.TeamList.get_name(dat)
    if(len(team) == 0):
        valor = data['venta']
        valoresp = valor['name']
        logging.error(f'{valoresp} No existe en la Base de Datos')
        return (f'{valoresp} No existe en la Base de Datos')
    else:
        sales = data["venta"] 
        value = team[0]
        team_id = value['id']
        get_team_repeticion = rs_sale.SaleOrderList.get_order_ref_team(sales,team_id)
        if(len(get_team_repeticion) != 0):
            val = get_team_repeticion[0]
            idventa = val['name']
            logging.error(f'{idventa} Esa Venta ya existe en la Base de Datos')
            return jsonify("Esa venta ya existe "+idventa)
        else:       
            cliente = data["cliente"] 
            partner = rs_partner.ResPartnerList.get_rut(cliente)
            if (partner == []):
                logging.info(f'No existe el cliente por lo que se creo uno nuevo')           
                partner_id = rs_partner.ResPartnerCreate.post(cliente)
            else:                
                partner_id = partner[0]['id']
                logging.info(f'existe el cliente {partner_id}')  

            valoressale = data['venta']
            product = rs_product_template.ProductList.get_default_code(valoressale)
            if(len(product)== 0):
                logging.error(f'No existe el producto') 
                return"No existe ese Producto"       
            else:
                order = data["venta"] 
                order_id = rs_sale.SaleOrderCreate.post(order,partner_id,team_id)
                logging.info(f'orden creada {order_id}') 
                order_line = data["producto"]               
                rs_sale_line.SaleOrderLineCreate.post(order_line,order_id)
                logging.info(f'line agregada a la orden') 
            
            return jsonify({"creado":order_line})

##GET PRODUCT
@app.route("/product/get", methods=["GET"])
def get_prod():
    logging.info("Vista --> /product/get")
    data = request.get_json()
    product = data["get_producto"]
    checkprod = rs_product_template.ProductList.get_default_code(product)
    if(len(checkprod) == 0):
        logging.error("Error : no existe un producto con ese defaultcode")
        return jsonify({"Error" : "No existe un producto con ese defaultcode"})
    logging.info(f'producto encontrado {checkprod}')
    return jsonify({"producto encontrado ": checkprod})

## CREATE PRODUCT
@app.route("/product/create", methods=["POST"])
def createproduct():

    logging.info("Vista --> /product/create")
    data = request.get_json()
    logging.info(f'data obtenida --> {data}')
    product = data["create_prod"]
    checkprod = rs_product_template.ProductList.get_default_code(product)
    if(len(checkprod) != 0):
        logging.error(f'Error-> no existe un producto con {checkprod}')
        return jsonify({"Error" : "Ya existe un producto con ese defaultcode"})
    if(len(rs_product_template.ProductList.get_barcode(product)) != 0):
        logging.error(f'Error-> ya existe un producto con ese barcode')
        return jsonify({"Error" : "Ya existe un producto con ese barcode"})
    
    verif = rs_product_categ.ProductCategList.get_name(product)    
    if(len(verif)==0):        
        val = product["categ_name"]
        logging.error(f'no existe esa categoria')
        return "No existe la categoria :"+ val

    check = rs_uom.UomList.get_uom(product)
    if(len(check)==0):
        val = product["uom_name"]
        logging.error(f'no existe esa unidad de medida')
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
    logging.info(f'producto creado con exito {crear}')
    return jsonify({" Producto creado ":crear})

#UPDATE PRODUCT
@app.route("/product/update", methods=["PUT"])
def update_product():
    logging.info("vista --> /product/template")
    data = request.get_json()
    product = data["update_prod"]
    checkprod = rs_product_template.ProductList.get_default_code(product)
    if(len(checkprod) == 0):
        logging.error("Error no existe un producto con ese defaultcode")
        return jsonify({"Error" : "No existe un producto con ese defaultcode"})
    else:
        ###
        #canal = data["get_canal"]
        verif = rs_product_categ.ProductCategList.get_name(product)    
        if(len(verif)==0):        
            val = product["categ_name"]
            logging.e
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
    logging.info("Vista --> /product/drop")
    logging.info(f'data obtenido {data}')
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
    logging.info(" vista : /canal")
    data = request.get_json()
    canal = data["get_canal"]
    checkprod = rs_team.TeamList.get_name(canal)
    if(len(checkprod) == 0):
        return jsonify({"Error" : "No existe ese con ese canal"})
    return jsonify({"canal encontrado ": checkprod})


@app.route("/sermecoop/authorize", methods=["POST"])
def srmc_authorize():
    #SO7209 => 7167
    #SO7166 => 7135

    logging.info(" vista : /sermecoop/authorize")
    data = request.get_json()
    value= data["sale_id"]
    iddd = data["id"]
    result = rs_sale.SaleOrderList.get_id(iddd)
    logging.info(f'se encontro a partir de Sale order list {result}')
    id = result[0]["partner_id"][0]

    partner = rs_partner.ResPartnerList.get_id(id)
    logging.info(f'se encontro a partir de partner {partner}')
    sale = result[0]["name"]

    sale_order_line = rs_sale_line.SaleOrderLineList.get_id(sale)   
    logging.info(f'se encontro a partir de sale order line {sale_order_line}')
    details = []
    #details2 = []
    for i in range(len(sale_order_line)):
        id = sale_order_line[i]["product_id"][0]
        product = rs_product.ProductList.get_id(id)
        logging.info(f'se encontro el product.product -> {product}')
        sku = product[0]["default_code"]
        name = product[0]["name"]
        categ= product[0]["categ_id"][1]
        price = product[0]["price"]
        quantity = sale_order_line[i]["product_uom_qty"]
        details.append({"pclass": categ, "name": name, "sku":sku, "quantity":int(quantity), "price":price, "bonus":10, "deductible":10, "copay" : 10})
        #en la docu sale medicationclass pero hay que pasarle pclass no se cambian los nombres
    productdata =  ({
        "operation_number": result[0]["id"],
        "company": result[0]["company_id"][0],
        "policy": result[0]["id"],
        "transaction_datetime": str(datetime.datetime.now()),
        "store": result[0]["id"],
        "pos": result[0]["id"],
        "store_description": "Caja 3 Local 1 FRACCION",
        "invoice": result[0]["id"],
        "client_rut": partner[0]["rut"],
        "client_sequence": 1003,
        "beneficiary_rut": partner[0]["rut"],
        "doctor_rut": partner[0]["rut"],
        "details" : details
    })
    
    logging.info(productdata)
    url = 'https://fracciondte.brazilsouth.cloudapp.azure.com/auth/token/'
    payload = {"username": "fraccion_erp_test","password": "erp.test"}
    
    response = requests.post(url, json=payload)
    
    #obtenemos el token
    
    if response.status_code == 200:
        val = response.json()
        logging.info(f'El token obtenido es {val["access_token"]}')
        url = 'http://fracciondte.brazilsouth.cloudapp.azure.com/sermecoop/authorize/'

        header = {'Authorization': 'Bearer ' + val["access_token"]}
        #usamos el token

        response2 = requests.post(url, json=productdata, headers=header)

        ##----------------------------
        val2=response2.json()
        logging.info(f'authorize nos retorna {val2}')
        #hacemos la consulta a authorize para obtener el query_id
        venta_data =  ({
        "query_id":val2["query_id"],
        "status":1,
        "doctor_name":"Mauricio Fernandez",
        "operation_number": result[0]["id"],
        "company": result[0]["company_id"][0],
        "policy": result[0]["id"],
        "transaction_datetime": str(datetime.datetime.now()),
        "store": result[0]["id"],
        "pos": result[0]["id"],
        "store_description": "Caja 3 Local 1 FRACCION",
        "invoice": result[0]["id"],
        "client_rut": partner[0]["rut"],
        "client_sequence": 1003,
        "beneficiary_rut": partner[0]["rut"],
        "doctor_rut": partner[0]["rut"],
        "details" : details
    })
        url = 'http://fracciondte.brazilsouth.cloudapp.azure.com/sermecoop/confirmation/'
        #otra vez hacemos la consulta ahora para obtner el bond_id que necesitamos para el nullify
        response3 = requests.post(url,json=venta_data, headers=header)
        bondid = response3.json()["bond_id"]
        logging.info(f'se obtuvo -> {bondid}')

        datafornullify = ({"operation_number": result[0]["id"], "bond_id":bondid})

        url = "http://fracciondte.brazilsouth.cloudapp.azure.com/sermecoop/nullify/"
        response4 = requests.post(url,json=datafornullify, headers=header)
        return (response4.json())
        

##GET DTE
@app.route("/adnet/dte/bo/op", methods=["GET"])
def get_adnet():
    logging.info(" vista : /adnet/dte/bo/op")
    data = request.get_json()
    id = data["sale_id"]
    checkorder = rs_dte_order.DteOrderList.get_dteorder(id)
    logging.info(f' es ---> {checkorder}')
    if(len(checkorder) == 0):
        return jsonify({"Error" : "No existe ese con ese canal"})
    return jsonify({"canal encontrado ": checkorder})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

    