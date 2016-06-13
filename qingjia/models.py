# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv import fields, osv

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
