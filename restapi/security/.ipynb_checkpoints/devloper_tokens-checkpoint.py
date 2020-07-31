from odoo import models, fields, api


class Token(models.Model):
    _name = 'restapi.tokens'
    
    name = fields.Char()