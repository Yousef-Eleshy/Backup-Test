from odoo import models, fields, api


class UserTokens(models.Model):
    _name = 'restapi.user.tokens'
    
    name = fields.Char()
    user_id = fields.Many2one('res.users')