from models.facturacion import Facturacion
from models.reporte import Reporte

facturacion = Facturacion("Restaurante XYZ", 10)
reporte = Reporte()
reporte.procesar_facturas()
reporte.generar_reporte()