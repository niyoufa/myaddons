# -*- coding: utf-8 -*-
from openerp import http

# class Jonthon(http.Controller):
#     @http.route('/jonthon/jonthon/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jonthon/jonthon/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('jonthon.listing', {
#             'root': '/jonthon/jonthon',
#             'objects': http.request.env['jonthon.jonthon'].search([]),
#         })

#     @http.route('/jonthon/jonthon/objects/<model("jonthon.jonthon"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jonthon.object', {
#             'object': obj
#         })