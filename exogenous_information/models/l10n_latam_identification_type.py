from odoo import models, fields, api
from odoo.osv import expression


class L10nLatamIdentificationType(models.Model):
    _inherit = 'l10n_latam.identification.type'
    
    code = fields.Integer(string='Código Tipo de Documento')