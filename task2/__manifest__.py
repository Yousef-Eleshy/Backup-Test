# -*- coding: utf-8 -*-
{
    'name': "task2_texmar",

    'summary': """
        Tasks 2 Texmar
        
        """,

    'description': """
        Tasks 2 Texmar
    """,

    'author': "EgyMentors, Hatem & Muhammed",
    'website': "https://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','product','account','stock'],

    # always loaded
    'data': [
        'security/multy_company_security.xml',
        'views/sale_order_line.xml',
    ],
    # only loaded in demonstration mode
   
}
