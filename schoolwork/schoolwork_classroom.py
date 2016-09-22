#coding=utf=8

#  classroom
import pdb
from openerp.osv import osv,fields

class classroom(osv.osv):
    _name = "schoolwork.classroom"
    _description = "classroom"

    _columns = {
        "name" : fields.char("classroom",required=True),
        "number" : fields.char("classroom no"),
        "school_id" : fields.many2one("res.company","school"),
        "teacher":fields.one2many("res.users","classroom_id","teacher"),
        "sc_course_schedule" : fields.one2many("schoolwork.course.schedule","classroom_id","course schedule"),
        "state":fields.boolean("state"),
    }

    _defaults = {
        "state":False,
    }

class course_schedule(osv.osv):
    _name = "schoolwork.course.schedule"
    _description = "course schedule"

    _columns = {
        "name" : fields.char("course schedule"),
        "classroom_id" : fields.many2one("schoolwork.classroom","classroom"),
        "schedule_line" : fields.one2many("schoolwork.course.schedule.line","course_schedule_id","course schedule line"),
    }

class course_schedule_line(osv.osv):
    _name = "schoolwork.course.schedule.line"
    _description = "course schedule line"

    _columns = {
        "name" : fields.char("course schedule line"),
        "course_schedule_id" : fields.many2one("schoolwork.course.schedule","course schedule"),
        "lesson_id" : fields.many2one("schoolwork.lession","lession"),
    }

class lesson(osv.osv):
    _name = "schoolwork.lesson"
    _description = u"教学课"
    _columns = {
        "name":fields.char(u"名称"),
        "lesson_type":fields.selection(( (1,u"正常"), (10,u"习题课"), (20,u"自习课"), (30,u"实验课"), (40,u"自习课") ),u"类型"),
        "course_type_id":fields.many2one("schoolwork.course.type","类型"),
    }

    def query_current_lesson(self,*args,**kwargs):
        pass

class course_type(osv.osv):
    _name = "schoolwork.course.type"
    _description = u"教育部颁布的课程类型"
    _columns = {
        "number":fields.char(u'编号'),
        "name":fields.char(u"课程名称"),
    }
