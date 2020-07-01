# -*- coding: utf-8 -*-
{
    'name': "Delivery History",

    'summary': """
        Create Delivery Date Change history""",

    'description': """
        Create Button in Sale order line to view the history of changing the values of delivery Date in SOL.
    """,

    'author': "Egymnetors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','stock','egymentors_purchase_fx','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_line_view.xml',
        'views/delivery_date_history.xml',
    ],

}
