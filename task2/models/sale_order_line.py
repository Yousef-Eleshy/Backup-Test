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
    batch = fields.Many2many('stock.quant',string='Batch',check_company=True)
    
    @api.onchange('batch')
    def batch_quantity(self):
        qty = 0
        for batch in self.batch:
            qty += batch.lot_id.product_qty 
        self.product_uom_qty = qty

        
class StockQuant(models.Model):
    _inherit = 'stock.quant'
    _rec_name = 'name'
    
    name = fields.Char(compute='_compute_name')
    batch_number = fields.Selection([
        ('one', 'batch number 1'), ('two', 'batch number 2'),('three', 'batch number 3'), ('four', 'batch number 4'),
        ('five', 'batch number 5'), ('six', 'batch number 6'),
        ('seven', 'batch number 7'), ('eight', 'batch number 8'),('nine', 'batch number 9'), ('ten', 'batch number 10')
    ], string="Batch Number",related='lot_id.batch_number')
    
    @api.depends('lot_id','batch_number','inventory_quantity')
    def _compute_name(self):
        for rec in self:
            lot = rec.lot_id.name or ''
            if rec.batch_number:  
                batch = f'Batch {rec.batch_number}'
            else:
                batch = ''
            qty = rec.lot_id.product_qty 

            rec.name = f'{batch} || {lot} || {qty}' 
