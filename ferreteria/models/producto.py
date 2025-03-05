from odoo import models, fields, api, exceptions

# Modelo para productos de ferretería
class Producto(models.Model):
    _name = 'ferreteria.producto'
    _description = 'Productos de Ferretería'

    # Campos del modelo
    name = fields.Char(
        string="Nombre", 
        required=True
    )
    
    # Guarda un código único para el producto
    codigo = fields.Char(
        string="Código", 
        required=True, 
        copy=False, 
        readonly=True, 
        default=lambda self: 'New'
    )
    
    # Precio del producto en un formato monetario
    precio = fields.Monetary(
        string="Precio",
        currency_field='currency_id', 
        required=True
    )

    # Guarda la cantidad de unidades disponibles
    stock = fields.Integer(
        string="Stock", 
        required=True
    )
    
    # Almacena una descripción detallada del producto
    descripcion = fields.Text(
        string="Descripción"
    )

    # Campo de moneda
    currency_id = fields.Many2one(
        'res.currency', 
        string="Moneda", 
        default=lambda self: self.env.company.currency_id
    )

    # Relaciones:
    # Un producto puede estar en muchas ventas.
    ventas_ids = fields.One2many(
        'ferreteria.venta.linea', 
        'producto_id', 
        string="Ventas"
    )

    # Cada producto pertenece a una categoría.
    categoria_id = fields.Many2one(
        'ferreteria.categoria', 
        string="Categoría", 
        required=True, 
        ondelete="cascade"
    )

    # Restricción: Evitar valores negativos en precio y stock
    @api.constrains('stock', 'precio')
    def _verificar_stock_precio(self):
        for producto in self:
            if producto.stock < 0:
                raise exceptions.ValidationError(
                "Error: El stock del producto '{}' no puede ser negativo.".format(producto.name))
            if producto.precio < 0:
                raise exceptions.ValidationError(
                "Error: El precio del producto '{}' no puede ser negativo.".format(producto.name))

    # Generación automática del código único    
    @api.model
    def create(self, vals):
        if vals.get('codigo', 'New') == 'New':
            vals['codigo'] = self.env['ir.sequence'].next_by_code('ferreteria.producto') or 'New'
        return super(Producto, self).create(vals)

    # Imprimir el inventario desde la vista de productos
    @api.model
    def action_print_inventario(self):
        productos = self.search([])
        return self.env.ref('ferreteria.action_reporte_inventario').report_action(productos)
        
