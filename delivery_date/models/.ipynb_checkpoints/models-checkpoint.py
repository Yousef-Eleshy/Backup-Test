# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, RedirectWarning, UserError

class Mo(models.Model):
    _inherit = 'mrp.production'
    
#     date_deadline = fields.Date(string='Deadline',store=True,readonly=True,related='sale_line_id.line_delivery_date')

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
        #mentors start
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
#           adding terms to mo
                    mo = self.sudo().env['mrp.production'].search([('origin','=',f"{sale.name}/{purchase_order.name}")])
                    mo.notes = notes
                    if not(mo.date_deadline):
                        mo.date_deadline = self.date_order
                        
                self.add_delivery(purchase_order)

        #mentors end
        return True
    
    

# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'

#     def write(self, vals):
#             self.add_delivery_date()
#             """
#             Change Status Of SO
#             :param vals:
#             :return:
#             """
#             super(SaleOrderLineInherit, self).write(vals)
#             if vals.get('line_status'):
#                 # Check Other Lines:
#                 for line in self:
#                     if line.order_id:
#                         if all(line_status == 'closed' for line_status
#                                 in line.order_id.order_line.mapped('line_status')):
#                             status = 'closed'
#                         else:
#                             status = 'open'
#                         line.order_id.write({'order_status': status})
#                 return True
#         def add_delivery_date(self):
#             mo = self.env['mrp.production'].search([('')])