# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    primer_nombre = fields.Char(string='Primer Nombre')
    segundo_nombre = fields.Char(string='Segundo Nombre')
    primer_apellido = fields.Char(string='Primer Apellido')
    segundo_apellido = fields.Char(string='Segundo Apellido')