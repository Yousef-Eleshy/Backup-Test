# -*- coding: utf-8 -*-
# from odoo import http


# class CashTransactionsReport(http.Controller):
#     @http.route('/cash_transactions_report/cash_transactions_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cash_transactions_report/cash_transactions_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cash_transactions_report.listing', {
#             'root': '/cash_transactions_report/cash_transactions_report',
#             'objects': http.request.env['cash_transactions_report.cash_transactions_report'].search([]),
#         })

#     @http.route('/cash_transactions_report/cash_transactions_report/objects/<model("cash_transactions_report.cash_transactions_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cash_transactions_report.object', {
#             'object': obj
#         })
