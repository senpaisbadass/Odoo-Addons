# -*- coding: utf-8 -*-
{
    'name': "non_teaching_staffs",
    'summary': "Add and manage non-teaching staff records",
    'description': """
        This module allows you to add, update, and delete non-teaching staff records, 
        including their name, position, and profile photo.
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Website',
    'license': 'LGPL-3',
    'version': '0.1',
    'depends': ['web', 'website'],
    
    'data': [
        'views/non_teaching_staff_form.xml',
        'views/non_teaching_staff_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,  # Set to True if you want to make it an application module
}
