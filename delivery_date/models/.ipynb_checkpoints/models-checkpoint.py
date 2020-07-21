# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, RedirectWarning, UserError

class Mo(models.Model):
    _inherit = 'mrp.production'
    
    date_deadline = fields.Datetime(string='Deadline',store=True,readonly=True,related='sale_line_id.line_delivery_date')
    

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))
        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'sale',
            'date_order': fields.Datetime.now()
        })
        self._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        #Mentors start
        notes = self.note
#        # adding customer name and phone and terms to purchase from sales
        purchase_orders = self.sudo().env['purchase.order'].search([('origin','=',self.name)])
        
        if purchase_orders:
            for purchase_order in purchase_orders:
                purchase_order.customer_name = self.partner_id['name']
                purchase_order.customer_phone = self.partner_id['mobile']
                purchase_order.notes = notes 
#           adding customer name and phone and terms to main sales from purchase
                sales = self.sudo().env['sale.order'].search([('name','=',purchase_order.partner_ref)])
                for sale in sales:
                    sale.branch_customer_name = self.partner_id['name']
                    sale.branch_customer_phone = self.partner_id['mobile']
                    sale.note = notes
                    sale.branch_delivery_states = self.delivery_states
                    sale.add_delivery(purchase_order)
#            adding customer name and phone and terms to main delivery from main sales
                    deliveries = self.sudo().env['stock.picking'].search([('origin','=',f'{sale.name}/{purchase_order.name}')])
                    for delivery in deliveries:
                        delivery.branch_customer_name = self.partner_id['name']
                        delivery.branch_customer_phone = self.partner_id['mobile']
#           adding terms and deadline date to mo 
                    mos = self.sudo().env['mrp.production'].search([('origin','=',f"{sale.name}/{purchase_order.name}")])
                    for mo in mos:
                        mo.notes = notes
                        if not(mo.date_deadline):
                            mo.date_deadline = self.date_order
                            mo.date_planned_finished = self.date_order
                            
                self.add_delivery(purchase_order)
                
            
        else:
            mos = self.sudo().env['mrp.production'].search([('origin','=',f"{self.name}")]) or \
                    self.sudo().env['mrp.production'].search([('origin','=',f"{self.name}/{self.client_order_ref}")])
            for mo in mos:
                if not(mo.date_deadline):
                    mo.date_deadline = self.date_order
                    mo.date_planned_finished = self.date_order
                    
        #Mentors end
        return True
    
    

class SaleOrderLineInherit(models.Model):
	_inherit = 'sale.order.line'
    
	line_delivery_date = fields.Datetime("Delivery Date")