# -*- coding: utf-8 -*-
from odoo import http

# class LateOrder(http.Controller):
#     @http.route('/late_order/late_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/late_order/late_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('late_order.listing', {
#             'root': '/late_order/late_order',
#             'objects': http.request.env['late_order.late_order'].search([]),
#         })

#     @http.route('/late_order/late_order/objects/<model("late_order.late_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('late_order.object', {
#             'object': obj
#         })