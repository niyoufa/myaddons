#coding=utf-8
from openerp import models, fields, api, _


# odootask.task
class Task(models.Model):
    _inherit = "mail.thread"
    _name = "odootask.task"
    
    name = fields.Char()
    close_date = fields.Date()
    description = fields.Text()
    applier_ids = fields.Many2many("res.users")
    comment_ids = fields.One2many("odootask.task_comment", "task_id")
    state = fields.Selection(
        [("confirmed", "等待入库"),("approved","确认收入"), ("done", "完成发放"), ("draft", "取消收入")], default="confirmed")

    number = fields.Char()
    category_id = fields.Many2one("odootask.task_category")
    amount = fields.Float()
    unit = fields.Many2one("odootask.unit")
    doantor_id = fields.Many2one("res.partner")
    donate_time = fields.Date()
    donee_id = fields.Many2one("res.partner")
    donee_type = fields.Many2one("odootask.donee_type")
    remark = fields.Char(size=1000)
    track = fields.One2many("odootask.track","number")

# odootask.task_category
class TaskCategory(models.Model):
    _name = "odootask.task_category"

    name = fields.Char()
    task_ids = fields.One2many("odootask.task", "category_id")


# odootask.task_comment
class Comment(models.Model):
    _name = "odootask.task_comment"
    content = fields.Char(size=1000)
    task_id = fields.Many2one("odootask.task")


class User(models.Model):
    _inherit = "res.users"

    odootask_ids = fields.One2many("odootask.task", "create_uid")

class DoneeType(models.Model):
    _name = "odootask.donee_type"

    name = fields.Char(size=255)

class Unit(models.Model):
    _name = "odootask.unit"

    name = fields.Char(size=10)

class Track(models.Model):
    _name = "odootask.track"
    
    number = fields.Many2one("odootask.task")
    type = fields.Many2one("odootask.track_type")
    time = fields.Date()

class TrackType(models.Model):
    _name = "odootask.track_type"

    name = fields.Char(size=255)
    desc = fields.Text()
