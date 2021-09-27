from datetime import date, datetime, timedelta
from odoo import api, fields, models, _

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    prima = fields.Boolean(string='Pago de Prima')
    cesantias = fields.Boolean(string='Pago de Cesantias')

    total_extras_recargos_hours = fields.One2many('hr.payslip.total_hours', 'name', string='Total Extras y Recargos', copy=False)

    @api.onchange('date_from','date_to')
    def prima_cesantias(self):
        year = datetime.now().year

        primera_prima = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','DPP')],limit=1).parameter_value
        date_primera_prima = datetime.strptime(primera_prima + '/' + str(year), '%d/%m/%Y').date()
        segunda_prima = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','DSP')],limit=1).parameter_value
        date_segunda_prima = datetime.strptime(segunda_prima + '/' + str(year), '%d/%m/%Y').date()

        if (self.date_from <= date_primera_prima <= self.date_to) or (self.date_from <= date_segunda_prima <= self.date_to):
            self.prima = True
        else:
            self.prima = False

        fecha_cesantias = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FCE')],limit=1).parameter_value
        date_cesantias = datetime.strptime(fecha_cesantias + '/' + str(year), '%d/%m/%Y').date()

        if (self.date_from <= date_cesantias <= self.date_to):
            self.cesantias = True
        else:
            self.cesantias = False
    
    @api.onchange('worked_days_line_ids','date_from','date_to')
    def get_hours(self):
        for line_worked_days in self.worked_days_line_ids:
            tipo_entrada = line_worked_days.work_entry_type_id
            line_worked_days.numero_horas_diurnas_ordinarias = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HDO')
            line_worked_days.numero_horas_nocturnas_ordinarias = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HNO')
            line_worked_days.numero_horas_diurnas_festivas = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HDF')
            line_worked_days.numero_horas_nocturnas_festivas = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HNF')
            line_worked_days.numero_horas_extras_ordinarias_diurnas = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HEDO')
            line_worked_days.numero_horas_extras_ordinarias_nocturnas = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HENO')
            line_worked_days.numero_horas_extras_festivas_diurnas = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HEDF')
            line_worked_days.numero_horas_extras_festivas_nocturnas = self.compute_horas(tipo_entrada, self.date_from, self.date_to, 'HENF')

    def compute_horas(self, tipo, inicio, fin, tipo_hora):

        HDO_number = 0
        HNO_number = 0
        HDF_number = 0
        HNF_number = 0
        HEDO_number = 0
        HENO_number = 0
        HEDF_number = 0
        HENF_number = 0

        entries = self.env['hr.work.entry'].search([('work_entry_type_id','=',tipo.id)])

        for work_entry in entries:
            work_entry_id = self.env['hr.work.entry'].search([('id','=',work_entry.id)])
            
            if work_entry_id.date_start:
                fecha_real_inicio = (work_entry_id.date_start - timedelta(hours=5)).date()
            else:
                fecha_real_inicio = datetime.today().date()

            if work_entry_id.date_stop:
                fecha_real_fin = (work_entry_id.date_stop - timedelta(hours=5)).date()
            else:
                fecha_real_fin = datetime.today().date()

            if (fecha_real_inicio >= inicio) and (fecha_real_fin <= fin):
                if tipo_hora == 'HDO':
                    HDO_number += work_entry_id.horas_diurnas_ordinarias
                if tipo_hora == 'HNO':
                    HNO_number += work_entry_id.horas_nocturnas_ordinarias
                if work_entry_id.pay_festivos:
                    if tipo_hora == 'HDF':
                        HDF_number += work_entry_id.horas_diurnas_festivas
                    if tipo_hora == 'HNF':
                        HNF_number += work_entry_id.horas_nocturnas_festivas
                if tipo_hora == 'HEDO':
                    HEDO_number += work_entry_id.horas_extras_ordinarias_diurnas
                if tipo_hora == 'HENO':
                    HENO_number += work_entry_id.horas_extras_ordinarias_nocturnas
                if work_entry_id.pay_festivos:
                    if tipo_hora == 'HEDF':
                        HEDF_number += work_entry_id.horas_extras_festivas_diurnas
                    if tipo_hora == 'HENF':
                        HENF_number += work_entry_id.horas_extras_festivas_nocturnas
                
        horas = HDO_number + HNO_number + HDF_number + HNF_number + HEDO_number + HENO_number + HEDF_number + HENF_number

        return horas
    
    @api.onchange('worked_days_line_ids')
    def get_total_hours(self):

        self.total_extras_recargos_hours = self.total_extras_recargos_hours.new()
        
        if self.name:
            self.total_extras_recargos_hours.name = str(self.id) + ' Extras y Recargos ' + self.name
        else:
            self.total_extras_recargos_hours.name = str(self.id) + ' Extras y Recargos '

        self.total_extras_recargos_hours.total_numero_horas_diurnas_ordinarias = 0
        self.total_extras_recargos_hours.total_numero_horas_nocturnas_ordinarias = 0
        self.total_extras_recargos_hours.total_numero_horas_diurnas_festivas = 0
        self.total_extras_recargos_hours.total_numero_horas_nocturnas_festivas = 0
        self.total_extras_recargos_hours.total_numero_horas_extras_ordinarias_diurnas = 0
        self.total_extras_recargos_hours.total_numero_horas_extras_ordinarias_nocturnas = 0
        self.total_extras_recargos_hours.total_numero_horas_extras_festivas_diurnas = 0
        self.total_extras_recargos_hours.total_numero_horas_extras_festivas_nocturnas = 0

        for line_worked_days in self.worked_days_line_ids:
            for line_total_houres in self.total_extras_recargos_hours:
                line_total_houres.total_numero_horas_diurnas_ordinarias += line_worked_days.numero_horas_diurnas_ordinarias
                line_total_houres.total_numero_horas_nocturnas_ordinarias += line_worked_days.numero_horas_nocturnas_ordinarias
                line_total_houres.total_numero_horas_diurnas_festivas += line_worked_days.numero_horas_diurnas_festivas
                line_total_houres.total_numero_horas_nocturnas_festivas += line_worked_days.numero_horas_nocturnas_festivas
                line_total_houres.total_numero_horas_extras_ordinarias_diurnas += line_worked_days.numero_horas_extras_ordinarias_diurnas
                line_total_houres.total_numero_horas_extras_ordinarias_nocturnas += line_worked_days.numero_horas_extras_ordinarias_nocturnas
                line_total_houres.total_numero_horas_extras_festivas_diurnas += line_worked_days.numero_horas_extras_festivas_diurnas
                line_total_houres.total_numero_horas_extras_festivas_nocturnas += line_worked_days.numero_horas_extras_festivas_nocturnas

    def compute_sheet(self):     
        res = super(HrPayslip, self).compute_sheet()
        if True:
            print("")
            print("ENTRA")
            print("")
        return res

class TotalHoursPayslip(models.Model):
    _name = 'hr.payslip.total_hours'

    name = fields.Char()
    total_numero_horas_diurnas_ordinarias = fields.Float(string='Total Horas Diurnas Ordinales')
    total_numero_horas_nocturnas_ordinarias = fields.Float(string='Total Horas Nocuturna Ordinales')
    total_numero_horas_diurnas_festivas = fields.Float(string='Total Horas Diurnas Festivas')
    total_numero_horas_nocturnas_festivas = fields.Float(string='Total Horas Nocuturna Festivas')
    total_numero_horas_extras_ordinarias_diurnas = fields.Float(string='Total Horas Extra Ordinarias Diurnas')
    total_numero_horas_extras_ordinarias_nocturnas = fields.Float(string='Total Horas Extra Ordinarias Nocturnas')
    total_numero_horas_extras_festivas_diurnas = fields.Float(string='Total Horas Extra Diurnas Festivas')
    total_numero_horas_extras_festivas_nocturnas = fields.Float(string='Total Horas Extra Nocturnas Festivas')