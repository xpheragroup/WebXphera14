from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

class HrContract(models.Model):
    _inherit = 'hr.contract'

    auxilio_transporte = fields.Boolean(string='Auxilio de Transporte', help='La empresa da a sus empleados auxilio de transporte. Es una casilla que habilita la posibilidad debido a que no es una obligación.')
    auxilio_conectividad = fields.Boolean(string='Auxilio de Conectividad', help='La empresa da a sus empleados auxilio de conectividad. Es una casilla que habilita la posibilidad debido a que no es una obligación.')
    
    prima_1 = fields.Float(string='Primas Enero')
    prima_2 = fields.Float(string='Primas Febrero')
    prima_3 = fields.Float(string='Primas Marzo')
    prima_4 = fields.Float(string='Primas Abril')
    prima_5 = fields.Float(string='Primas Mayo')
    prima_6 = fields.Float(string='Primas Junio')
    prima_7 = fields.Float(string='Primas Julio')
    prima_8 = fields.Float(string='Primas Agosto')
    prima_9 = fields.Float(string='Primas Septiembre')
    prima_10 = fields.Float(string='Primas Octubre')
    prima_11 = fields.Float(string='Primas Noviembre')
    prima_12 = fields.Float(string='Primas Diciembre')

    cesantias_1 = fields.Float(string='Cesantias Enero')
    cesantias_2 = fields.Float(string='Cesantias Febrero')
    cesantias_3 = fields.Float(string='Cesantias Marzo')
    cesantias_4 = fields.Float(string='Cesantias Abril')
    cesantias_5 = fields.Float(string='Cesantias Mayo')
    cesantias_6 = fields.Float(string='Cesantias Junio')
    cesantias_7 = fields.Float(string='Cesantias Julio')
    cesantias_8 = fields.Float(string='Cesantias Agosto')
    cesantias_9 = fields.Float(string='Cesantias Septiembre')
    cesantias_10 = fields.Float(string='Cesantias Octubre')
    cesantias_11 = fields.Float(string='Cesantias Noviembre')
    cesantias_12 = fields.Float(string='Cesantias Diciembre')

    intereses_cesantias_1 = fields.Float(string='Intereses Cesantias Enero')
    intereses_cesantias_2 = fields.Float(string='Intereses Cesantias Febrero')
    intereses_cesantias_3 = fields.Float(string='Intereses Cesantias Marzo')
    intereses_cesantias_4 = fields.Float(string='Intereses Cesantias Abril')
    intereses_cesantias_5 = fields.Float(string='Intereses Cesantias Mayo')
    intereses_cesantias_6 = fields.Float(string='Intereses Cesantias Junio')
    intereses_cesantias_7 = fields.Float(string='Intereses Cesantias Julio')
    intereses_cesantias_8 = fields.Float(string='Intereses Cesantias Agosto')
    intereses_cesantias_9 = fields.Float(string='Intereses Cesantias Septiembre')
    intereses_cesantias_10 = fields.Float(string='Intereses Cesantias Octubre')
    intereses_cesantias_11 = fields.Float(string='Intereses Cesantias Noviembre')
    intereses_cesantias_12 = fields.Float(string='Intereses Cesantias Diciembre')

    total_cesantias_year = fields.Float(string='Total Cesantias del Año')
    total_intereses_cesantias_year = fields.Float(string='Total Intereses Cesantias del Año')

    vacaciones_1 = fields.Float(string='Vacaciones Enero')
    vacaciones_2 = fields.Float(string='Vacaciones Febrero')
    vacaciones_3 = fields.Float(string='Vacaciones Marzo')
    vacaciones_4 = fields.Float(string='Vacaciones Abril')
    vacaciones_5 = fields.Float(string='Vacaciones Mayo')
    vacaciones_6 = fields.Float(string='Vacaciones Junio')
    vacaciones_7 = fields.Float(string='Vacaciones Julio')
    vacaciones_8 = fields.Float(string='Vacaciones Agosto')
    vacaciones_9 = fields.Float(string='Vacaciones Septiembre')
    vacaciones_10 = fields.Float(string='Vacaciones Octubre')
    vacaciones_11 = fields.Float(string='Vacaciones Noviembre')
    vacaciones_12 = fields.Float(string='Vacaciones Diciembre')

    total_vacaciones = fields.Float(string='Total Vacaciones')

    riesgo = fields.Selection([
        ('1', 'Riesgo I'),
        ('2', 'Riesgo II'),
        ('3', 'Riesgo III'),
        ('4', 'Riesgo IV'),
        ('5', 'Riesgo V')], string='Riesgo ARL')

    @api.onchange('auxilio_transporte')
    def just_auxilio_transporte(self):
        if self.auxilio_transporte:
            self.auxilio_conectividad = False

    @api.onchange('auxilio_conectividad')
    def just_auxilio_conectividad(self):
        if self.auxilio_conectividad:
            self.auxilio_transporte = False