# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models

class Partner(models.Model):
    _description = "Municipio"
    _name = "res.municipio"

    name = fields.Char('Nombre')
    code = fields.Integer('Código')

    _sql_constraints = [
        ('name_uniq', 'unique (code, name)', 'El nombre o código de municipio ya existe!')
    ]

class Partner(models.Model):
    _inherit = 'res.partner'

    municipio = fields.Many2one('res.municipio')
    DV = fields.Integer('DV', compute='_compute_DV', help='Dígito de verificación.')

    @api.onchange('vat')
    def _compute_DV(self):
        self.DV = 0
        '''if int(self.vat[len(self.vat)-1:]):
            self.DV = int(self.vat[len(self.vat)-1:])
        else:
            self.DV = 0
        if self.vat:
            if self.vat.isdigit() and len(self.vat)<16:
            vpri = [0,3,7,13,17,19,23,29,37,41,43,47,53,59,67,71]
            x = 0
            y = 0
            for i in range(0,len(self.vat)):
                y = int(self.vat[i])
                x = x + (y * vpri[len(self.vat)-i])
                y = x % 11
            dv = 11 - y if y > 1 else y'''
            
class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def _load(self, sale_tax_rate, purchase_tax_rate, company):
        res = super(AccountChartTemplate, self)._load(sale_tax_rate, purchase_tax_rate, company)

        # by default, anglo-saxon companies should have totals
        # displayed below sections in their reports
        company.totals_below_sections = True

        #set a default misc journal for the tax closure
        company.account_tax_periodicity_journal_id = company._get_default_misc_journal()

        company.account_tax_periodicity_reminder_day = 3

        # create the recurring entry
        vals = {
            'company_id': company,
            'totals_below_sections' : company.totals_below_sections,
            'account_tax_periodicity' : company.account_tax_periodicity,
            'account_tax_periodicity_reminder_day' : company.account_tax_periodicity_reminder_day,
            'account_tax_original_periodicity_reminder_day' : company.account_tax_original_periodicity_reminder_day,
            'account_tax_periodicity_journal_id' : company.account_tax_periodicity_journal_id,
            'account_tax_next_activity_type' : company.account_tax_next_activity_type,
            'account_revaluation_journal_id' : company.account_revaluation_journal_id,
            'account_revaluation_expense_provision_account_id' : company.account_revaluation_expense_provision_account_id,
            'account_revaluation_income_provision_account_id' : company.account_revaluation_income_provision_account_id,
        }
        config_settings_company = self.env['res.company'].search([('id', '=', company.id)], limit=1)
        config_settings_company._create_edit_tax_reminder(vals)

        config_settings = self.env['res.config.settings'].with_context(company=company)

        config_settings.use_anglo_saxon = True

        config_settings.group_analytic_accounting = True
        config_settings.module_account_budget = True
        config_settings.module_product_margin = True       
        config_settings.group_analytic_tags = True

        config_settings_all = self.env['res.config.settings'].search([('company_id', '=', company.id)], limit=1)
        config_settings_all.group_analytic_accounting = True
        config_settings_all.module_account_budget = True
        config_settings_all.module_product_margin = True
        config_settings_all.group_analytic_tags = True

        config_settings.account_tax_periodicity_reminder_day = 3

        company.account_tax_original_periodicity_reminder_day = company.account_tax_periodicity_reminder_day

        # Asinar automáticamente el grupo a las cuentas contables de esa compañía con grupo con prefijo de código de 6 dígitos a cuantas contables de 8 dígitos. modelo: account.account
        account_groups = self.env['account.group'].search([])
        account_accounts = self.env['account.account'].search([])

        for group in account_groups:
            for account in account_accounts:
                if len(group.code_prefix) == 4:
                    if len(account.code) == 6:
                        if group.code_prefix in account.code:
                            account.group_id = group
                if len(group.code_prefix) == 6:
                    if len(account.code) == 8:
                        if group.code_prefix in account.code:
                            account.group_id = group
                if len(group.code_prefix) == 8:
                    if len(account.code) == 10:
                        if group.code_prefix in account.code:
                            account.group_id = group

        return res