# -*- coding: utf-8 -*-

# 基于中学教学

from openerp.osv import osv,fields

class school(osv.osv):
    _name = "res.company"
    _inherit = "res.company"
    _description = u"学校"

    _columns = {}

    def print_a(self,*args,**kwargs):
        print "a"
        print args

    def print_b(self,*args,**kwargs):
        print "b"
        print args

class student(osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"
    _description = u"学生"
    _columns = {
        "number":fields.char("工号"),
        'partner_type':fields.char('partner_type'),
    }

class teacher(osv.osv):
    _name = "res.users"
    _inherit = "res.users"
    _description = u"老师"
    _columns = {
        "number":fields.char("工号"),
        #"classroom_id":fields.many2one("schoolwork.classroom","classroom"),
    }

# class classroom(osv.osv):
#     _name = "classroom"
#     _discription = u'班级'
#     _columns = {
#         'number': fields.char(u'班级编号', size=64, select=True),
#         'name':fields.many2one(''),
#         'nb_student': fields.integer(u'学生人数', select=True),
#         'location': fields.char(u'地点描述', size=125, select=True),
#         'teacher':fields.many2many('teacher',u'值班老师'),
#         'student':fields.one2many('student','classsroom_id',string=u'班级学生'),
#     }

# class course(osv.osv):
#     _name = "course"
#     _columns = {
#         'number':fields.char(u'课程编号'),
#         'name': fields.char(u'课程名'),
#         'lesson_period':fields.integer(u'课时'),
#         'course_type':fields.many2one('course.type',string=u'课程类型'),
#         'teacher': fields.many2many('teacher', u'授课老师'),
#         'students': fields.many2many('student', string=u'学生'),
#     }

# class course_type(osv.osv):
#     _name = "course.type"
#     _description = u"教育部颁布的课程类型"
#     _columns = {
#         "number":fields.char(u'编号'),
#         "name":fields.char(u"课程名称"),
#         "course_requirements":fields.one2many("course.course_requirement","course_type_id",string=u"课程要求"),
#         "course_tests":fields.one2many("course.course_test","course_type_id",string=u"课程考点"),
#     }

# class course_course_require(osv.osv):
#     _name = "course.course.require"
#     _description = u"课程要求"
#     _columns = {
#         "number":fields.char(u"编号"),
#         "description":fields.char(u"描述"),
#         "course_type_id":fields.one2many("course.type",string=u"课程类型"),
#     }

# class course_course_point(osv.osv):
#     _name = "course.course.point"
#     _description = u"课程知识点"

#     _columns = {
#         "number":fields.char(u"编号"),
#         "description":fields.char(u"描述"),
#         "course_type_id":fields.one2many("course.type",string=u"课程类型"),
#     }

# class lesson(osv.osv):
#     _name = "lesson"
#     _description = u"教学课"
#     _columns = {
#         "name":fields.char(u"名称"),
#         "lesson_type":fields.selection(( (1,u"正常"), (10,u"习题课"), (20,u"自习课"), (30,u"实验课"), (40,u"自习课") ),u"类型"),
#         "course_course_point":fields.many2many("course.course.point",u"知识点"),
#     }

# class question(osv.osv):
#     _name = "question"
#     _description = u"问题"
#     _columns= {
#         "user_id":fields.many2many("res.users",u"提问者"),
#         "name":fields.char(u"问题名称"),
#         "description":fields.char(u"问题详细描述"),
#         "lesson":fields.many2one("lesson",u"相关教学课"),
#         "course_course_point":fields.many2many("course.course.point",u"相关知识点"),
#         "attachment":fields.binary(u"相关附件"),
#     }

# class workbook(osv.osv):
#     _name = "workbook"
#     _description = "作业本"
#     columns = {
#         "name":fields.char("名称"),
#         "user_id":fields.many2one("res.users",string="主人"),
#         "schoolworks":fields.many2many("schoolwork","作业集"),
#     }

# class schoolwork(osv.osv):
#     _name = "schoolwork"
#     _description = "作业"
#     _columns = {
#         "number":fields.char(u"作业编号"),
#         "name":fields.char(u"作业名称"),
#         "description":fields.char(u"作业描述"),
#         "work_type":fields.selection((
#                 (1,"预习作业"),
#                 (10,"课堂作业"),
#                 (20,"课后作业"),
#                 (30,"短假作业"),
#                 (40,"长假作业"),
#             ),"作业类型"),
#         "work_exercises":one2many("work.exercises","schoolwork_id",string="作业题"),
#         "deadline":fields.char(u"截止日期"),
#     }

# class work_exercises(osv.osv):
#     _name = "work.exercises"
#     _description = "作业题"
#     _columns = {
#         "title":fields.char(u"标题"),
#         "description":fields.char(u"描述"),
#         "work_exercises_type":fields.many2one("work.exercises.type",string="类型"),
#         "course_course_point":fields.many2many("course.course.point",u"相关知识点"),
#         "work_exercises_solutions":fields.one2many("work.exercises.solution","work_exercises_id",string="答案"),
#     }

# class work_exercises_type(osv.osv):
#     _name = "work.exercises.type"
#     _description = "题目类型"
#     columns = {
#         "number":fields.char("编号"),
#         "name":fields.char("名称"),
#         "description":fields.char("描述"),
#     }

# class work_exercises_solution(osv.osv):
#     _name = "work.exercises.solution"
#     _description = "答案"
#     columns = {
#         "user_id" :fields.many2one("res.users",string="答题者"),
#         "work_exercises_id":fields.many2one("work.exercises",string="题目"),
#         "description":fields.char("答题结果描述"),
#         "attachment":fields.binary(u"相关附件"),
#         "state":fields.selection((
#                 (1,"未批改"),
#                 (10,"批改中"),
#                 (20,"正确"),
#                 (30,"通过"),
#                 (40,"未通过"),
#                 (40,"错误"),
#             )
#             "状态"),
#     }

# class comment(osv.osv):
#     _name = "comment"
#     _description = "评论"
#     columns = {
#         "creator_id":fields.many2one("res.users","创建者"),
#         "type":fields.selection((
#             (20,"学生"),
#             (30,"老师"),
#             (40,"班级"),
#             (50,"课程"),
#             (51,"课程要求")
#             (51,"课程知识点")
#             (60,"课"),
#             (70,"问题"),
#             (80,"作业"),
#             (81,"作业本")
#             (82,"作业题"),
#             (83,"作业解答"),
#             ),"类型"),
#         "obj_id":fields.integer("评论对象id"),
#     }



