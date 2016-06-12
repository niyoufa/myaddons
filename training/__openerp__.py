# -*- coding: utf-8 -*-
{
    'name': "Training",

    'summary': """
        课程模块
        """,

    'description': """
        需求描述
        输入和查询课程,把信息储存到课程对象里
        课程包含以下信息：名称，价格，天数，开始日期，教师，学员
        每个课程可以有多个学员，要记录学员的姓名、电话、电子邮件
        课程可以添加教材和作业等文档附件
        用户可以设置默认值以加速输入
        可以按名称查询课程，也可以用其他信息查找课程，并保存常用查询条件
        可以导出课程信息到excel文件，并支持导入
        可以按日期查看课程，并调整课程时间
        老师只能看到自己的课程
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}