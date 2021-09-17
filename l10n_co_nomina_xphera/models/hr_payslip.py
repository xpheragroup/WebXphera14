from datetime import date, datetime, timedelta
from odoo import api, fields, models, _

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    prima = fields.Boolean(string='Pago de Prima')

    @api.onchange('date_from','date_to')
    def es_prima(self):
        year = datetime.now().year

        primera_prima = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','DPP')],limit=1).parameter_value
        date_primera_prima = datetime.strptime(primera_prima + '/' + str(year), '%d/%m/%Y').date()
        segunda_prima = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','DSP')],limit=1).parameter_value
        date_segunda_prima = datetime.strptime(segunda_prima + '/' + str(year), '%d/%m/%Y').date()

        if (self.date_from <= date_primera_prima <= self.date_to) or (self.date_from <= date_segunda_prima <= self.date_to):
            self.prima = True
        else:
            self.prima = False
    
        for line_worked_days in self.worked_days_line_ids:
            line_worked_days.numero_horas_diurnas_ordinarias = self.compute_horas(line_worked_days.work_entry_type_id, self.date_from, self.date_to, 'HDO')
            line_worked_days.numero_horas_nocturnas_ordinarias = self.compute_horas(line_worked_days.work_entry_type_id, self.date_from, self.date_to, 'HNO')
            line_worked_days.numero_horas_diurnas_festivas = self.compute_horas(line_worked_days.work_entry_type_id, self.date_from, self.date_to, 'HDF')
            line_worked_days.numero_horas_nocturnas_festivas = self.compute_horas(line_worked_days.work_entry_type_id, self.date_from, self.date_to, 'HNF')
            line_worked_days.numero_horas_extras_ordinarias_diurnas = self.compute_horas(line_worked_days.work_entry_type_id, self.date_from, self.date_to, 'HEDO')
            line_worked_days.numero_horas_extras_ordinarias_nocturnas = self.compute_horas(line_worked_days.work_entry_type_id, self.date_from, self.date_to, 'HENO')
            line_worked_days.numero_horas_extras_festivas_diurnas = self.compute_horas(line_worked_days.work_entry_type_id, self.date_from, self.date_to, 'HEDF')
            line_worked_days.numero_horas_extras_festivas_nocturnas = self.compute_horas(line_worked_days.work_entry_type_id, self.date_from, self.date_to, 'HENF')
    
    def compute_horas(self, tipo, inicio, fin, tipo_hora):
        HDO
        HNO
        HDF
        HNF
        HEDO
        HENO
        HEDF
        HENF

        for work_entry in self.env['hr.work.entry'].search([('work_entry_type_id','=',tipo.id),('date_start','>=',inicio),('date_stop','>=',fin)]):
