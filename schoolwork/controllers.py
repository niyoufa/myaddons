# -*- coding: utf-8 -*-
from openerp import http

# class Schoolwork(http.Controller):
#     @http.route('/schoolwork/schoolwork/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/schoolwork/schoolwork/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('schoolwork.listing', {
#             'root': '/schoolwork/schoolwork',
#             'objects': http.request.env['schoolwork.schoolwork'].search([]),
#         })

#     @http.route('/schoolwork/schoolwork/objects/<model("schoolwork.schoolwork"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('schoolwork.object', {
#             'object': obj
#         })