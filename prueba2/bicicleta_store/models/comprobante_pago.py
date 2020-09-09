import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

TERMINO_PAGO_SELECTION = [
    ('contado', 'Al contado'),
    ('plazo_15', '15 días plazo'),
    ('plazo_30', '30 días plazo')
]

STATE_SELECTION = [
    ('budget', 'Presupuesto'),
    ('confirm', 'Confirmado'),
    ('paid', 'Pagado')
]
STATE_PAGO_SELECTION = [
    ('pending', 'Pendiente'),
    ('today', 'Hoy'),
    ('overdue', 'Vencido')
]


class ComprobantePagoCliente(models.Model):
    _name = 'bicicletastore.comprobantepago.cliente'
    _description = 'Comprobantes de pago de cliente'

    name = fields.Char(string='Serie-Correlativo')
    fecha_emision = fields.Date(
        string='Fecha de Emisión',
        default=fields.Date.context_today,
        readonly=True,
        states={'budget': [('required', True),
                           ('readonly', False)]}
    )
    fecha_vencimiento = fields.Date(
        string='Fecha de Vencimiento',
        states={'paid': [('readonly', True)],
                'confirm': [('required', True)]}
    )
    cliente_id = fields.Many2one(
        'bicicletastore.cliente',
        string='Cliente',
        required=True,
        readonly=True,
        states={'budget': [('readonly', False)],
                'paid': [('readonly', True)]}
    )
    vendedor_id = fields.Many2one(
        'bicicletastore.vendedor',
        string='Vendedor',
        states={'confirm': [('required', True)],
                'paid': [('readonly', True)]}
    )
    tipo = fields.Selection(
        [('factura', 'Factura'),
        ('boleta', 'Boleta')],
        string='Tipo comprobante',
        readonly=True,
        states={'budget': [('readonly', False),
                           ('required', True)]}
    )
    termino_pago = fields.Selection(
        TERMINO_PAGO_SELECTION,
        string='Plazo pago',
        states={'paid': [('readonly', True)],
                'confirm': [('required', True)]}
    )
    moneda = fields.Selection(
        [('pen', 'Soles'),
         ('usd', 'Dólares')],
        string='Moneda',
        states={'paid': [('readonly', True)],
        'confirm': [('required', True)]}
    )
    total = fields.Float(string='Total')
    saldo = fields.Float(string='Saldo')

    state = fields.Selection(
        STATE_SELECTION,
        default='budget',
        string='Estado'
    )
    state_pago = fields.Selection(
        STATE_PAGO_SELECTION,
        default='pending',
        compute='_compute_state_pago',
        string='Estado Pago',
        store=True,
        states={'paid': [('readonly', True)]}
    )

    line_ids = fields.One2many(
        'bicicletastore.comprobantepago.cliente.bicicleta',
        'comprobante_id',
        string='Bicicletas',
    )
    pago_ids = fields.One2many(
        'bicicletastore.comprobantepago.historico',
        'comprobante_id',
        string='Pagos'
    )

    # @api.depends('line_ids')
    # def _compute_total(self):
    #     suma_total = 0
    #     for line in self.line_ids:
    #         suma_total += line.total
    #     self.total = suma_total

    @api.onchange('line_ids')
    def _onchange_line_ids(self):
        suma_total = 0
        for line in self.line_ids:
            suma_total += line.total
        return {
            'value': {
                'total': suma_total,
                'saldo': suma_total
            }
        }

    @api.onchange('pago_ids')
    def _onchange_pago_ids(self):
        suma_pago_total = 0
        for pago in self.pago_ids:
            # if pago.state == 'confirm':
            suma_pago_total += pago.monto
        return {
            'value': {
                'saldo': self.total - suma_pago_total
            }
        }

    @api.depends('fecha_vencimiento')
    def _compute_state_pago(self):
        today = fields.Date.context_today(self)
        if self.fecha_vencimiento:
            if self.fecha_vencimiento > today:
                self.state_pago = 'pending'
            elif self.fecha_vencimiento == today:
                self.state_pago = 'today'
            elif self.fecha_vencimiento < today:
                self.state_pago = 'overdue'

    def action_set_confirm(self):
        self.state = 'confirm'

    def action_set_paid(self):
        self.state = 'paid'


class ComprobantePagoClienteProducto(models.Model):
    _name = 'bicicletastore.comprobantepago.cliente.bicicleta'
    _description = 'Venta de bicicletas'

    comprobante_id = fields.Many2one('bicicletastore.comprobantepago.cliente', string='Comprobante')
    bicicleta_id = fields.Many2one('bicicletastore.bicicleta', string='Bicicleta', required=True)
    detalle = fields.Text(string='Detalle')
    precio = fields.Float(string='Precio', required=True)
    qty = fields.Float(string='Cantidad', required=True)
    total = fields.Float(string='Total', required=True)

    @api.onchange('bicicleta_id')
    def _onchange_bicicleta_id(self):
        return {'value': {'precio': self.bicicleta_id.precio}}

    @api.onchange('precio', 'qty')
    def _onchange_precio_qty(self):
        return {'value': {'total': self.precio * self.qty}}


class ComprobantePagoHistorico(models.Model):
    _name = 'bicicletastore.comprobantepago.historico'
    _description = 'Comprobantes de pago de historico'

    comprobante_id = fields.Many2one(
        'bicicletastore.comprobantepago.cliente',
        string='Comprobante'
    )
    fecha_pago = fields.Date(
        default=fields.Date.context_today,
        string='Fecha'
    )
    monto = fields.Float(string='Monto')
    state = fields.Selection(
        [('pending', 'Pendiente'),('confirm', 'Confirmado')],
        default='pending',
        string='Estado'
    )
    user_id = fields.Many2one(
        'res.users',
        default=lambda self: self.env.user.id
    )

    @api.onchange('monto')
    def _onchange_monto(self):
        if self.monto > self.comprobante_id.saldo:
            return {
                'value': {'monto': 0.0},
                'warning': {
                    'title': 'Error',
                    'message': 'No puede pagar más que el Saldo.'
                }
            }