# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class HrExpense(models.Model):

    _inherit = "hr.expense"

    partner_id = fields.Many2one('res.partner', string='Proveedor', required='True')

    def action_move_create(self):
        '''
        main function that is called when trying to create the accounting entries related to an expense
        '''
        move_group_by_sheet = self._get_account_move_by_sheet()

        move_line_values_by_expense = self._get_account_move_line_values()

        for expense in self:
            # get the account move of the related sheet
            move = move_group_by_sheet[expense.sheet_id.id]

            # get move line values
            move_line_values = move_line_values_by_expense.get(expense.id)

            # cambia el tercero del asiento contable en el caso que se requiera
            for line in move_line_values:
                account_product = self.env['hr.expense'].search([('id','=',line['expense_id'])])
                account_tax = self.env['account.tax'].search([('invoice_repartition_line_ids.account_id','=',line['account_id'])])
                account_tax_rec = self.env['account.tax'].search([('refund_repartition_line_ids.account_id','=',line['account_id'])])
                
                if account_tax or account_tax_rec or (account_product.product_id.property_account_expense_id.id == line['account_id']):
                    line['partner_id'] = self.partner_id.id

            # link move lines to move, and move to expense sheet
            move.write({'line_ids': [(0, 0, line) for line in move_line_values]})
            expense.sheet_id.write({'account_move_id': move.id})

            if expense.payment_mode == 'company_account':
                expense.sheet_id.paid_expense_sheets()

        # post the moves
        for move in move_group_by_sheet.values():
            move._post()

        return move_group_by_sheet
