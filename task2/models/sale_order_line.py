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
    batch = fields.Many2many('stock.quant',string='Batch',company_dependent=False,check_company=False)
    
    @api.onchange('batch')
    def batch_quantity(self):
        qty = 0
        for batch in self.batch:
            qty += batch.lot_id.product_qty 
            batch.company_dependent = False
            batch.check_company=False
        self.product_uom_qty = qty

    
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
    
#     def action_confirm(self):
#         raise ValidationError('sasasaas')
#         for rec in self:
#             lines = rec.order_line
#             for line in lines:
#                 batches = line.batch
#                 for batch in batches:
#                     batch.write({'state':'reserved'})
        
#         return super(SaleOrder, self).action_confirm()

        
