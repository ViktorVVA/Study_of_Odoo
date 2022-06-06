# -*- coding: utf-8 -*-
{
    'name': "Openacademy",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'board'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/openacademy_menu.xml',
        'views/course_views.xml',
        'views/partner_views.xml',
        'views/session_views.xml',
        'wizards/session_wizard_views.xml',
        'views/templates.xml',
        'reports/session_board.xml',
        'reports/session_report.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/course_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
