from datetime import datetime
import uuid

class Producto:
    def __init__(self, nombre, tipo, precio, cantidad):
        self.nombre = nombre
        self.tipo = tipo
        self.precio = precio
        self.cantidad = cantidad

    def calcular_total(self):
        return self.cantidad * self.precio

class Facturacion:
    def __init__(self, info_restaurante,propina = 0):
        self.info_restaurante = info_restaurante
        self.id_pedido = str(uuid.uuid4().hex)
        self.detalle_pedido = []
        self.propina = propina
        self.fecha = datetime.now()
        self.iva = 19 # IVA en Colombia es del 19%

    def agregar_item(self, producto, cantidad, precio_unitario):
        self.detalle_pedido.append(Producto(producto, producto, precio_unitario, cantidad))

    def calcular_subtotal(self):
        return sum(item.cantidad * item.precio for item in self.detalle_pedido)

    def calcular_propina(self):
        return self.propina * self.calcular_subtotal()

    def calcular_iva(self):
        return self.calcular_subtotal() * self.iva / 100
    
    def total(self):
        return self.calcular_subtotal() + self.calcular_propina() + self.calcular_iva()
