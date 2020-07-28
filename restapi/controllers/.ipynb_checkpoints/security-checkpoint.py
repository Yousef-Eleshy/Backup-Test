from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError
import io
import base64
from . import controllers

class security(controllers.Restapi):
     @http.route('/web/session/forget_password',type='json',auth='none')
     def forget_password(self,email,base_location=None):
        try:
            email = 'hatemmostafa31@gmail.com'
            request.session.authenticate('yousef-eleshy-mentors-devs-task2-api-1312735',email,'admin')
            user = request.env['res.users'].search([('login','=',email)],limit=1)
            user.sudo().action_reset_password()
            return  'resend a reset password to user mail'
        except AccessError:
            return 'You are not allowed to do this'