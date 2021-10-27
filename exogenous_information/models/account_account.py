# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class AccountAccount(models.Model):
    _inherit = 'account.account'

    concepto = fields.Integer(string='Concepto', help='Es el número de concepto de la cuenta ante la DIAN.')
