# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'sequence': -100,
    'category': 'Hospital',
    'summary': 'Hospital Management System',
    'description': """ Hospital Management System Description """,
    'depends': ['mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/ir_sequence_data.xml',
        'wizard/cancel_appointment.xml',
        'views/menu.xml',
        'views/patient_views.xml',
        'views/female_patient_view.xml',
        'views/appointment_views.xml',
        'views/patient_tag_views.xml',
        'views/odoo_playgroud_views.xml',
        'views/res_config_settings_views.xml',
        'views/operation_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3'
}
