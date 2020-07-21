# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Partner(models.Model):
    _inherit = 'res.partner'



    @api.constrains('mobile')
    def _onchange_mobile(self):
        if self.country_id.name == 'Egypt':
            self.onchange_mobile()
    #Only numbers and 11 (16 including spaces) digits only
    def onchange_mobile(self):
        if self.mobile:
            if len(self.mobile) != 16:
                raise ValidationError(_("Enter valid 11 digits Mobile number"))
        digits = [' ','+','0','1','2','3','4','5','6','7','8','9']
        for i in list(self.mobile):
            if i in digits:
                continue
            else:
                raise ValidationError("Attention !! Mobile number %s , should contains only numbers" % (self.mobile))