# -*- coding: utf-8 -*-
{
    'name': "teaching_staffs",
    'summary': "add and delete the teaching staff",
    'description': """
        you can add and delete the teaching staffs from this module
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Website',
    'license': 'LGPL-3',
    'version': '0.1',
    'depends': ['web', 'website'],
      
    'data': [
        'views/teaching_staff_form.xml',
        'views/teaching_staff_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,  
}
