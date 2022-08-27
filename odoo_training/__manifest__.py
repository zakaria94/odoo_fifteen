{
    'name': "Odoo Training",
    'version': '1.0',
    'depends': ['base', 'purchase'],
    'author': "Zakariya Mahmoud",
    'category': 'Category',
    'description': """
    Odoo module for training 
    """,
    # data files always loaded at installation
    'data': [
        'views/purchase.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
