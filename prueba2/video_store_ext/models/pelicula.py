from odoo import fields, models


class Pelicula(models.Model):
    _inherit = 'videostore.pelicula'

    titulo_original = fields.Char(string='Título original')
    anio_lanzamiento = fields.Char(required=True)