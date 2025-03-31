from models.facturacion import Facturacion

facturacion = Facturacion("Restaurante XYZ", 10, 0)
facturacion.obtener_pedidos("pedidos.json")
facturacion.generar_factura()