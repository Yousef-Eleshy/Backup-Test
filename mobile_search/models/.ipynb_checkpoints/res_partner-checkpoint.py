# -*- coding: utf-8 -*-

from odoo import models, api,_
from odoo.exceptions import ValidationError, AccessError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """ This method will find Customer names according to their mobile,
        phone, city, email and its job position."""
        if name and not self.env.context.get('import_file'):
            #name.replace(" ","")
            #name = [i.replace(",", "") for i in name]
            
            args = args if args else []
            args.extend(['|', ['name', 'ilike', name],
                         '|', ['mobile', 'ilike', name],
                         '|', ['city', 'ilike', name],
                         '|', ['email', 'ilike', name],
                         '|', ['phone', 'ilike', name],
                         ['function', 'ilike', name]])
            name = ''
        return super(ResPartner, self).name_search(
            name=name, args=args, operator=operator, limit=limit)