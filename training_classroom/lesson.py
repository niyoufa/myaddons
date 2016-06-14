# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class training_lesson(osv.osv):
    _name = 'training.lesson'  #本对象的名称
    _inherit = 'training.lesson'  #要继承的对象的_name
    _columns = {
       'classroom_id': fields.many2one('training.classroom', u'教室'), #添加一个教室属性，为多对一对象。
    }
