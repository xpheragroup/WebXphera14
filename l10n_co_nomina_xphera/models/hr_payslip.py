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
    
    @api.onchange('worked_days_line_ids','date_from','date_to')
    def get_hours(self):
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

        HDO_number = 0
        HNO_number = 0
        HDF_number = 0
        HNF_number = 0
        HEDO_number = 0
        HENO_number = 0
        HEDF_number = 0
        HENF_number = 0

        for work_entry in self.env['hr.work.entry'].search([('work_entry_type_id','=',tipo.id),('date_start','>=',inicio),('date_stop','>=',fin)]):
            if tipo_hora == 'HDO':
                HDO_number += work_entry.horas_diurnas_ordinarias
            if tipo_hora == 'HNO':
                HNO_number += work_entry.horas_nocturnas_ordinarias
            if tipo_hora == 'HDF':
                HDF_number += work_entry.horas_diurnas_festivas
            if tipo_hora == 'HNF':
                HNF_number += work_entry.horas_nocturnas_festivas
            if tipo_hora == 'HEDO':
                HEDO_number += work_entry.horas_extras_ordinarias_diurnas
            if tipo_hora == 'HENO':
                HENO_number += work_entry.horas_extras_ordinarias_nocturnas
            if tipo_hora == 'HEDF':
                HEDF_number += work_entry.horas_extras_festivas_diurnas
            if tipo_hora == 'HENF':
                HENF_number += work_entry.horas_extras_festivas_nocturnas
        
        horas = HDO_number + HNO_number + HDF_number + HNF_number + HEDO_number + HENO_number + HEDF_number + HENF_number

        return horas