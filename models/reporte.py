import os

class Reporte:
    def __init__(self, directorio_facturas="/Users/user/Documents/Proyecto/RestaManager"):
        # Si no se pasa un directorio, usar la carpeta actual como base
        if directorio_facturas is None:
            self.directorio_facturas = os.path.join(os.getcwd(), "RestaManager")
        else:
            self.directorio_facturas = os.path.abspath(directorio_facturas)

        # Verificar si la carpeta existe
        if not os.path.exists(self.directorio_facturas):
            raise FileNotFoundError(f"La carpeta '{self.directorio_facturas}' no existe.")
        
        self.ganancias_totales = 0
        self.detalles_facturas = []


    def procesar_facturas(self):
        try:
            # Recorrer todos los archivos en el directorio de facturas
            for archivo in os.listdir(self.directorio_facturas):
                if archivo.endswith("_factura.txt"):  # Verifica que sea una factura
                    ruta_factura = os.path.join(self.directorio_facturas, archivo)
                    with open(ruta_factura, 'r', encoding='utf-8') as file:
                        for linea in file:
                            # Buscar la línea del "Total a pagar" en la factura
                            if "Total a pagar" in linea:
                                total = float(linea.split()[-1])  # Tomar el valor al final de la línea
                                print(f"Factura: {archivo}, Total: {total}")
                                self.detalles_facturas.append((archivo, total))
                                self.ganancias_totales += total
                                break  # Salir después de encontrar el total de esta factura
        except Exception as e:
            print(f"Error al procesar las facturas: {e}")

    def generar_reporte(self, archivo_salida="reporte_facturas.txt"):
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as file:
                file.write("=" * 50 + "\n")
                file.write(f"{'Nombre de Factura':<30} {'Total':<10}\n")
                file.write("=" * 50 + "\n")
                for factura, total in self.detalles_facturas:
                    file.write(f"{factura:<30} {total:<10.2f}\n")
                file.write("=" * 50 + "\n")
                file.write(f"{'Ganancias Totales':<30} {self.ganancias_totales:<10.2f}\n")
                file.write("=" * 50 + "\n")
            print("Reporte generado correctamente.")
        except Exception as e:
            print(f"Error al generar el reporte: {e}")