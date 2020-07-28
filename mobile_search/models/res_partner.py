# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    modified_mobile = fields.Char(string='Modified Mobile', compute='get_modified_mobile_number', store=True)

    @api.depends('mobile')
    def get_modified_mobile_number(self):
        for partner in self:
            if partner.mobile:
                partner.modified_mobile = partner.mobile.replace(" ", "")
            else:
                partner.modified_mobile = ' '

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if name and not self.env.context.get('import_file'):
            args = args if args else []
            args.extend(['|', ['name', 'ilike', name],
                         '|', ['mobile', 'ilike', name],
                         '|', ['modified_mobile', 'ilike', name],
                         '|', ['city', 'ilike', name],
                         '|', ['email', 'ilike', name],
                         '|', ['phone', 'ilike', name],
                         ['function', 'ilike', name]])
            name = ''

        return super(ResPartner, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
