# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class duplicate_fields(models.Model):
#     _name = 'duplicate_fields.duplicate_fields'
#     _description = 'duplicate_fields.duplicate_fields'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    advanced_amounted =fields.Monetary(related='payment_history_ids.advance_amount')
    advanced_amounted_y =fields.Float(compute='_compute_amount_advanced_amount', store = True)
    
    due_amount = fields.Float(compute='_compute_amount_total_due', store = True)
    
    @api.depends('advanced_amounted','amount_total','return_pay')
    def _compute_amount_total_due(self):
        for record in self:
            record.due_amount = (record.amount_total - record.advanced_amounted_y) - record.return_pay
            
    
    return_pay = fields.Float(compute='_return_pay', store = True)
    
    @api.depends('order_line.qty_delivered','order_line.price_unit')
    def _return_pay(self):
        delivery_line_t = 0
        for record in self:
            for line in record.order_line:
                if line.line_status == "closed":
                    delivery_line = (line.product_uom_qty -line.qty_delivered) * line.price_unit
                    delivery_line_t = delivery_line_t + delivery_line
            record.return_pay = delivery_line_t
                
    
    @api.depends('payment_history_ids.advance_amount')
    def _compute_amount_advanced_amount(self):
        advance_amount_line_t = 0
        for record in self:
            for line in record.payment_history_ids:
                advance_amount_line = line.advance_amount
                advance_amount_line_t = advance_amount_line_t + advance_amount_line
            record.advanced_amounted_y = advance_amount_line_t
                