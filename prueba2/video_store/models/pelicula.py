from odoo import api, fields, models


GENERO_SELECTION = [
    ('terror', 'Terror'),
    ('horror', 'Horror'),
    ('comendia', 'Comedia'),
    ('suspenso', 'Suspenso'),
    ('drama', 'Drama')
]

class Pelicula(models.Model):
    _name = 'videostore.pelicula'
    _description = 'Tabla de Películas.'

    name = fields.Char(string='Nombre', required=True)
    duracion = fields.Char(string='Duración')
    director = fields.Char(string='Nombre Director', required=True)
    anio_lanzamiento = fields.Char(string='Año lanzamiento')
    genero = fields.Selection(GENERO_SELECTION, string='Género')
    numero = fields.Integer(string='Número')
    resenia = fields.Text(string='Reseña')
    line_ids = fields.One2many('videostore.pelicula.line', 'pelicula_id', string='Actores')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'El nombre no puede ser repetido.'),
    ]

class PeliculaLine(models.Model):
    _name = 'videostore.pelicula.line'
    _description = 'Películas por Actor'
    # _rec_name = 'pelicula_id'

    def _default_sueldo(self):
        return 10000

    name = fields.Char(string='Name', compute='_compute_name')
    pelicula_id = fields.Many2one('videostore.pelicula', string='Película', required=True)
    actor_id = fields.Many2one('videostore.actor', string='Actor', required=True)
    sueldo = fields.Float(string='Sueldo', default=_default_sueldo)

    @api.depends('pelicula_id', 'actor_id')
    def _compute_name(self):
        if self.pelicula_id and self.actor_id and self.actor_id.apellido:
            # self.name = self.pelicula_id.name + ' ' + self.actor_id.name+ ' ' + self.actor_id.apellido
            self.name = '%s %s %s' % (self.pelicula_id.name, self.actor_id.name, self.actor_id.apellido)
            # self.name = '{} {} {}'.format(self.pelicula_id.name, self.actor_id.name, self.actor_id.apellido)
        else:
            self.name = '/'

    _sql_constraints = [
        ('unique_pelicula_id_actor_id', 'unique(pelicula_id,actor_id)',
         'La relación entre película y actor debe ser única.'),
    ]
