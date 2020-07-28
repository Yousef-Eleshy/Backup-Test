from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError
import io
import base64
from . import controllers

class write_update(controllers.Restapi):
     @http.route('/web/session/edit_customer',type='json',auth='none')
     def edit_customer(self,customer_id,full_name,country_code,mobile,email,base_location=None):
        try:
            email = 'hatemmostafa31@gmail.com'
            request.session.authenticate('yousef-eleshy-mentors-devs-task2-api-1312735',email,'admin')
            country = request.env['res.country'].sudo().search([('code','=',country_code)],limit=1).id
            customer = request.env['res.partner'].sudo().search([('id','=',customer_id)],limit=1)
            vals = {
                'name':full_name,
                'mobile':mobile,
                'email':email,
                'country_id':country,
            }
            customer.sudo().write(vals)
            return 'edited successfully',
        
        except AccessError:
            return 'You are not allowed to do this'
        
        except ValidationError as e:
            return e.name
     
     @http.route('/web/session/create_customer',type='json',auth='none')
     def create_customer(self,email,full_name,country_code,mobile,base_location=None):
        try:
            auth_email = 'hatemmostafa31@gmail.com'
            request.session.authenticate('yousef-eleshy-mentors-devs-task2-api-1312735',auth_email,'admin')
            country = request.env['res.country'].sudo().search([('code','=',country_code)],limit=1).id
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
            return 'You are not allowed to do this'
        
        except ValidationError as e:
            return e.name
            

