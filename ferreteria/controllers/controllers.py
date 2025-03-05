# -*- coding: utf-8 -*-
# from odoo import http


# class Ferreteria(http.Controller):
#     @http.route('/ferreteria/ferreteria', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ferreteria/ferreteria/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ferreteria.listing', {
#             'root': '/ferreteria/ferreteria',
#             'objects': http.request.env['ferreteria.ferreteria'].search([]),
#         })

#     @http.route('/ferreteria/ferreteria/objects/<model("ferreteria.ferreteria"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ferreteria.object', {
#             'object': obj
#         })

