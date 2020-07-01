# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    
    _inherit = "sale.order.line"
    
    def action_view_delivered_per_line(self):
        pass