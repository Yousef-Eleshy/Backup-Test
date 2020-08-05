from odoo import models, fields, api

class total_tax(models.Model):
    _inherit = 'account.move.line'
    total_with_tax=fields.Float(compute='_calc_total_tax', store = True)
    
    @api.depends('tax_ids','price_subtotal')
    def _calc_total_tax(self):
        for line in self:
            sum=0
            for tax in line.tax_ids:
                sum+=tax.amount
            if sum==0:
                line.total_with_tax=0
            else:
                line.total_with_tax= (sum/100)*line.price_subtotal + line.price_subtotal

    
    