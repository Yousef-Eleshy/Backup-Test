# -*- coding: utf-8 -*-
from odoo import http,fields,models
from odoo.http import request
import io
import base64
class Restapi(http.Controller):
     def prepare_allowed_companies(self,user_id):
            user = request.env['res.users'].search([('id','=',user_id)])
            ids = [company.id for company in user.company_id]
            return ids
        
     @http.route('/web/session/create_customer',type='json',auth='none')
     def create_customer(self,full_name,country_code,mobile,email,base_location=None):
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
            'created successfully'
        }
    
     @http.route('/web/session/edit_customer',type='json',auth='none')
     def edit_customer(self,customer_id,full_name,country_code,mobile,email,base_location=None):
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
            'edited successfully',
        }
    
     @http.route('/web/session/popular_products',type='json',auth='none')
     def popular_products(self,base_location=None):
        result = []
        products = request.env['product.template'].sudo().search([('name','=','Test')])
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
    
     @http.route('/web/session/list_customers',type='json',auth='none')
     def list_customers(self,base_location=None):
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
     @http.route('/web/session/sales_home',type='json',auth='none')
     def sales_home(self,user_id,base_location=None):
        result = []
        allowed_companies = self.prepare_allowed_companies(user_id)
        sales = request.env['sale.order'].sudo().search([('company_id','in',allowed_companies)])
        sales_today = [sale for sale in sales if sale.date_order.day == fields.date.today().day and sale.date_order.month == fields.date.today().month and sale.date_order.year == fields.date.today().year]
        sales_yesterday = [sale for sale in sales if sale.date_order.day == fields.date.today().day - 1 and sale.date_order.month == fields.date.today().month and sale.date_order.year == fields.date.today().year]
        sales_today_sum = 0
        sales_yesterday_sum = 0
        for sale in sales_today:
            sales_today_sum += sale.amount_total
        for sale in sales_yesterday:
            sales_yesterday_sum += sale.amount_total
        perc = ((sales_today_sum - sales_yesterday_sum) / sales_yesterday) * 100 if sales_yesterday_sum != 0 else 100
        return {
            'today_sales_amount':sales_today_sum,
            'today_sales_percentage':perc,
            'draft_notes':[]
        }
    
     @http.route('/web/session/scan_product',type='json',auth='none')
     def scan_product(self,code,base_location=None):
        product = request.env['product.product'].sudo().search([('barcode','=',code)],limit=1)
        info = {
            'name':product.name,
            'code':product.barcode,
            'price':product.list_price,
            'description':product.description,
            'stock_availability ':product.virtual_available,
            'product_id':product.id
        }
        return  info
    
     @http.route('/web/session/forget_password',type='json',auth='none')
     def forget_password(self,email,base_location=None):
        email = 'hatemmostafa31@gmail.com'
        request.session.authenticate('yousef-eleshy-mentors-devs-task2-api-1312735',email,'admin')
        user = request.env['res.users'].search([('login','=',email)],limit=1)
        user.sudo().action_reset_password()
        return  'resend a reset password to user mail'                                          
                       
                                                         

    