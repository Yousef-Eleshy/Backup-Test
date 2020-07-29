# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SpecsConditions(models.Model):
    _inherit = 'sale.order'
    
    
    specs_conditions = fields.Html(string='Offer Specifications and Conditions', required=True, default="""
                                    <ul>
                                    <li><b>All prices are in Egyptian pound LE and subject to 14% vat.</b></li>
                                    <li>Please note any fabric marked WRF are 100% flam ratadant polyster durable for 12 to 16 wash to match and pass the highest required American standard NFPA701</li>
                                    <li>All original fabric is construction engineered to match the project durability use and safety requirements.</li>
                                    <li>All fabrics made to pass aatcc 16e (U.S.A) Xeon test 5 blue scale minimum (for light fastness)</li>
                                    <li>Fabric specifications for indoor use only</li>
                                    <li>All fabrics made to pass aatcc 8 (U.S.A) for dry and wet grey scale (crocking fastness rubbing)</li>
                                    <li>All upholstery fabrics made to pass astm 4966 Abrasion test for upholstery items (20000 rubs minimum)</li>
                                    <p>Ordered qty subject for (5% + or -) on delivery</p>""")
    
