# -*- coding: utf-8 -*-
from openerp import http

# class ExerciseBook(http.Controller):
#     @http.route('/exercise_book/exercise_book/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exercise_book/exercise_book/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('exercise_book.listing', {
#             'root': '/exercise_book/exercise_book',
#             'objects': http.request.env['exercise_book.exercise_book'].search([]),
#         })

#     @http.route('/exercise_book/exercise_book/objects/<model("exercise_book.exercise_book"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exercise_book.object', {
#             'object': obj
#         })