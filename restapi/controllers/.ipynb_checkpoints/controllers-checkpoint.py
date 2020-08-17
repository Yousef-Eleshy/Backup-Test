# -*- coding: utf-8 -*-
from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError
import io
import base64
import jwt


class Restapi(http.Controller):
    def __init__(self):
        self.secret = 'secret'
        self.algorithm = 'HS256'
        self.db = 'yousef-eleshy-mentors-devs-restapi-2-1371421'
    
    def authrize_developer(self,token):
        token_record = request.env['restapi.tokens'].sudo().search([('name','=',token)]).name
        if not token_record:
            return False
        try:
            jwt.decode(token_record,self.secret,[self.algorithm])
        except jwt.ExpiredSignatureError:
            return False
    
    def authrize_user(self,token):
        try:
            token_info = jwt.decode(token,self.secret,[self.algorithm])
            user = request.env['res.users'].sudo().search([('id','=',token_info['user_id'])])
            token_record = request.env['restapi.user.tokens'].sudo().search([('name','=',token)])
            if token:
                return token_info
            else:
                return False     
        except:
            return False
            
            
    def prepare_allowed_companies(self,login):
            user  = request.env['res.users'].search([('login','=',login)])
            ids = [company.id for company in user.company_id]
            return ids
    
    def get_total_sales(self,sales):
        sum = 0
        for sale in sales:
            sum += sale.amount_total
        return sum
    
    def get_percentage(self,perv_sale,sale):
        return ((sale - perv_sale) / perv_sale) * 100 if perv_sale != 0 else 100
    
    def product_info(self,product):
        image = product.image_1920
        availability = 'In Stock' if product.virtual_available > 0 else 'Out Of Stock'
        return {
            'product_id':product.id,
            'product_name':product.name,
            'product_code':product.default_code,
            'price':product.list_price,
            'availability':availability,
            'image':base64.b64decode(image) if image else '',
            }
    
    def get_params(self,url):
        params = url.split('?')
        params = params[1].split('&')
        result = {}
        for param in params:
            key_value = param.split('=')
            result[key_value[0].strip()] =  int(key_value[1].strip())
        return result
            
        
        
        

    

    

    


        

    

    
                                                         

    