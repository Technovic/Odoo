# -*- coding: utf-8 -*-
###################################################################################
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Sayooj A O(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Lesser General Public License(LGPLv3) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
###################################################################################
{
    'name': 'Delivery Gate Pass',
    'summary': """Generating Gate pass slip in delivery orders""",
    'version': '12.0.1.0.0',
    'description': """Generating Gate pass slip in delivery orders""",
    'author': 'Technovic Infotech Solutions',
    'company': 'Technovic Infotech Solutions',
    # 'website': 'http://www.cybrosys.com',
    'category': 'Inventory',
    'depends': ['base', 'stock'],
    'license': 'LGPL-3',
    'data': [
        'views/gate_pass_details_views.xml',
        'report/gate_pass_template.xml',
        'report/gate_pass_report.xml',
        'report/delivery_notes_report.xml',
        'report/delivery_notes_template.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}
