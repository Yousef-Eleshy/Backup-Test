# -*- coding: utf-8 -*-
 
from odoo import models, fields, api


class restapi(models.Model):
    _inherit = 'res.company'
    
    lat = fields.Char(string='latitude')
    long = fields.Char(string='longitude')

    
