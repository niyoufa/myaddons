# -*- coding: utf-8 -*-

from openerp.osv import osv,fields
from openerp import tools, api

class project(osv.osv):
    _name = "project.project"
    _inherit = "project.project"

    _columns = {
        "worksheet":fields.boolean("工作日报"),
    }