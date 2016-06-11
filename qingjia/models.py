# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv import fields, osv

# class Qingjd(models.Model):
#     _name = 'qingjia.qingjd'

#     name = fields.Many2one('res.users', string="申请人", required=True)
#     days = fields.Float(string="天数", required=True,help="请假天数从假日生效日开始计算")
#     startdate = fields.Date(string="开始日期", required=True)
#     reason = fields.Text(string="请假事由")

#     def send_qingjd(self,cr,uid,*args,**kwargs):
#         self.sended = True
#         return self.sended

#     def confirm_qingjd(self,cr,uid,*args,**kwargs):
#         self.state = 'confirmed'
#         return self.state

class Qingid(osv.osv):
    _name = 'qingjia.qingjd'

    def _qingjia_rel_days(self,cr,uid,record_ids,fields,*args,**kwargs):
        res = {}
        for record in self.browse( cr,uid,record_ids):
            res[record.id] = record.days + 1
        return res

    _columns = {
        'name' : fields.many2one('res.users',string="申请人",required=True),
        'days' : fields.float(string="天数", required=True,help="请假天数从假日生效日开始计算"),
        'startdate' : fields.date(string="开始日期", required=True),
        'date' : fields.selection((('0','am'),('1','pm')),string="请假时间"),
        'reason' : fields.text(string="请假事由"),
        'rel_days' : fields.function(_qingjia_rel_days,string="请假实际天数",type="float"),
    }

    def send_qingjd(self,cr,uid,*args,**kwargs):
        self.sended = True
        return self.sended

    def confirm_qingjd(self,cr,uid,*args,**kwargs):
        self.state = 'confirmed'
        return self.state

# from openerp import models, fields, api
# import logging
# class Qingjd(models.Model):
#     _name = 'qingjia.qingjd'
#     name = fields.Many2one('hr.employee', string="申请人", readonly=True)
#     manager = fields.Many2one('hr.employee', string="主管",readonly=True)
#     beginning = fields.Datetime(string="开始时间", required=True,default = fields.Datetime.now())
#     ending = fields.Datetime(string="结束时间", required=True)
#     reason = fields.Text(string="请假事由",required=True)
#     accept_reason = fields.Text(string="同意理由",default="同意。")#########compute 没有写入数据库 on the fly 可以被workflow的condition调用
#     current_name = fields.Many2one('hr.employee', string="当前登录人",compute="_get_current_name")
#     is_manager = fields.Boolean(compute='_get_is_manager')######
#     state = fields.Selection([('draft', "草稿"),('confirmed', '待审核'),('accepted', '批准'),('rejected', '拒绝'),],string='状态',default='draft',readonly=True)
    
#     @api.model#使用新的api
#     def _get_default_name(self):
#         uid = self.env.uid
#         res = self.env['resource.resource'].search([('user_id','=',uid)])
#         name = res.name
#         employee = self.env['hr.employee'].search([('name_related','=',name)])#   
#         for i in self.env.user:# 说明其是recordset#        
#             print('hello')
#             return employee

#     @api.model
#     def _get_default_manager(self):
#     #单记录recordset可以直接用点记号读取属性值
#         uid = self.env.uid
#         res = self.env['resource.resource'].search([('user_id','=',uid)])
#         name = res.name
#         employee = self.env['hr.employee'].search([('name_related','=',name)])logging.info("myinfo  {}".format(employee.parent_id))
#         return employee.parent_id # 似乎有这种数字引用方法值得我们注意

#         _defaults = {
#             'name' : _get_default_name ,
#             'manager' : _get_default_manager ,
#         }
#         def _get_is_manager(self):###这里return不起作用
#             print('----------test')
#             print(self.current_name, self.manager,self.env.uid)
#             if self.current_name == self.manager:
#                 self.is_manager = True
#             else:
#                 self.is_manager = False

#         def _get_current_name(self):
#             uid = self.env.uid
#             res = self.env['resource.resource'].search([('user_id','=',uid)])
#             name = res.name
#             employee = self.env['hr.employee'].search([('name_related','=',name)])
#             self.current_name = employee##############################

#         def draft(self, cr, uid, ids, context=None):
#             if context is None:
#                 context={}
#                 self.write(cr,uid,ids,{'state':'draft'},context=context)
#                 return True

#         def confirm(self, cr, uid, ids, context=None):
#             if context is None:
#                 context={}
#                 self.write(cr,uid,ids,{'state':'confirmed'},context=context)
#                 return True

#         def accept(self, cr, uid, ids, context=None):
#             if context is None:
#                 context={}
#                 self.write(cr,uid,ids,{'state':'accepted'},context=context)
#                 print('你的请假单被批准了')
#                 return True

#         def reject(self, cr, uid, ids, context=None):
#             if context is None:context={}
#                 self.write(cr,uid,ids,{'state':'rejected'},context=context)
#                 print('抱歉，你的请假单没有被批准。')
#                 return True

