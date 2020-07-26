# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import io
import base64
class Restapi(http.Controller):
     @http.route('/web/session/create_customer',type='json',auth='none')
     def getauthentication(self,db,username,password,full_name,country_code,mobile,email,base_location=None):
        request.session.authenticate(db,username,password)
        country = request.env['res.country'].search([('code','=',country_code)],limit=1).id
        vals = {
            'name':full_name,
            'mobile':mobile,
            'email':email,
            'country_id':country,
            'customer_rank':True
        }
        request.env['res.partner'].create(vals)
        return {
            'result':'created successfully'
        }
     @http.route('/web/session/edit_customer',type='json',auth='none')
     def edit_customer(self,db,username,password,customer_id,full_name,country_code,mobile,email,base_location=None):
        request.session.authenticate(db,username,password)
        country = request.env['res.country'].search([('code','=',country_code)],limit=1).id
        customer = request.env['res.partner'].search([('id','=',customer_id)],limit=1)
        vals = {
            'name':full_name,
            'mobile':mobile,
            'email':email,
            'country_id':country,
        }
        customer.write(vals)
        return {
            'result':'edited successfully',
        }
    
     @http.route('/web/session/popular_products',type='json',auth='none')
     def popular_products(self,db,username,password,base_location=None):
        request.session.authenticate(db,username,password)
        result = []
        products = request.env['product.template'].search([])
        for product in products:
            image = product.image_1920
            availability = 'In Stock' if product.virtual_available > 0 else 'Out Of Stock'
            vals = {
                'product_id':product.id,
                'image':base64.b64decode(image) if image else '',
                'product_name':product.name,
                'product_code':product.default_code,
                'price':product.list_price,
                'availability':availability
            }
            result.append(vals)
        return result
    
     @http.route('/web/session/list_customers',type='json',auth='none')
     def list_customers(self,db,username,password,base_location=None):
        request.session.authenticate(db,username,password)
        result = []
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

    