# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Partner(models.Model):
    _inherit = 'res.partner'


    #When the Country is Egypt
    @api.constrains('mobile')
    def _onchange_mobile(self):
        if self.country_id.name == 'Egypt':
            self.onchange_mobile()
            
    #Only numbers and 11 (16 including spaces) digits only
    def onchange_mobile(self):
        if self.mobile:
            if len(self.mobile) != 16:
                raise ValidationError(_("WARNING: Please Enter a Valid 11 Digit Mobile Number"))
        digits = [' ','+','0','1','2','3','4','5','6','7','8','9']
        for i in list(self.mobile):
            if i in digits:
                continue
            else:
                raise ValidationError("WARNING: Mobile Numbers %s , Should only contain Numbers" % (self.mobile))
    
    # Make sure the Mobile Number is Unique
#     _sql_constraints = [
#                      ('mobile', 
#                       'unique(mobile)',
#                       'WARNING: Another Contact with this Mobile Number Already Exists')
#     ]
    
    @api.constrains('mobile')
    def mobile_unique_constrain(self):
        for partner in self:
            if partner.ref and self.env['res.partner'].search_count([('mobile', '=', partner.mobile)]) > 1:
                raise Warning(_("WARNING: Another Contact with this Mobile Number Already Exists"))