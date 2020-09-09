{
    'name' : 'Tienda de Bicicletas',
    'version' : '0.0.1',
    'summary': 'Módulo para vender Bicicletas',
    'description': """Módulo para administrar la venta
     venta de Bicicletas""",
    'category': 'Sale',
    'website': 'https://www.vendobicicletas.com',
    'depends' : ['base'],
    'data': [
        # Archivo de reglas de acceso
        'security/ir.model.access.csv',
        # Vistas
        'views/bicicleta_store_menus.xml',
        'views/cliente_views.xml',
        'views/comprobante_pago_views.xml',
    ],
    'installable': True,
}
