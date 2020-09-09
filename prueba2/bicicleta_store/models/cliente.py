from odoo import fields, models


class Cliente(models.Model):
    _name = 'bicicletastore.cliente'
    _description = 'Tabla Cliente'

    name = fields.Char(string='Nombre', required=True)
    direccion = fields.Char(string='Dirección')