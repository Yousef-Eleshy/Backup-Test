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
        self.db = 'yousef-eleshy-mentors-devs-restapi-1317643'
    
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
            
            
    def prepare_allowed_companies(self,user_id):
            user = request.env['res.users'].search([('id','=',user_id)])
            ids = [company.id for company in user.company_id]
            return ids
    
    def get_total_sales(self,sales):
        sum = 0
        for sale in sales:
            sum += sale.amount_total
        return sum
    
    def get_percentage(self,perv_sale,sale):
        return ((sale - perv_sale) / perv_sale) * 100 if perv_sale != 0 else 100
        
        
        

    

    

    


        

    

    
                                                         

    