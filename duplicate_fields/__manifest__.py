# -*- coding: utf-8 -*-
{
    'name': "Duplicate fields",

    'summary': """
        duplicated (total,advance payment total,return,due amount)""",

    'description': """
       duplicated (total,advance payment total,return(from delivery),due amount)
    """,

    'author': "Egymentors-Hamza",
    'website': "www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','so_po_advance_payment_app'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': True,
}
