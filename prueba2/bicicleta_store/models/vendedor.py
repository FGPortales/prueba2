from odoo import fields, models


class Vendedor(models.Model):
    _name = 'bicicletastore.vendedor'
    _description = 'Tabla vendedor'

    name = fields.Char(string='Nombre')
    direccion = fields.Char(string='Dirección')
