from odoo import models, fields, api, exceptions

# Modelo para ventas de ferretería
class Venta(models.Model):
    _name = 'ferreteria.venta'
    _description = 'Ventas en Ferretería'

    # Campo del modelo
    name = fields.Char(
        string="Número de Venta", 
        required=True, 
        copy=False, 
        readonly=True, 
        default=lambda self: 'New'
    )
    
    # Relacion: varios productos en cada venta
    lineas_venta_ids = fields.One2many(
        'ferreteria.venta.linea', 
        'venta_id', 
        string="Líneas de Venta"
    )  
    
    # Campo calculado para el total de la venta
    precio_total = fields.Monetary(
        string="Total", 
        compute="_calcular_total",
        currency_field='currency_id', 
        store=True
    )
    
    # Campo de moneda, se asigna por defecto a la moneda de la compañía
    currency_id = fields.Many2one(
        'res.currency', 
        string="Moneda", 
        default=lambda self: self.env.company.currency_id
    )

    # Campo calculado para concatenar los productos de la venta
    productos_resumen = fields.Char(
        string="Productos",
        compute="_compute_productos_resumen",
        store=True
    )

    # Campo calculado para mostrar la cantidad total de artículos
    cantidad_total = fields.Integer(
        string="Cantidad Total",
        compute="_compute_cantidad_total",
        store=True
    )

    # Generación automática de código único y secuencial
    @api.model
    def create(self, vals):
        """Genera un número de venta único y secuencial."""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('ferreteria.venta') or 'New'
        return super(Venta, self).create(vals)

    # Cálculo automático del Total
    @api.depends('lineas_venta_ids.subtotal')
    def _calcular_total(self):
        """Suma todos los subtotales de las líneas para obtener el total de la venta."""
        for venta in self:
            venta.precio_total = sum(venta.lineas_venta_ids.mapped('subtotal'))

    # Define la línea de venta
    @api.depends('lineas_venta_ids.producto_id')
    def _compute_productos_resumen(self):
        """Concatena el nombre de todos los productos"""
        for venta in self:
            nombres = venta.lineas_venta_ids.mapped('producto_id.name')
            venta.productos_resumen = ', '.join(nombres) if nombres else ''

    # Indica la cantidad total de la venta
    @api.depends('lineas_venta_ids.cantidad')
    def _compute_cantidad_total(self):
        """Suma la cantidad de todas las líneas para obtener la cantidad total de artículos."""
        for venta in self:
            venta.cantidad_total = sum(venta.lineas_venta_ids.mapped('cantidad'))

# Clase para las líneas de venta.
class VentaLinea(models.Model):
    _name = 'ferreteria.venta.linea'
    _description = 'Línea de Venta'        
    
    # Relaciona la línea con la venta
    venta_id = fields.Many2one(
        'ferreteria.venta', 
        string="Venta", 
        required=True, 
        ondelete="cascade"
    )

    # Relaciona la línea con un producto
    producto_id = fields.Many2one(
        'ferreteria.producto', 
        string="Producto", 
        required=True
    )
    
    # Cantida de producto vendido en la línea
    cantidad = fields.Integer(
        string="Cantidad", 
        required=True, 
        default=1
    )

    # Campo calculado para mostrar el total de la línea
    subtotal = fields.Monetary(
        string="Subtotal", 
        compute="_calcular_subtotal",
        currency_field='currency_id', 
        store=True
    )

    # Campo de moneda, hereda la moneda del registro de venta principal
    currency_id = fields.Many2one(
        'res.currency', 
        string="Moneda", 
        related='venta_id.currency_id',
        store=True,
        readonly=True
    )

    # Cálculo del subtotal
    @api.depends('cantidad', 'producto_id.precio')
    def _calcular_subtotal(self):
        """Calcula el subtotal de cada línea"""
        for linea in self:
            linea.subtotal = linea.cantidad * (linea.producto_id.precio or 0.0)

    # Restricción en Cantidad
    @api.constrains('cantidad')
    def _verificar_cantidad(self):
        """Evita que la cantidad sea menor o igual a cero"""
        for linea in self:
            if linea.cantidad <= 0:           
                raise exceptions.ValidationError("La cantidad debe ser mayor a 0.")
    
    # Advertencias
    @api.onchange('producto_id')
    def _actualizar_stock(self):
        """Muestra una advertencia en el formulario con el stock disponible"""
        if self.producto_id:
            return {
                'warning': {
                    'title': "Stock Disponible",
                    'message': f"Actualmente hay {self.producto_id.stock} unidades disponibles."
                }
            }

