# -*- coding: utf-8 -*-
from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError
import io
import base64
class Restapi(http.Controller):
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
        
        
        

    

    

    


        

    

    
                                                         

    