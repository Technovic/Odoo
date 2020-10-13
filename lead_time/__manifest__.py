# -*- coding: utf-8 -*-

{
    'name': 'Lead Time',
    'version': '13.0.1.0',
    'author': 'Technovicinfotech',
    'company': 'Technovicinfotech',
    'website': 'https://technovicinfotech.com/',
    'category': 'Project',
    'summary': 'Lead Time Calculation',
    'description': """ Lead Time Calculation """,
    'depends': ['mrp', 'planning', 'project_forecast'],
    'data': [
            'security/ir.model.access.csv',
            'views/tailor_leadtime.xml',
            'views/free_employee.xml',
            'data/reference_code.xml',
    ],
    'installable': True,
    'auto_install': False,
}