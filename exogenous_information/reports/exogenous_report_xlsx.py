import pandas as pd
from odoo import models, fields, api
from datetime import datetime, timedelta

class ExogenousReportXlsx(models.AbstractModel):
    _name = 'report.exogenous_information.reporte_exogena_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font_size':14, 'font_name':'Arial', 'valign':'vcenter', \
                                        'align':'center', 'bold':True})
        format2 = workbook.add_format({'font_size':14, 'font_name':'Arial', 'valign':'vcenter', \
                                        'align':'left', 'bold':True})
        format3 = workbook.add_format({'font_size':10, 'font_name':'Arial', 'valign':'vcenter', \
                                        'align':'left', 'text_wrap':True})
        format4 = workbook.add_format({'font_size':10, 'font_name':'Arial', 'text_wrap':True, 'border':True, \
                                        'valign':'vcenter', 'align':'center', 'bg_color':'#008080', \
                                        'font_color':'white', 'bold':True})
        format5 = workbook.add_format({'font_size':10, 'font_name':'Arial', 'align':'center',\
                                        'valign':'vcenter', 'num_format': 'dd/mm/yyyy hh:mm'}) 
        format6 = workbook.add_format({'font_size':14, 'font_name':'Arial', 'valign':'vcenter', \
                                        'align':'center', 'text_wrap':True})                         

        for formato in lines.formato:
            sheet = workbook.add_worksheet(str(formato.code))
            #Fila,Columna
            sheet.set_column(0,0,15)
            sheet.set_column(0,1,15)
            sheet.set_column(0,2,15)
            sheet.set_column(0,3,15)
            sheet.set_column(0,4,15)
            sheet.set_column(0,5,15)
            sheet.set_column(0,6,15)
            sheet.set_column(0,7,15)
            sheet.set_column(0,8,15)
            sheet.set_column(0,9,15)
            sheet.set_column(0,10,15)
            sheet.set_column(0,11,15)
            sheet.set_column(0,12,15)
            sheet.set_column(0,13,15)
            sheet.set_column(0,14,15)
            sheet.set_column(0,15,15)

            sheet.write(0,0,'Fecha de Reporte',format3)
            sheet.write(0,1,datetime.today()-timedelta(hours=5),format5)
            sheet.write(1,0,formato.code,format1)
            sheet.write(1,1,formato.name,format2)

            fila = 2
            if formato.code == 1001:
                sheet.write(fila,0,'Concepto',format4)
                sheet.write(fila,1,'Tipo de Documento',format4)
                sheet.write(fila,2,'Número Identificación',format4)
                sheet.write(fila,3,'Primer Apellido del Informado',format4)
                sheet.write(fila,4,'Segundo Apellido del Informado',format4)
                sheet.write(fila,5,'Primer Nombre del Informado',format4)
                sheet.write(fila,6,'Otros Nombres del Informado',format4)
                sheet.write(fila,7,'Razón social informado',format4)
                sheet.write(fila,8,'Dirección',format4)
                sheet.write(fila,9,'Código Departamento',format4)
                sheet.write(fila,10,'Código Municipio',format4)
                sheet.write(fila,11,'País de Residencia o Domicilio',format4)
            else:
                sheet.write(fila,0,'Concepto',format4)
                sheet.write(fila,1,'Tipo de Documento',format4)
                sheet.write(fila,2,'Número Identificación',format4)
                sheet.write(fila,3,'Primer Apellido del Informado',format4)
                sheet.write(fila,4,'Segundo Apellido del Informado',format4)
                sheet.write(fila,5,'Primer Nombre del Informado',format4)
                sheet.write(fila,6,'Otros Nombres del Informado',format4)
                sheet.write(fila,7,'Razón social informado',format4)
                sheet.write(fila,8,'Dirección',format4)
                sheet.write(fila,9,'Código Departamento',format4)
                sheet.write(fila,10,'Código Municipio',format4)
