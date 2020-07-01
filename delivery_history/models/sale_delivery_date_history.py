# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleDeliveryDateHistory(models.Model):
    
    _name = "sale.delivery.date.history"
    
    
#     sale_order_line_id = fields.One2many('sale.order.line')
#     delivery_date = fields.Date('Delivery Date')
#     delivery_date = fields.Date('Editing Date')
    
#     def action_view_delivered_per_line(self):
#         pass