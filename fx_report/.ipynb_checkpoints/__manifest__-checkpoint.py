# -*- coding: utf-8 -*-
{
    'name': "FX Report",

    'summary': """
        FX Report Print""",

    'description': """
        FX Report Print
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'egymentors_purchase_fx', 'purchase', 'purchase_stock'],

    # always loaded
    'data': [
        'reports/reports.xml',
        'reports/fx_report.xml',
    ],
}
