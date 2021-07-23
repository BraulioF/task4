import requests
class tokenSermecoop:
    """get tokken from sernecoop api"""

    def get_token():
        """get tokken"""
        url = 'https://fracciondte.brazilsouth.cloudapp.azure.com/auth/token/'
        payload = {"username": "fraccion_erp_test","password": "erp.test"}
        
        response = requests.post(url, json=payload)

        return response


class sermecoopAuthorize:
    
    
    def get_authorize(data,productdata):

        url = 'http://fracciondte.brazilsouth.cloudapp.azure.com/sermecoop/authorize/'

        header = {'Authorization': 'Bearer ' + data["access_token"]}
        #usamos el token

        response = requests.post(url, json=productdata, headers=header)

        return response


class sermecoopConfirm:
    
    
    def confirmation(data,venta_data):

        url = 'http://fracciondte.brazilsouth.cloudapp.azure.com/sermecoop/confirmation/'

        header = {'Authorization': 'Bearer ' + data["access_token"]}
        #usamos el token

        response = requests.post(url, json=venta_data, headers=header)

        return response


class sermecoopNullify:
    
    
    def nullify(data,venta_data):

        url = 'http://fracciondte.brazilsouth.cloudapp.azure.com/sermecoop/nullify/'

        header = {'Authorization': 'Bearer ' + data["access_token"]}
        #usamos el token

        response = requests.post(url, json=venta_data, headers=header)

        return response