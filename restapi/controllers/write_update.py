from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError
import io
import base64
from . import controllers

class write_update(controllers.Restapi):
     @http.route('/edit_customer',type='json',auth='none')
     def edit_customer(self,customer_id,full_name,country_code,mobile,email,base_location=None):
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
                country = request.env['res.country'].search([('code','=',country_code)],limit=1).id
                if not country:
                    return 'invalid country code'
                customer = request.env['res.partner'].search([('id','=',customer_id)],limit=1)
                if not customer:
                    return 'customer not found'
                vals = {
                    'name':full_name,
                    'phone':mobile,
                    'mobile':mobile,
                    'email':email,
                    'country_id':country,
                }
                customer.write(vals)
                return 'edited successfully'
        
        except AccessError:
            return {'error':'You are not allowed to do this'}
        
        except ValidationError as e:
            return {'error':e.name}
     
     @http.route('/create_customer',type='json',auth='none')
     def create_customer(self,email,full_name,country_code,mobile,base_location=None):
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
                country = request.env['res.country'].search([('code','=',country_code.upper())],limit=1).id
                if not country:
                    return 'invalid country code'
                vals = {
                    'name':full_name,
                    'mobile':mobile,
                    'email':email,
                    'country_id':country,
                    'customer_rank':True
                }
                request.env['res.partner'].create(vals)
                return 'created successfully '
            
        except AccessError:
            return {'error':'You are not allowed to do this'}
        
        except ValidationError as e:
            return {'error':e.name}
            

