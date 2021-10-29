
{
    'name': 'Información Exogena (Xphera)',
    'version': '0.1',
    'category': 'Localization',
    'description': 'Información Exogena (Xphera)',
    'author': 'Xphera Group S.A.S.',
    'website': 'http://xphera.co',
    'depends': ['base', 'account', 'account_reports',
    ],
    'data': [
        'views/account_menuitem.xml',
        'views/account_exogenous.xml',
        'views/res_partner.xml',
        'views/account_account.xml',
        'views/l10n_latam_identification_type.xml',
        'data/account.exogenous.formats.csv',
        'reports/exogenous_report.xml',
    ],
}