# -*- coding: utf-8 -*-
{
    'name': "bill_invoice_layout_inherit",

    'summary': """
        this texmar gap 8 for modify reports  
        """,

    'description': """
        this texmar gap 8 for modify reports  
  -Use Default Header in Odoo
  -View New Field (Description) From Label Field in Bill  
  -View Taxes Amount from Tax_ids
  -View Taxes Name from Invoice_line_ids 
  -Rate (One Digit Number

""",

    'author': "EgyMentors@Muhammed Ashraf",
    'website': "https://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','egymentors_accounting_enhancement','account', 'sale_discount_total', 'purchase_discount'],

    # always loaded
    'data': [
        'reports/bill_invoice_inherit.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}
