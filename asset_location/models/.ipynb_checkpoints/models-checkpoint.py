# -*- coding: utf-8 -*-

from odoo import models, fields


class AssetLocation(models.Model):
    _name = 'asset.location'
    _inherit = ['mail.thread']
    
    name = fields.Char(string="Asset Location", required=True)
    parent = fields.Many2one('asset.location', string="Parent Location")
    
    

class AccountAssets(models.Model):
    _inherit = 'account.asset'

    assets_location = fields.Many2one('asset.location', 'Asset Location')