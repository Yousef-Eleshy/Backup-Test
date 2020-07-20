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
    batch2 = fields.Many2one('stock.quant',string='Batch2',check_company=False)
    
    @api.onchange('batch')
    def batch_quantity(self):
        qty = 0
        for batch in self.batch:
            qty += batch.lot_id.product_qty 
        self.product_uom_qty = qty
    
class StockQuant(models.Model):
    _inherit = 'stock.quant'
    _rec_name = 'name'
    
    name = fields.Char(default='Hatem',compute='_compute_name')
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
    @api.model
    def create(self, vals):
        """ Override to handle the "inventory mode" and create a quant as
        superuser the conditions are met.
        """
        if self._is_inventory_mode() and 'inventory_quantity' in vals:
            allowed_fields = self._get_inventory_fields_create()
            if any([field for field in vals.keys() if field not in allowed_fields]):
                raise UserError(_("Quant's creation is restricted, you can't do this operation."))
            inventory_quantity = vals.pop('inventory_quantity')

            # Create an empty quant or write on a similar one.
            product = self.env['product.product'].browse(vals['product_id'])
            location = self.env['stock.location'].browse(vals['location_id'])
            lot_id = self.env['stock.production.lot'].browse(vals.get('lot_id'))
            package_id = self.env['stock.quant.package'].browse(vals.get('package_id'))
            owner_id = self.env['res.partner'].browse(vals.get('owner_id'))
            quant = self._gather(product, location, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=True)
            if quant:
                quant = quant[0]
            else:
                quant = self.sudo().create(vals)
            # Set the `inventory_quantity` field to create the necessary move.
            quant.inventory_quantity = inventory_quantity
            return quant
        res = super(StockQuant, self).create(vals)
#         if self._is_inventory_mode():
#             res._check_company()
        return res
        
