# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

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

    @api.constrains('vat', 'country_id')
    def check_vat(self):
        """
        Valida si el nit es correcto.
        """
        if self.vat:
            nit = self.vat.replace('-','')
            nit = nit.strip()

            if self.l10n_latam_identification_type_id.name == 'NIT':
                if (len(nit) < 9) or (len(nit) > 10):    
                    raise UserError(_("El NIT debe tener 9 dígitos sin incluir el dígito de verificación o 10 dígitos incluyendo el digito de verificación."))
                
                if len(nit) == 9:
                    mult = [41,37,29,23,19,17,13,7,3] # multiplicadores
                    v = sum(list(map(lambda x,y: x*y, mult,[int(c) for c in nit])))
                    v = int(v) % 11       
                    if (v >= 2):
                        v = 11 - v
                    self.vat = nit + "-" + str(v)
                
                if len(nit) == 10:
                    mult = [41,37,29,23,19,17,13,7,3] # multiplicadores
                    v = sum(list(map(lambda x,y: x*y, mult,[int(c) for c in nit[:-1]])))
                    v = int(v) % 11      
                    if (v >= 2):
                        v = 11 - v
                    if str(v) != nit[9]:
                        raise UserError(_("El dígito de verificación es incorrecto."))

        res = super(Partner, self).check_vat()
        return res

    @api.onchange('vat','l10n_latam_identification_type_id')
    def _compute_DV(self):
        self.check_vat()
        if self.vat:
            if len(self.vat) == 11:
                self.DV = float(self.vat[10])
        else:
            self.DV = 0
            
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