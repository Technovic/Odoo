# -*- coding: utf-8 -*-

{
    'name': 'DarAlHay Sale',
    'version': '13.0.1.0',
    'author': 'Technovicinfotech',
    'company': 'Technovicinfotech',
    'website': 'https://technovicinfotech.com/',
    'category': 'account',
    'summary': 'Sales',
    'description': """ Sales """,
    'depends': ['sale', 'account'],
    'data': [
            # 'security/ir.model.access.csv',
            'views/sale_changes.xml',
    ],
    'installable': True,
    'auto_install': False,
}