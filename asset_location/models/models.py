# -*- coding: utf-8 -*-

from odoo import models, fields


class AssetLocation(models.Model):
    _name = 'asset.location'
    _inherit = ['mail.thread']
    
    name = fields.Char(string="Asset Location", required=True)
    parent = fields.Char(string="Parent Location", required=True)