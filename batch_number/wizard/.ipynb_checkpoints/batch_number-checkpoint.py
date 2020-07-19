from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError ,ValidationError
from odoo.tools.float_utils import float_round
from odoo.tools import float_compare

class MrpProductProduceInherit(models.TransientModel):
    _inherit = 'mrp.product.produce'
    batch_number = fields.Selection([
        ('one', 'batch number 1'), ('two', 'batch number 2'),('three', 'batch number 3'), ('four', 'batch number 4'),
        ('five', 'batch number 5'), ('six', 'batch number 6'),
        ('seven', 'batch number 7'), ('eight', 'batch number 8'),('nine', 'batch number 9'), ('ten', 'batch number 10')
    ], string="Batch Number")
    
    
    def _update_finished_move(self):
        """ Update the finished move & move lines in order to set the finished
        product lot on it as well as the produced quantity. This method get the
        information either from the last workorder or from the Produce wizard."""
        production_move = self.production_id.move_finished_ids.filtered(
            lambda move: move.product_id == self.product_id and
            move.state not in ('done', 'cancel')
        )
        if production_move and production_move.product_id.tracking != 'none':
            if not self.finished_lot_id:
                raise UserError(_('You need to provide a lot for the finished product.'))
            move_line = production_move.move_line_ids.filtered(
                lambda line: line.lot_id.id == self.finished_lot_id.id
            )
            if move_line:
                if self.product_id.tracking == 'serial':
                    raise UserError(_('You cannot produce the same serial number twice.'))
                move_line.product_uom_qty += self.qty_producing
                move_line.qty_done += self.qty_producing
            else:
                location_dest_id = production_move.location_dest_id._get_putaway_strategy(self.product_id).id or                                     production_move.location_dest_id.id
                move_line.create({
                    'move_id': production_move.id,
                    'product_id': production_move.product_id.id,
                    'lot_id': self.finished_lot_id.id,
                    'product_uom_qty': self.qty_producing,
                    'product_uom_id': self.product_uom_id.id,
                    'qty_done': self.qty_producing,
                    'location_id': production_move.location_id.id,
                    'location_dest_id': location_dest_id,
                #hatem start
                    'batch_number':self.batch_number
                })
                self.finished_lot_id.batch_number = self.batch_number
                #hatem end
        
                
        else:
            rounding = production_move.product_uom.rounding
            production_move._set_quantity_done(
                float_round(self.qty_producing, precision_rounding=rounding)
            )