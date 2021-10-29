from odoo import api, fields, models, _

class AccountAccount(models.Model):
    _name = 'account.exogenous'

    name = fields.Char()
    formato = fields.Many2many('account.exogenous.formats', string='Formato')
    date_from = fields.Date()
    date_to = fields.Date()

    def generar_exogena(self):
        if self.date_from and self.date_to:
            self.name = self.date_from.strftime('%Y%m%d') + '_' + self.date_to.strftime('%Y%m%d') + '_' 

        self.name += 'Exógenas'

        for formato in self.formato:
            self.name += '_' + str(formato.code)
        
        return self.env.ref('exogenous_information.exogenous_report_xlsx').report_action(self)

class AccountAccount(models.Model):
    _name = 'account.exogenous.formats'

    code = fields.Integer(string='Código Formato')
    name = fields.Char(string='Nombre Formato')

    def name_get(self):
        result = []
        for formato in self:
            result.append((formato.id, "%s - %s" % (str(formato.code), formato.name)))
        return result
    