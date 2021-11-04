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

            sheet.write(0,0,'Fecha de Reporte',format3)
            sheet.write(0,1,datetime.today()-timedelta(hours=5),format5)
            sheet.write(1,0,formato.code,format1)
            sheet.write(1,1,formato.name,format2)

            header_row_1001 = ['Concepto','Tipo de documento','Número identificación','Primer apellido del informado','Segundo apellido del informado','Primer nombre del informado','Otros nombres del informado','Razón social informado','Dirección','Código Departamento','Código Municiío','País de Residencia o domicilio','Pago o abono en cuenta deducible','Pago o abono en cuenta NO deducible','IVA mayor valor del costo o gasto, deducible','IVA mayor valor del costo o gasto no deducible','Retención en la fuente practicada Renta','Retención en la fuente asumida Renta','Retención en la fuente practicada IVA Régimen común','Retención en la fuente practicada IVA no domiciliados']
            header_row_1003 = ['Concepto','Tipo de documento','Número identificación del informado','DV','Primer apellido del informado','Segundo apellido del informado','Primer nombre del informado','Otros nombres del informado','Razón social informado','Dirección','Código del Departamento','Código del Municipio','Valor acumulado del pago o abono sujeto a Retención en la fuente','Retención que le practicaron']
            header_row_1004 = ['Concepto','Tipo de documento del Tercero','Número de Identificación del Tercero','Primer apellido','Segundo apellido','Primer nombre','Otros nombres','Razón Social','Dirección','Código Departamento','Código Municipio','Código País','Correo Electrónico','Valor del Pago o Abono en Cuenta','Valor del Descuento Tributario']
            header_row_1005 = ['Tipo de Documento','Numero de identificación del informado','DV','Primer apellido del informado','Segundo apellido del informado','Primer nombre del informado','Otros nombres del informado','Razón social informado','Impuesto descontable','IVA resultante por devoluciones en ventas anuladas, rescindidas o resueltas']
            header_row_1006 = ['Tipo de Documento','Número identificación','DV','Primer apellido del informado','Segundo apellido del informado','Primer nombre del informado','Otros nombres del informado','Razón social informado','Impuesto generado','IVA recuperado en devoluciones en compras anuladas. rescindidas o resueltas','Impuesto al consumo']
            header_row_1007 = ['Concepto','Tipo de documento','Número identificación del informado','Primer apellido del informado','Segundo apellido del informado','Primer nombre del informado','Otros nombres del informado','Razón social informado','País de residencia o domicilio','Ingresos brutos recibidos','Devoluciones, rebajas y descuentos']
            header_row_1008 = ['Concepto','Tipo de documento','Número identificación','DV','Primer apellido deudor','Segundo apellido deudor','Primer nombre deudor','Otros nombres deudor','Razón social deudor','Dirección','Código Departamento','Código Municipio','País de residencia o domicilio','Saldo cuentas por cobrar al 31-12']
            header_row_1009 = ['Concepto','Tipo de documento','Número identificación','DV','Primer apellido','Segundo apellido','Primer nombre','Otros nombres','Razón social','Dirección','Código Departamento','Código Municipio','País de residencia o domicilio','Saldo cuentas por pagar al 31-12 ']
            header_row_1010 = ['Tipo de documento','Número identificación socio o accionista','DV','Primer apellido socio o accionista','Segundo apellido socio o accionista','Primer nombre del socio o accionista','Otros nombres socio o accionista','Razón social','Dirección','Código Departamento','Código Municipio','País de residencia o domicilio','Valor patrimonial acciones o aportes al 31-12','Porcentaje de participación','Porcentaje de participación (posición decimal)']
            header_row_1011 = ['Concepto','Saldos al -31-12']
            header_row_1012 = ['Concepto','Tipo de documento','Número de Identificación','DV','Primer apellido del informado','Segundo apellido del informado','Primer nombre del informado','Otros nombres del informado','Razón social informado','Pais de residencia o domicilio','Valor al 31-12']
            header_row_1656 = ['Concepto','Tipo de documento','Número identificación','Primer apellido del informado','Segundo apellido del informado','Primer nombre del informado','Otros nombres del informado','Razón social informado','Dirección','Código Departamento','Código Municipio','País de Residencia o domicilio','Pago o abono en cuenta','IVA mayor valor del costo o gasto','Retención en la fuente practicada RENTA','Retención en la fuente asumida RENTA','Retención en la fuente practicada IVA Régimen común','Retención en la fuente practicada IVA no domiciliados']
            header_row_1647 = ['Concepto','Tipo de documento de quien se recibe el ingreso','Número identificación de quien recibe el ingreso','DV','Primer apellido de quien se recibe el ingreso','Segundo apellido de quien se recibe el ingreso','Primer nombre de quien se recibe el ingreso','Otros nombres de quien se recibe el ingreso','Razón social de quien se recibe el ingreso','País de residencia o domicilio de quien se recibe el ingreso','Valor total de la operación','Valor ingreso reintegrado transferido distribuido al tercero','Valor retención reintegrada transferida distribuida al tercero','Tipo de documento del tercero para quien se recibió el ingreso','Identificación del tercero para quien se recibió el ingreso','Primer apellido del tercero para quien se recibió el ingreso','egundo apellido del tercero par quien se recibió el ingreso','Primer nombre del tercero para quien se recibió el ingreso','Otros nombres del tercero para quien se recibió el ingreso','Razón social del tercero para quien se recibió el ingreso','Dirección','Código Departamento','Código Municipio','País de residencia o domicilio']
            header_row_2275 = ['Concepto','Tipo de documento del tercero','Número identificación del tercero','Primer apellido del informado','Segundo apellido del informado','Primer nombre del informado','Otros nombres del informado','Razón social','Dirección','Código Departamento','Código Municipio','Código País','Correo electrónico','Valor total del ingreso','Valor del ingreso no constitutivo de renta ni ganancia ocasional solicitado']
            header_row_2276 = ['Entidad Informante','Tipo de documento del beneficiario','Número de Identificación del beneficiario','Primer Apellido del beneficiario','Segundo Apellido del beneficiario','Primer Nombre del beneficiario','Otros Nombres del beneficiario','Dirección del beneficiario','Departamento del beneficiario','Municipio del beneficiario','País del beneficiario','Pagos por Salarios','Pagos por emolumentos eclesiásticos','Pagos por honorarios','Pagos por servicios','Pagos por comisiones','Pagos por prestaciones sociales','Pagos por viáticos','Pagos por gastos de representación','Pagos por compensaciones trabajo asociado cooperativo','Otros pagos','Cesantías e intereses de cesantías efectivamente pagadas, consignadas o reconocidas en el periodo','Pensiones de Jubilación, vejez o invalidez','Total Ingresos brutos de rentas de trabajo y pensión','Aportes Obligatorios por Salud','Aportes obligatorios a fondos de pensiones y solidaridad pensional y Aportes voluntarios al - RAIS','Aportes voluntarios a fondos de pensiones voluntarias','Aportes a cuentas AFC','Aportes a cuentas AVC','Valor de las retenciones en la fuente por pagos de rentas de trabajo o pensiones','Pagos realizados con bonos electrónicos o de papel de servicio, cheques, tarjetas, vales, etc.','Apoyos económicos no reembolsables o condonados, entregados por el Estado o financiados con recursos públicos, para financiar programas educativos','Pagos por alimentación mayores a 41 UVT','Pagos por alimentación hasta a 41 UVT','Identificación del fideicomiso o contrato','Tipo documento participante en contrato de colaboración','Identificación participante en contrato colaboración']
                                                    
            fila = 2
            columna = 0
            if formato.code == 1001:
                for header in header_row_1001:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 1003:
                for header in header_row_1003:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 1004:
                for header in header_row_1004:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 1005:
                for header in header_row_1005:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 1006:
                for header in header_row_1006:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 1007:
                for header in header_row_1007:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 1008:
                for header in header_row_1008:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 1009:
                for header in header_row_1009:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 1010:
                for header in header_row_1010:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 1011:
                for header in header_row_1011:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 1012:
                for header in header_row_1012:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 1656:
                for header in header_row_1656:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 1647:
                for header in header_row_1647:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 2275:
                for header in header_row_2275:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
            if formato.code == 2276:
                for header in header_row_2276:
                    sheet.set_column(0,columna,15)
                    sheet.write(fila,columna,header,format4)
                    columna += 1
                    
