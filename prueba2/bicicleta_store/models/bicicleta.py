from odoo import fields, models


class Bicicleta(models.Model):
    _name = 'bicicletastore.bicicleta'
    _description = 'Tabla bicicleta'

    name = fields.Char(string='Nombre')
    precio = fields.Float(string='Precio')
    marca = fields.Char(string='Marca')
    modelo = fields.Char(string='Modelo')
