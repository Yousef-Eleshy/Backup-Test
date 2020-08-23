'''
add file churn with the script inside the dirctory 
'''

from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError
from . import churn

class Restapi(http.Controller):    
    
    @http.route('/churn',type='json',auth='none')
    def churn(self,before,after,author,base_location=None):
        return churn.main(before=before,after=after,author=author,dir='/home/odoo/src/user/')