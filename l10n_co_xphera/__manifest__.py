
{
    'name': 'Contabilidad (Xphera)',
    'version': '0.9',
    'category': 'Localization',
    'description': 'Preconfiguración Contabilidad (Xphera)',
    'author': 'Xphera Group S.A.S.',
    'website': 'http://xphera.co',
    'depends': [
        'base',
        'base_setup',
        'account',
        'contacts',
        'base_vat',
    ],
    'data': [
        'data/l10n_co_xphera_chart_data.xml',
        'data/account.account.template.csv',
        'data/account_chart_template_data.xml',
        'data/account.tax.group.csv',
        'data/account_tax_template.xml',
        'data/account_chart_template_configure_data.xml',
        'data/fiscal_templates_data.xml',
        'data/res.municipio.csv',
        'views/res_partner.xml',
    ],
}
