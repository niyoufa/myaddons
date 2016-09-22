#coding=utf-8

from openerp.osv import osv,fields
from openerp import tools, api
import pdb

#odootask.task
class Task(osv.osv):
    _inherit = "mail.thread"
    _name = "odootask.task"

    @api.multi
    def _get_image(self, name, args):
        return dict((p.id, tools.image_get_resized_images(p.image)) for p in self)

    @api.one
    def _set_image(self, name, value, args):
        return self.write({'image': tools.image_resize_image_big(value)})

    @api.multi
    def _has_image(self, name, args):
        return dict((p.id, bool(p.image)) for p in self)

    def write(self,cr,uid,ids,vals,context=None):
        context = context or {}
        if vals.has_key("id"):
            ids = [vals["id"]]
        res = super(Task, self).write(cr,uid,ids,vals,context=context)
        return res

    _columns = {

        'number':fields.char('Number'),
        'category_id':fields.many2one('odootask.task_category'),
        'amount':fields.float(),
        'unit':fields.many2one("odootask.unit"),
        'donator_id':fields.many2one("res.partner"),
        'donate_time':fields.datetime("Donate Time"),
        'donee_id':fields.many2one('odootask.donatee'),
        'donee_type':fields.many2one('odootask.donee_type'),
        'remark':fields.char('Remark'),
        'track':fields.one2many('odootask.track','number'),

        'state':fields.selection(
            [("confirmed", "等待入库"),("approved","确认收入"), ("done", "完成发放"), ("draft", "取消收入")], default="confirmed"),

        # image: all image fields are base64 encoded and PIL-supported
        'image': fields.binary("Image",
            help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={
                'odootask.task': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized image of this contact. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'odootask.task': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized image of this contact. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),
        'has_image': fields.function(_has_image, type="boolean"),

        'image_path':fields.char("图片地址"),
        "image_url":fields.char("图片查询url"),
    }

# 志愿者
class GoodPartner(osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"

    def write(self,cr,uid,ids,vals,context=None):
        context = context or {}
        if vals.has_key("id"):
            ids = [vals["id"]]
        res = super(GoodPartner, self).write(cr,uid,ids,vals,context=context)
        return res

    _columns = {
        'number':fields.char("编号"),
        'partner_type':fields.selection([("donator", "志愿者"),("donatee","受赠人")]),
        'cardid':fields.char("身份证"),
        'goods':fields.one2many("odootask.task","donator_id"),
        'donatee_goods':fields.one2many("odootask.task","donee_id"),
    }

class Donatee(osv.osv):
    _name = "odootask.donatee"

    _columns = {
        'name':fields.char('名称'),
        'phone':fields.char('手机号'),
        'partner_type': fields.selection([("donator", "志愿者"), ("donatee", "受赠人")]),
        'cardid': fields.char("身份证"),
        'donatee_goods': fields.one2many("odootask.task", "donee_id"),
    }

# odootask.task_category
class TaskCategory(osv.osv):
    _name = "odootask.task_category"

    @api.multi
    def _get_image(self, name, args):
        return dict((p.id, tools.image_get_resized_images(p.image)) for p in self)

    @api.one
    def _set_image(self, name, value, args):
        return self.write({'image': tools.image_resize_image_big(value)})

    @api.multi
    def _has_image(self, name, args):
        return dict((p.id, bool(p.image)) for p in self)

    _columns = {
        'name':fields.char('名称'),
        'unit':fields.many2one('odootask.unit',"计量单位"),
        'task_ids':fields.one2many('odootask.task','category_id'),

        # image: all image fields are base64 encoded and PIL-supported
        'image': fields.binary("Image",
            help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={
                'odootask.task_category': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized image of this contact. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'odootask.task_category': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized image of this contact. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),
        'has_image': fields.function(_has_image, type="boolean"),
    }

# odootask.task_comment
class Comment(osv.osv):
    _name = "odootask.task_comment"

    _columns = {
        'content':fields.char('Content'),
        'task_id':fields.many2one('odootask.task'),
    }

class DoneeType(osv.osv):
    _name = "odootask.donee_type"

    _columns = {
        'name':fields.char('名称'),
    }

class Unit(osv.osv):
    _name = "odootask.unit"

    _columns = {
        'name':fields.char('名称'),
    }

class Community(osv.osv):
    _name = "odootask.community"

    _columns = {
        'name':fields.char('名称'),
        'number':fields.char('编号'),
    }

class Track(osv.osv):
    _name = "odootask.track"

    @api.multi
    def _get_image(self, name, args):
        return dict((p.id, tools.image_get_resized_images(p.image)) for p in self)

    @api.one
    def _set_image(self, name, value, args):
        return self.write({'image': tools.image_resize_image_big(value)})

    @api.multi
    def _has_image(self, name, args):
        return dict((p.id, bool(p.image)) for p in self)


    _columns = {
        'number':fields.many2one('odootask.task'),
        'type':fields.many2one('odootask.track_type'),
        'time':fields.datetime('Time'),
        
        # image: all image fields are base64 encoded and PIL-supported
        'image': fields.binary("Image",
            help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={
                'odootask.track': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized image of this contact. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'odootask.track': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized image of this contact. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),
        'has_image': fields.function(_has_image, type="boolean"),
    }

class TrackType(osv.osv):
    _name = "odootask.track_type"

    _columns = {
        'name':fields.char('名称'),
        'desc':fields.text('Desc'),
    }
