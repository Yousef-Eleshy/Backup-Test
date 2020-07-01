# -*- coding: utf-8 -*-
{
    'name': "advacne_payment_button",

    'summary': """
        This module for update state invisible for advance payment method
        """,

    'description': """
         This module for update state invisible for advance payment method
    """,

    'author': "EgyMentors",
    'website': "https://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','sale','so_po_advance_payment_app','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'installable':True,
    'auto_install':False,
    'application':True,
}
