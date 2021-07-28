"""odoo integration module"""

import xmlrpc.client



url = 'http://adnetworks.cl:1469'
db = 'adnetdev'
username = 'bfernandez@adnetworks.cl'
password = 'spO%4N6Ba2Op$wC#tLBJYP'

class OdooClient():
    """ class connect odoo client"""
   
    def __init__(self):
        self.url = url
        self.db = db
        self.username = username
        self.password = password


    def logging(self):
        """conecto to xmlrpc odoo client"""
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        common.version()
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        return uid, models