# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date, datetime, timedelta
from odoo import api, fields, models

class HrWorkEntry(models.Model):
    _inherit = 'hr.work.entry'

    pagar_festivos = fields.Boolean(string='Pagar festivos', help='Esta opción permite saber si se deben tener en cuenta las horas de en días festivos.')

    @api.depends('date_start','date_stop','employee_id')
    def _calculo_horas(self):

        year = datetime.now().year
        fecha = date(year,1,1)
        fecha += timedelta(days=6-fecha.weekday())
        domingos=[]
        while fecha.year == year:
            domingos.append(fecha)
            fecha += timedelta(days=7)
        
        fecha_real_inicio = (self.date_start - timedelta(hours=5))
        fecha_real_fin = (self.date_stop - timedelta(hours=5))

        morning = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','HM')],limit=1).parameter_value
        hour_morning = datetime.strptime(morning, '%H:%M').time().hour
        afternoon = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','HT')],limit=1).parameter_value
        hour_afternoon = datetime.strptime(afternoon, '%H:%M').time().hour

        new_year = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FAN')],limit=1).parameter_value
        reyes = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FRM')],limit=1).parameter_value
        san_jose = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FSJ')],limit=1).parameter_value
        jueves_santo = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FJS')],limit=1).parameter_value
        viernes_santo = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FVS')],limit=1).parameter_value
        work_day = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FDT')],limit=1).parameter_value
        ascension_cristo = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FAC')],limit=1).parameter_value
        corpus_christi = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FCC')],limit=1).parameter_value
        sagrado_corazon = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FSC')],limit=1).parameter_value
        sanpedro_sanpablo = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FPP')],limit=1).parameter_value
        independencia_colombia = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FDI')],limit=1).parameter_value
        batalla_boyaca = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FBB')],limit=1).parameter_value
        virgen_maria = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FVM')],limit=1).parameter_value
        raza = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FDR')],limit=1).parameter_value
        santos = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FFD')],limit=1).parameter_value
        independencia_cartagena = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FIC')],limit=1).parameter_value
        inmaculada_concepcion = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FDC')],limit=1).parameter_value
        navidad = self.env['hr.rule.parameter.value'].search([('rule_parameter_id.code','=','FDN')],limit=1).parameter_value

        date_new_year = datetime.strptime(new_year + '/' + str(year), '%d/%m/%Y').date()
        date_reyes = datetime.strptime(reyes + '/' + str(year), '%d/%m/%Y').date()
        date_san_jose = datetime.strptime(san_jose + '/' + str(year), '%d/%m/%Y').date()
        date_jueves_santo = datetime.strptime(jueves_santo + '/' + str(year), '%d/%m/%Y').date()
        date_viernes_santo = datetime.strptime(viernes_santo + '/' + str(year), '%d/%m/%Y').date()
        date_work_day = datetime.strptime(work_day + '/' + str(year), '%d/%m/%Y').date()
        date_ascension_cristo = datetime.strptime(ascension_cristo + '/' + str(year), '%d/%m/%Y').date()
        date_corpus_christi = datetime.strptime(corpus_christi + '/' + str(year), '%d/%m/%Y').date()
        date_sagrado_corazon = datetime.strptime(sagrado_corazon + '/' + str(year), '%d/%m/%Y').date()
        date_sanpedro_sanpablo = datetime.strptime(sanpedro_sanpablo + '/' + str(year), '%d/%m/%Y').date()
        date_independencia_colombia = datetime.strptime(independencia_colombia + '/' + str(year), '%d/%m/%Y').date()
        date_batalla_boyaca = datetime.strptime(batalla_boyaca + '/' + str(year), '%d/%m/%Y').date()
        date_virgen_maria = datetime.strptime(virgen_maria + '/' + str(year), '%d/%m/%Y').date()
        date_raza = datetime.strptime(raza + '/' + str(year), '%d/%m/%Y').date()
        date_santos = datetime.strptime(santos + '/' + str(year), '%d/%m/%Y').date()
        date_independencia_cartagena = datetime.strptime(independencia_cartagena + '/' + str(year), '%d/%m/%Y').date()
        date_inmaculada_concepcion = datetime.strptime(inmaculada_concepcion + '/' + str(year), '%d/%m/%Y').date()
        date_navidad = datetime.strptime(navidad + '/' + str(year), '%d/%m/%Y').date()

        festivos = [
            date_new_year,
            date_reyes,
            date_san_jose,
            date_jueves_santo,
            date_viernes_santo,
            date_work_day,
            date_ascension_cristo,
            date_corpus_christi,
            date_sagrado_corazon,
            date_sanpedro_sanpablo,
            date_independencia_colombia,
            date_batalla_boyaca,
            date_virgen_maria,
            date_raza,
            date_santos,
            date_independencia_cartagena,
            date_inmaculada_concepcion,
            date_navidad
        ]

        domingos_festivos = festivos + domingos

        self.horas_diurnas_ordinarias = 0
        self.horas_nocturnas_ordinarias = 0
        self.horas_diurnas_festivas = 0
        self.horas_nocturnas_festivas = 0
        
        self.horas_extras_ordinarias_diurnas = 0
        self.horas_extras_ordinarias_nocturnas = 0
        self.horas_extras_festivas_diurnas = 0
        self.horas_extras_festivas_nocturnas = 0

        fecha_conteo = fecha_real_inicio
        day_conteo = fecha_real_inicio.day
        mes_conteo = fecha_real_inicio.month

        hr_cero = datetime.strptime(str(day_conteo)+'/'+str(mes_conteo)+'/'+str(year)+' '+'00', '%d/%m/%Y %H')
        hr_morning = datetime.strptime(str(day_conteo)+'/'+str(mes_conteo)+'/'+str(year)+' '+str(hour_morning), '%d/%m/%Y %H')
        hr_afternoon = datetime.strptime(str(day_conteo)+'/'+str(mes_conteo)+'/'+str(year)+' '+str(hour_afternoon), '%d/%m/%Y %H')
        hr_final = datetime.strptime(str(day_conteo)+'/'+str(mes_conteo)+'/'+str(year)+' '+'23'+':'+'59'+':'+'59', '%d/%m/%Y %H:%M:%S')

        while fecha_conteo < fecha_real_fin:
            if fecha_conteo == fecha_real_inicio:
                if hr_morning < fecha_real_fin:
                    if hr_cero <= fecha_conteo < hr_morning:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (hr_morning - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, hr_morning)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_morning
                        else:
                            self.horas_nocturnas_ordinarias += (hr_morning - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, hr_morning)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_morning
                else:
                    if hr_cero <= fecha_conteo < fecha_real_fin:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (fecha_real_fin - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin
                        else:
                            self.horas_nocturnas_ordinarias += (fecha_real_fin - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin

                if hr_afternoon < fecha_real_fin:
                    if hr_morning <= fecha_conteo < hr_afternoon:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_diurnas_festivas += (hr_afternoon - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, hr_afternoon)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_afternoon
                        else:
                            self.horas_diurnas_ordinarias += (hr_afternoon - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, hr_afternoon)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_afternoon
                else:
                    if hr_morning <= fecha_conteo < fecha_real_fin:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_diurnas_festivas += (fecha_real_fin - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin
                        else:
                            self.horas_diurnas_ordinarias += (fecha_real_fin - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin

                if hr_final < fecha_real_fin:
                    if hr_afternoon <= fecha_conteo <= hr_final:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (hr_final - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, hr_final)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            hr_cero += timedelta(days=1)
                            fecha_conteo = hr_cero
                        else:
                            self.horas_nocturnas_ordinarias += (hr_final - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, hr_final)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            hr_cero += timedelta(days=1)
                            fecha_conteo = hr_cero
                else:
                    if hr_afternoon <= fecha_conteo < fecha_real_fin:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (fecha_real_fin - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin
                        else:
                            self.horas_nocturnas_ordinarias += (fecha_real_fin - fecha_conteo).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(fecha_conteo, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin

            else:
                if hr_morning < fecha_real_fin:
                    if hr_cero <= fecha_conteo < hr_morning:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (hr_morning - hr_cero).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_cero, hr_morning)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_morning
                        else:
                            self.horas_nocturnas_ordinarias += (hr_morning - hr_cero).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_cero, hr_morning)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_morning
                else:
                    if hr_cero <= fecha_conteo < fecha_real_fin:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (fecha_real_fin - hr_cero).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_cero, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin
                        else:
                            self.horas_nocturnas_ordinarias += (fecha_real_fin - hr_cero).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_cero, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin

                if hr_afternoon < fecha_real_fin:
                    if hr_morning <= fecha_conteo < hr_afternoon:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_diurnas_festivas += (hr_afternoon - hr_morning).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_morning, hr_afternoon)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_afternoon
                        else:
                            self.horas_diurnas_ordinarias += (hr_afternoon - hr_morning).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_morning, hr_afternoon)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = hr_afternoon
                else:
                    if hr_morning <= fecha_conteo < fecha_real_fin:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_diurnas_festivas += (fecha_real_fin - hr_morning).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_morning, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin
                        else:
                            self.horas_diurnas_ordinarias += (fecha_real_fin - hr_morning).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_morning, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_diurnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin

                if hr_final < fecha_real_fin:
                    if hr_afternoon <= fecha_conteo <= hr_final:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (hr_final - hr_afternoon).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_afternoon, hr_final)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_diurnas += self.compute_horas_extra(dupla, day)
                            hr_cero += timedelta(days=1)
                            fecha_conteo = hr_cero
                        else:
                            self.horas_nocturnas_ordinarias += (hr_final - hr_afternoon).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_afternoon, hr_final)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_diurnas += self.compute_horas_extra(dupla, day)
                            hr_cero += timedelta(days=1)
                            fecha_conteo = hr_cero
                else:
                    if hr_afternoon <= fecha_conteo <= fecha_real_fin:
                        if fecha_conteo.date() in domingos_festivos:
                            self.horas_nocturnas_festivas += (fecha_real_fin - hr_afternoon).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_afternoon, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_festivas_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin
                        else:
                            self.horas_nocturnas_ordinarias += (fecha_real_fin - hr_afternoon).seconds / 3600  # Number of hours
                            dupla = self.dupla_horas(hr_afternoon, fecha_real_fin)
                            day = fecha_conteo.strftime('%A')
                            self.horas_extras_ordinarias_nocturnas += self.compute_horas_extra(dupla, day)
                            fecha_conteo = fecha_real_fin

            hr_morning += timedelta(days=1)
            hr_afternoon += timedelta(days=1)
            hr_final += timedelta(days=1)
        
        self.horas_diurnas_ordinarias = round(self.horas_diurnas_ordinarias)
        self.horas_nocturnas_ordinarias = round(self.horas_nocturnas_ordinarias)
        self.horas_diurnas_festivas = round(self.horas_diurnas_festivas)
        self.horas_nocturnas_festivas = round(self.horas_nocturnas_festivas)
        
        self.horas_extras_ordinarias_diurnas = round(self.horas_extras_ordinarias_diurnas)
        self.horas_extras_ordinarias_nocturnas = round(self.horas_extras_ordinarias_nocturnas)
        self.horas_extras_festivas_diurnas = round(self.horas_extras_festivas_diurnas)
        self.horas_extras_festivas_nocturnas = round(self.horas_extras_festivas_nocturnas)
        
    horas_diurnas_ordinarias = fields.Float(string='Horas Diurnas Ordinales', compute=_calculo_horas)
    horas_nocturnas_ordinarias = fields.Float(string='Horas Nocuturna Ordinales', compute=_calculo_horas)
    horas_nocturnas_festivas = fields.Float(string='Horas Nocuturna Festivas', compute=_calculo_horas)
    horas_diurnas_festivas = fields.Float(string='Horas Diurnas Festivas', compute=_calculo_horas)
    horas_extras_ordinarias_diurnas = fields.Float(string='Horas Extra Ordinarias Diurnas', compute=_calculo_horas)
    horas_extras_ordinarias_nocturnas = fields.Float(string='Horas Extra Ordinarias Nocturnas', compute=_calculo_horas)
    horas_extras_festivas_diurnas = fields.Float(string='Horas Extra Diurnas Festivas', compute=_calculo_horas)
    horas_extras_festivas_nocturnas = fields.Float(string='Horas Extra Nocturnas Festivas', compute=_calculo_horas)
    
    def dupla_horas(self, fecha_inicio, fecha_fin):
        dupla = [(fecha_inicio.hour + (fecha_inicio.minute/60.0) + (fecha_inicio.minute/(60.0*60.0))),(fecha_fin.hour + (fecha_fin.minute/60.0) + (fecha_fin.minute/(60.0*60.0)))]
        return dupla

    def compute_horas_extra(self, dupla, day):
        intersecto = []
        horas = 0
        rango = []
        
        horas_lunes_empleado = 0
        horas_martes_empleado = 0
        horas_miercoles_empleado = 0
        horas_jueves_empleado = 0
        horas_viernes_empleado = 0
        horas_sabado_empleado = 0
        horas_domingo_empleado = 0

        rangos_horas_lunes = []
        rangos_horas_martes = []
        rangos_horas_miercoles = []
        rangos_horas_jueves = []
        rangos_horas_viernes = []
        rangos_horas_sabado = []
        rangos_horas_domingo = []

        for horario in self.employee_id.resource_calendar_id.attendance_ids:
            horas_empleado = horario.hour_to - horario.hour_from
            rangos = [horario.hour_from,horario.hour_to]

            if horario.dayofweek == '0':
                horas_lunes_empleado += horas_empleado
                rangos_horas_lunes.append(rangos)
            if horario.dayofweek == '1':
                horas_martes_empleado += horas_empleado
                rangos_horas_martes.append(rangos)
            if horario.dayofweek == '2':
                horas_miercoles_empleado += horas_empleado
                rangos_horas_miercoles.append(rangos)
            if horario.dayofweek == '3':
                horas_jueves_empleado += horas_empleado
                rangos_horas_jueves.append(rangos)
            if horario.dayofweek == '4':
                horas_viernes_empleado += horas_empleado
                rangos_horas_viernes.append(rangos)
            if horario.dayofweek == '5':
                horas_sabado_empleado += horas_empleado
                rangos_horas_sabado.append(rangos)
            if horario.dayofweek == '6':
                horas_domingo_empleado += horas_empleado
                rangos_horas_domingo.append(rangos)

        if day == 'Monday':
            rango = rangos_horas_lunes
        if day == 'Tuesday':
            rango = rangos_horas_martes
        if day == 'Wednesday':
            rango = rangos_horas_miercoles
        if day == 'Thursday':
            rango = rangos_horas_jueves
        if day == 'Friday':
            rango = rangos_horas_viernes
        if day == 'Saturday':
            rango = rangos_horas_sabado
        if day == 'Sunday':
            rango = rangos_horas_domingo

        for i in rango:
            i1 = dupla[0]
            f1 = dupla[1]
            i2 = i[0]
            f2 = i[1]
            if ((f1>=i2 and f1<=f2) or (f2>=i1 and f2<=f1)):
                start=0
                end=0
                start = i1 if i1>i2 else i2
                end = f1 if f1<f2 else f2
                intersecto.append([start,end])
        
        horas_dupla = dupla[1] - dupla[0]
        horas_intersecto = 0
        for inter in intersecto:
            horas_intersecto += inter[1] - inter[0]
        
        if horas_dupla - horas_intersecto > 0:
            horas = horas_dupla - horas_intersecto

        return horas