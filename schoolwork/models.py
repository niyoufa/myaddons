# -*- coding: utf-8 -*-

# 基于中学教学的表结构

from openerp.osv import osv,fields

class teacher(osv.osv):
    _name = "res.users"
    _inherit = "res.users"
    _description = u"老师"
    _columns = {
        "number":fields.char(u"工号",readonly=True),
    }

class student(osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"
    _description = u"学生"
    _columns = {
        "number":fields.char(u"学号",readonly=True),
        'classsroom':fields.many2one('classroom',string=u'班级'),
    }

class classroom(osv.osv):
    _name = "classroom"
    _discription = u'班级'
    _columns = {
        'number': fields.char(u'班级编号'),
        'name':fields.char(u"名称"),
        'nb_student': fields.integer(u'学生人数', select=True),
        'location': fields.char(u'地点描述', size=125, select=True),
        'teachers':fields.many2many('res.users',string=u'值班老师'),
        'students':fields.one2many('res.partner','classsroom',string=u'班级学生'),
    }

class workbook(osv.osv):
    _name = "workbook"
    _description = u"作业本"
    _columns = {
        "name":fields.char(u"名称"),
        "student":fields.many2one("res.users",string=u"学生"),
        "course_type":fields.many2one("course.type",string=u"类型"),
        "schoolworks":fields.one2many("schoolwork","workbook",string=u"作业"),
    }

class schoolwork(osv.osv):
    _name = "schoolwork"
    _description = "作业"
    _columns = {
        "number":fields.char(u"作业编号"),
        "name":fields.char(u"作业名称"),
        "description":fields.char(u"作业描述"),
        "work_type":fields.selection((
                (1,"预习作业"),
                (10,"课堂作业"),
                (20,"课后作业"),
                (30,"短假作业"),
                (40,"长假作业"),
            ),u"作业类型"),
        "deadline":fields.char(u"截止日期"),

        # 作业表与其他表的关系
        "workbook":fields.many2one("workbook",string=u"作业本"),
        "teacher":fields.many2one("res.users",string=u"老师"),
        "student":fields.many2one("res.partner",string=u"学生"),
        "classroom":fields.many2one("classroom",string=u"教室"),
        "lesson":fields.many2many("lesson",string=u"课"),
        # "work_exercises":fields.one2many("work.exercises","schoolwork",string="作业题"),
        "questions":fields.one2many("question","schoolwork",string=u"问题"),
        "comment":fields.one2many("comment","schoolwork",string=u"评论"),
    }

class lesson(osv.osv):
    _name = "lesson"
    _description = u"教学课"
    _columns = {
        "name":fields.char(u"名称"),
        "description":fields.char(u"描述"),
        "lesson_type":fields.selection(( (1,u"教学"), (10,u"习题课"), (20,u"自习课"), (30,u"实验课"), (40,u"自习课") ),u"类型"),
        "start_time":fields.char(u"上课时间"),
        "end_time":fields.char(u"下课时间"),
    }

class question(osv.osv):
    _name = "question"
    _description = u"问题"
    _columns= {
        "user_id":fields.many2many("res.users",string=u"提问者"),
        "name":fields.char(u"问题名称"),
        "description":fields.char(u"问题详细描述"),
        "lesson":fields.many2one("lesson",u"相关教学课"),
        "course_course_point":fields.many2many("course.course.point",string=u"相关知识点"),
        # "attachment":fields.binary(u"相关附件"),
        "schoolwork":fields.many2one("schoolwork",string=u"作业"),
    }

class comment(osv.osv):
    _name = "comment"
    _description = u"评论"
    _columns = {
        "creator":fields.many2one("res.users",string=u"创建者"),
        "type":fields.selection((
            (20,u"学生"),
            (30,u"老师"),
            (40,u"班级"),
            (50,u"课程"),
            (51,u"课程要求"),
            (51,u"课程知识点"),
            (60,u"课"),
            (70,u"问题"),
            (80,u"作业"),
            (81,u"作业本"),
            (82,u"作业题"),
            (83,u"作业解答"),
            ),u"类型"),
        "schoolwork":fields.many2one("schoolwork",string=u"作业"),
    }

class course_course_requirement(osv.osv):
    _name = "course.course.requirement"
    _description = u"课程要求"
    _columns = {
        "number":fields.char(u"编号"),
        "description":fields.char(u"描述"),
        "course_type":fields.many2one("course.type",string=u"课程类型"),
    }

class course_course_point(osv.osv):
    _name = "course.course.point"
    _description = u"课程知识点"

    _columns = {
        "number":fields.char(u"编号"),
        "description":fields.char(u"描述"),
        "course_type":fields.many2one("course.type",string=u"课程类型"),
    }

class course_type(osv.osv):
    _name = "course.type"
    _description = u"教育部颁布的课程类型"
    _columns = {
        "number":fields.char(u'编号'),
        "name":fields.char(u"课程名称"),
        "course_requirements":fields.one2many("course.course.requirement","course_type",string=u"课程要求"),
        "course_points":fields.one2many("course.course.point","course_type",string=u"课程考点"),
    }

class course(osv.osv):
    _name = "course"
    _columns = {
        'number':fields.char(u'课程编号'),
        'name': fields.char(u'课程名'),
        'lesson_period':fields.integer(u'课时'),
        'course_type':fields.many2one('course.type',string=u'课程类型'),
        'teachers': fields.many2many('res.users', string=u'授课老师'),
        'students': fields.many2many('res.partner', string=u'学生'),
    }

class work_exercises(osv.osv):
    _name = "work.exercises"
    _description = u"作业题"
    _columns = {
        "title":fields.char(u"标题"),
        "description":fields.char(u"描述"),
        "work_exercises_type":fields.many2one("work.exercises.type",string=u"类型"),
        "course_course_point":fields.many2many("course.course.point",string=u"相关知识点"),
        "work_exercises_solutions":fields.one2many("work.exercises.solution","work_exercises",string=u"答案"),
    }

class work_exercises_type(osv.osv):
    _name = "work.exercises.type"
    _description = u"题目类型"
    _columns = {
        "number":fields.char(u"编号"),
        "name":fields.char(u"名称"),
        "description":fields.char(u"描述"),
    }

class work_exercises_solution(osv.osv):
    _name = "work.exercises.solution"
    _description = u"答案"
    _columns = {
        "user" :fields.many2one("res.users",string=u"学生"),
        "work_exercises":fields.many2one("work.exercises",string=u"题目"),
        "description":fields.char(u"答题结果描述"),
        # "attachment":fields.binary(u"相关附件"),
        "state":fields.selection((
                (1,u"未批改"), 
                (10,u"批改中"),
                (20,u"正确"),
                (30,u"通过"),
                (40,u"未通过"),
                (40,u"错误"),
            ),
            u"状态"),
    }
