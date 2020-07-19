# -*- coding: utf-8 -*-
{
    'name': "Batch Number",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/mrp_move_line.xml',
        'views/production_lot.xml',
        'wizard/batch_number.xml'
    ],
}
