# -*- coding: utf-8 -*-
{
    'name': "作业本",

    'summary': """
        作业本后台管理系统""",

    'description': """
        作业本后台管理系统，用于管理作业本网站和app的用户，资源，课程，作业等资源。
    """,

    'author': "Youfa Ni",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': '教育',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/schoolwork_security.xml',
        # 'security/ir.model.access.csv',
        'views/user_view.xml',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
