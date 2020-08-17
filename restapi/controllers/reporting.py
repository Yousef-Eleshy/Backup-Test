from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError
import io
import base64
from . import controllers
class reporting(controllers.Restapi): 
    
     @http.route('/sales_home',type='json',auth='none')
     def sales_home(self,base_location=None):
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
                allowed_companies = self.prepare_allowed_companies(user_info['login'])
                sales = request.env['sale.order'].search([('company_id','in',allowed_companies)])

                #dates
                day = fields.date.today().day 
                month = fields.date.today().month
                year = fields.date.today().year
                #filtering sale depending on date
                sales_today = [sale for sale in sales if sale.date_order.day == day and sale.date_order.month == month and sale.date_order.year == year]                                                        
                sales_yesterday = [sale for sale in sales if sale.date_order.day == day - 1 and sale.date_order.month == month and sale.date_order.year == year]  
                # getting the sum of all sales
                sales_today_sum = self.get_total_sales(sales_today)
                sales_yesterday_sum = self.get_total_sales(sales_yesterday)

                # calculating the percentage
                perc = self.get_percentage(sales_yesterday_sum,sales_today_sum) if sales_today_sum > 1 else -100 #abbas
                
                return {
                    'today_sales_amount':sales_today_sum,
                    'today_sales_percentage':float("{0:.1f}".format(perc)),
                    'draft_notes':[]
                }
        except AccessError:
            return {'error':'You are not allowed to do this'}
        
    
    
     @http.route('/sales_dashboard',type='json',auth='none')
     def sales_dashboard(self,base_location=None):
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
                allowed_companies = self.prepare_allowed_companies(user_info['login'])
                sales = request.env['sale.order'].search([('company_id','in',allowed_companies)])

                #dates
                day = fields.date.today().day 
                month = fields.date.today().month
                year = fields.date.today().year
                #filtering sale depending on date
                sales_today = [sale for sale in sales if sale.date_order.day == day and sale.date_order.month == month and sale.date_order.year == year]                                                        
                sales_yesterday = [sale for sale in sales if sale.date_order.day == day - 1 and sale.date_order.month == month and sale.date_order.year == year]                                                          
                sales_this_month = [sale for sale in sales if sale.date_order.month == month and sale.date_order.year == year]                                                                                                                                             
                sales_last_month = [sale for sale in sales if sale.date_order.month == month - 1 and sale.date_order.year == year]                                                                           

                # getting the sum of all sales
                sales_today_sum = self.get_total_sales(sales_today)
                sales_yesterday_sum = self.get_total_sales(sales_yesterday)
                sales_this_month_sum = self.get_total_sales(sales_this_month)
                sales_last_month_sum = self.get_total_sales(sales_last_month)

                # calculating the percentage
                daily_perc = self.get_percentage(sales_yesterday_sum,sales_today_sum) if sales_today_sum > 1 else -100
                monthly_perc = self.get_percentage(sales_last_month_sum,sales_this_month_sum) if sales_this_month_sum > 1 else -100

                return {'sales' : [
                            {'period' : 'daily' , 'amount': sales_today_sum , 'percentage' : float("{0:.1f}".format(daily_perc))},
                            {'period' : 'monthly' , 'amount': sales_this_month_sum , 'percentage' :float("{0:.1f}".format(monthly_perc))},
                            ],
                                    'target' : { 'date' : '', 'sales_amount': '','sales_percentage' : '','target_amount': '' } ,
                                    'history' :
                                    [ {'date': '' , 'sales_amount' : '' }] ,
                        }
        except AccessError:
            return 'You are not allowed to do this'
        
                                                       