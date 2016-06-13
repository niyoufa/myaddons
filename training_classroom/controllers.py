# -*- coding: utf-8 -*-
from openerp import http

# class TrainingClassroom(http.Controller):
#     @http.route('/training_classroom/training_classroom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/training_classroom/training_classroom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('training_classroom.listing', {
#             'root': '/training_classroom/training_classroom',
#             'objects': http.request.env['training_classroom.training_classroom'].search([]),
#         })

#     @http.route('/training_classroom/training_classroom/objects/<model("training_classroom.training_classroom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('training_classroom.object', {
#             'object': obj
#         })