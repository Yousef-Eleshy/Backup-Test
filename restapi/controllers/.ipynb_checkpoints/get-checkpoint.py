from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError
import io
import base64
import jwt
from . import controllers

class get(controllers.Restapi):
     @http.route('/web/session/scan_product',type='json',auth='none')
     def scan_product(self,code,base_location=None):
        dev_token = request.httprequest.headers['DevToken']
        user_token = request.httprequest.headers['UserToken'] 
        try:
            if self.authrize_developer(dev_token) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(user_token):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(user_token)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                product = request.env['product.product'].search([('barcode','=',code)],limit=1)
                info = {
                    'name':product.name,
                    'code':product.barcode,
                    'price':product.list_price,
                    'description':product.description,
                    'stock_availability ':product.virtual_available,
                    'product_id':product.id
                }
                return  info
        except AccessError:
            return {'error':'You are not allowed to do this'}
        
     
     @http.route('/web/session/stores_locations',type='json',auth='none')
     def stores_locations(self,base_location=None):
        result = []
        dev_token = request.httprequest.headers['DevToken']
        user_token = request.httprequest.headers['UserToken'] 
        try:
            if self.authrize_developer(dev_token) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(user_token):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(user_token)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                companies = request.env['res.company'].search([])
                for company in companies:
                    vals = {
                            'mobile ':company.phone,
                            'address':company.street or company.street2,
                            'lat':company.lat,
                            'long':company.long,
                        }
                    result.append(vals)
                return result
        except AccessError:
            return 'You are not allowed to do this'
        
     
     @http.route('/web/session/list_customers',type='json',auth='none')
     def list_customers(self,base_location=None):
        result = []
        dev_token = request.httprequest.headers['DevToken']
        user_token = request.httprequest.headers['UserToken'] 
        try:
            if self.authrize_developer(dev_token) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(user_token):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(user_token)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                customers = request.env['res.partner'].search([('customer_rank','=',True)])
                for customer in customers:
                    vals = {
                        'customer_name ':customer.name,
                        'mobile':customer.mobile,
                        'email':customer.email,
                        'customer_id':customer.id,
                        'history' : {}
                    }
                    result.append(vals)
                return result
        except AccessError:
            return {'error':'You are not allowed to do this'}  
        
    
     @http.route('/web/session/popular_products',type='json',auth='none')
     def popular_products(self,base_location=None):
        result = []
        dev_token = request.httprequest.headers['DevToken']
        user_token = request.httprequest.headers['UserToken'] 
        try:
            if self.authrize_developer(dev_token) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(user_token):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(user_token)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                products = request.env['product.template'].search([])
                for product in products:
                    image = product.image_1920
                    availability = 'In Stock' if product.virtual_available > 0 else 'Out Of Stock'
                    vals = {
                        'product_id':product.id,
                        'product_name':product.name,
                        'product_code':product.default_code,
                        'price':product.list_price,
                        'availability':availability,
                        'image':base64.b64decode(image) if image else '',
                    }
                    result.append(vals)
                return result
        except AccessError:
            return {'error':'You are not allowed to do this'}