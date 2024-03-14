# -*- coding: utf-8 -*-
{
    'name': "Hangry",

    'summary': """
        Module Hangry""",

    'description': """
        Take Home Test hangry
    """,

    'author': "Febry Ramadhan",
    'website': "https://framad.github.io/framadhan/",

    'category': 'Uncategorized',
    'version': '0.1',

		# Depencicy
    'depends': ['base','web'],

		# Include ALL XML Code in Here be mindful of order
    'data': [
        'security/access_groups.xml',
        'security/record_rules.xml',
        'security/ir.model.access.csv',
        'views/menuitems.views.xml',
        'views/master_data.views.xml',
        'views/master_data/employee.action.views.xml',
        'views/master_data/jam_shift.action.views.xml',
        'views/work_schedule/work_schedule.action.views.xml',
        'views/attendance/attendance.action.views.xml',
        'views/rekap_kehadiran/rekap_kehadiran.views.xml'
    ],

    'assets': {
        'web.assets_backend': [
            'hangry/static/src/js/geolocation.js'
        ]
    },

    'installable': True,
    'application': True,
    'auto_install': False

}