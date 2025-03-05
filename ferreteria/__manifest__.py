{
    'name': "Ferreteria",
    'summary': "Gestión de productos y ventas en una ferretería",
    'description': """Modulo para la gestión de productos y ventas de una ferretería.""",
    'author': "M Carmen Pereira Pereira",
    'website': "https://www.yourcompany.com",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/producto.xml',
        'views/categoria.xml',       
        'views/venta.xml',
        'views/menu.xml',
        'data/demo.xml',
        'report/reporte_inventario.xml',
        'report/reporte_inventario_template.xml',
    ],

    'installable': True,
    'application': True,
}

