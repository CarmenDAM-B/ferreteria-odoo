from odoo import models, fields

class CategoriaProducto(models.Model):
    _name = 'ferreteria.categoria'
    _description = 'Categorías de Productos'

    # Campos del modelo
    name = fields.Char(
        string="Nombre", 
        required=True
    )

    # Relación: Una categoría tiene muchos productos
    producto_ids = fields.One2many(
        'ferreteria.producto', 
        'categoria_id', 
        string="Productos"
    )
