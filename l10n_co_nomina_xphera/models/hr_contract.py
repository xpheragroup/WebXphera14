from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

class HrContract(models.Model):
    _inherit = 'hr.contract'

    auxilio_transporte = fields.Boolean(string='Auxilio de Transporte', help='La empresa da a sus empleados auxilio de transporte. Es una casilla que habilita la posibilidad debido a que no es una obligación.')
    auxilio_conectividad = fields.Boolean(string='Auxilio de Conectividad', help='La empresa da a sus empleados auxilio de conectividad. Es una casilla que habilita la posibilidad debido a que no es una obligación.')
    
    @api.onchange('auxilio_transporte')
    def just_auxilio_transporte(self):
        if self.auxilio_transporte:
            self.auxilio_conectividad = False

    @api.onchange('auxilio_conectividad')
    def just_auxilio_conectividad(self):
        if self.auxilio_conectividad:
            self.auxilio_transporte = False