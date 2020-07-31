# -*- coding: utf-8 -*-
{
    'name': "restapi",

    'summary': """
        this module for test rest api 
        """,

    'description': """
       this module for test rest api
    """,

    'author': "EgyMentors",
    'website': "https://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock','account','hr'],

    # always loaded
    'data': [
        'views/company_location.xml',
        'security/group.xml',
        'security/ir.model.access.csv'
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}
