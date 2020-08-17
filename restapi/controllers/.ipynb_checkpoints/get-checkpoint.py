from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError
import io
import base64
import jwt
import re
from datetime import datetime,timedelta,timezone
from . import controllers

class get(controllers.Restapi):
     @http.route('/scan_product',type='json',auth='none')
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
                    'description':product.description if product.description else '' ,
                    'stock_availability ':product.virtual_available,
                    'product_id':product.id
                }
                return info if product else 'no product found'
        except AccessError:
            return {'error':'You are not allowed to do this'}
        
     
     @http.route('/stores_locations',type='json',auth='none')
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
        
     
     @http.route('/list_customers',type='json',auth='none')
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
                customers = request.env['res.partner'].search([('customer_rank','=',True),('company_id','=',False)])
                for customer in customers:
                    vals = {
                        'customer_name ':customer.name,
                        'mobile':customer.mobile,
                        'email':customer.email,
                        'customer_id':customer.id,
                        'history' : {}
                    }
                    result.append(vals)
                return result if len(result) > 0 else 'no customers found'
        except AccessError:
            return {'error':'You are not allowed to do this'}  
        
    
     @http.route('/popular_products',type='json',auth='none')
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
                params = self.get_params(request.httprequest.url)
                limit = params.get('limit',5)
                offset = params.get('offset',0)
                
                user_info = self.authrize_user(user_token)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                
                products = request.env['product.product'].search([('company_id','=',False)],limit=limit,offset=offset)
                
                for product in products:
                    image = product.image_1920
                    availability = 'In Stock' if product.virtual_available > 0 else 'Out Of Stock'
                    result.append(self.product_info(product))
                    
                return result if len(result) > 0 else 'no products found'  
        except AccessError:
            return {'error':'You are not allowed to do this'}
     
     @http.route('/new_products',type='json',auth='none')
     def new_product(self,base_location=None):
        result = []
        dev_token = request.httprequest.headers['DevToken']
        user_token = request.httprequest.headers['UserToken']
        try:
            if self.authrize_developer(dev_token) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(user_token):
                return {'error':'invalid user token'}
            else:
                params = self.get_params(request.httprequest.url)
                limit = params.get('limit',5)
                offset = params.get('offset',0)
                
                user_info = self.authrize_user(user_token)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                
                exp_time = datetime.utcnow() - timedelta(days=30)
                products = request.env['product.product'].search([('company_id','=',False),('create_date','>',exp_time)],limit=limit,offset=offset)
                
                for product in products:
                    result.append(self.product_info(product))
                    
                return result if len(result) > 0 else 'no products found'
            
        except AccessError:
            return {'error':'You are not allowed to do this'}
     
     @http.route('/search_products',type='json',auth='none')
     def search_products(self,keyword,base_location=None):
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
                products = request.env['product.product'].search([('company_id','=',False)])
                result = []
                for product in products:
                    search = str(keyword).lower()
                    code = '' if not product.default_code else product.default_code.lower()
                    
                    if re.search(search,product.name.lower()) != None or                                                                                                      re.search(search,code) != None:
                        result.append(self.product_info(product))
                        
                return result if len(result) > 0 else 'no product found'
                    
                
        except AccessError:
            return {'error':'You are not allowed to do this'}