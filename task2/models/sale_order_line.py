# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError
from odoo.osv import expression
from odoo.tools.float_utils import float_round
from datetime import datetime
import operator as py_operator

class ForcastQty(models.Model):
    _inherit = 'sale.order.line'
    _rec_name = 'name'
    
    virtual_available = fields.Float(related='product_id.virtual_available', readonly=True,string='Available Quantity')
    batch = fields.Many2many('stock.quant',string='Batch')
