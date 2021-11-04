from odoo import models, fields, api

class ExogenousReportXlsx(models.AbstractModel):
    _name = 'report.exogenous_information.reporte_exogena_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font_size':10, 'align':'vcenter','bold':True})
        format2 = workbook.add_format({'font_size':10, 'align':'vcenter',})
        format3 = workbook.add_format({'font_size':10, 'align':'left','num_format': 'dd/mm/yy hh:mm'})
        
        for formato in lines.formato:
            sheet = workbook.add_worksheet(str(formato.code))
            sheet.set_column(3,3,50)
            sheet.set_column(2,2,50)
            sheet.write(2,2,'Requisición',format1)
            sheet.write(3,2,lines.name,format1)
