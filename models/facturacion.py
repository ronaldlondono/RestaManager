from datetime import datetime
import json
class Producto:
    def __init__(self, nombre, tipo, precio, cantidad):
        self.nombre = nombre
        self.tipo = tipo
        self.precio = precio
        self.cantidad = cantidad

class Facturacion:
    def __init__(self, info_restaurante,propina = 0):
        self.info_restaurante = info_restaurante
        self.id_pedido = 0
        self.detalle_pedido = []
        self.propina = propina
        self.fecha = datetime.now()
        self.iva = 19 # IVA en Colombia es del 19%

    def obtener_pedidos(self, archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as file:
                pedidos = json.load(file)
                self.id_pedido = pedidos["id"]
                ##lista de compresion para crear una lista de objetos Producto a partir de los datos del pedido
                self.detalle_pedido = [Producto(**pedido) for pedido in pedidos["productos"]]
                #La sintaxis **pedido desempaqueta el diccionario, pasando los valores a los parámetros del constructor de Producto (nombre, tipo, precio, cantidad).
                return print(f"Los pedidos son {pedidos}")
        except FileNotFoundError:
            print(f"El archivo {archivo} no se encontró.")
            return []
        except json.JSONDecodeError:
            print(f"Error al decodificar el archivo {archivo}.")
            return []

    def generar_factura(self):
        try:
            factura_nombre = f"{self.id_pedido}_{self.fecha.strftime('%Y%m%d_%H%M%S')}_factura.txt"
            with open(factura_nombre, 'w', encoding='utf-8') as file:
                file.write("="* 40 + "\n")
                file.write(f"Factura del restaurante {self.info_restaurante}\n")
                file.write(f"Fecha: {self.fecha.strftime('%d/%m/%Y')}\n")
                file.write("="* 40 + "\n")
                file.write(f"{'Producto':<20} {'Tipo':<20} {'Precio':<10} {'Cantidad':<10} {'Total':<10}\n")
                file.write("="* 40 + "\n")
                total = 0
                for producto in self.detalle_pedido:
                    subtotal = producto.precio * producto.cantidad
                    total += subtotal
                    file.write(f"{producto.nombre:<20} {producto.tipo:<20} {producto.precio:<10} {producto.cantidad:<10} {subtotal:<10}\n")
                file.write("="* 40 + "\n")
                file.write(f"{'Sub Total':<50} {total:<10}\n")
                #Propina
                if self.propina > 0:
                    file.write(f"{'Propina':<50} {self.propina:<10}\n")
                    total += self.propina
                #IVA
                iva_calculado = (total * self.iva) / 100
                file.write(f"{'IVA ('+str(self.iva)+'%)':<50} {iva_calculado:<10}\n")
                total += iva_calculado
                #Total
                file.write("="* 40 + "\n")
                file.write(f"{'Total a pagar':<50} {total:<10}\n")
                file.write("="* 40 + "\n")
                print("Factura generada correctamente.")
        except Exception as e:
            print(f"Error al generar la factura: {e}")




    # def generar_factura_consola(self):
    #     print("="* 40)
    #     print(f"Factura del restaurante {self.info_restaurante}")
    #     print(f"Fecha: {self.fecha.strftime('%d/%m/%Y')}")
    #     print("="* 40)
    #     print(f"{'Producto':<20} {'Tipo':<20} {'Precio':<10} {'Cantidad':<10} {'Total':<10}")
    #     print("="* 40)
    #     total = 0
    #     for producto in self.detalle_pedido:
    #         subtotal = producto.precio * producto.cantidad
    #         total += subtotal
    #         print(f"{producto.nombre:<20} {producto.tipo:<20} {producto.precio:<10} {producto.cantidad:<10} {subtotal:<10}")
    #     print("="* 40)
    #     print(f"{'Sub Total':<50} {total:<10}")
    #     if self.propina > 0:
    #         print(f"{'Propina':<50} {self.propina:<10}")
    #         total += self.propina
    #     if self.iva > 0:
    #         print(f"{'IVA':<50} {self.iva:<10}")
    #         total += self.iva
    #     print("="* 40)
    #     print(f"{'Total a pagar':<50} {total:<10}")
    #     print("="* 40)

