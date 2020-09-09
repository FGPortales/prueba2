from odoo import fields, models

TIPO_DOC_SELECTION = [
    ('dni', 'DNI'),
    ('ce', 'Carnet de Extrangería')
]

class Actor(models.Model):
    _name = 'videostore.actor'
    _description = 'Tabla de Actores.'

    name = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellidos')
    edad = fields.Integer(string='Edad')
    tipo_doc = fields.Selection(TIPO_DOC_SELECTION, string='Tipo doc.')
    num_doc = fields.Integer(string='Número doc.')
    direccion = fields.Char(string='Dirección')
    telefono = fields.Integer(string='Teléfono')
    line_ids = fields.One2many('videostore.pelicula.line', 'actor_id', string='Peliculas')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'El nombre no puede ser repetido.'),
    ]
