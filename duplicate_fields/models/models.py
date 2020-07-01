 -*- coding: utf-8 -*-

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
    
    _name='amount_total'
    
    name=fields.Char('Name')
        
