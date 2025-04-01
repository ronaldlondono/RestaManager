from flask import Flask, render_template, request, redirect, url_for
from models.facturacion import Facturacion
from datetime import datetime

app = Flask(__name__)

facturas = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        # Datos del restaurante
        info_restaurante = {
            "nombre": request.form['nombre_restaurante'],
            "direccion": request.form['direccion_restaurante'],
            "telefono": request.form['telefono_restaurante']
        }
        
        # Crear factura
        factura = Facturacion(info_restaurante, propina=float(request.form['propina']))
        
        # Agregar items
        productos = request.form.getlist('producto[]')
        cantidades = request.form.getlist('cantidad[]')
        precios = request.form.getlist('precio[]')
        
        for i in range(len(productos)):
            factura.agregar_item(
                producto=productos[i],
                cantidad=int(cantidades[i]),
                precio_unitario=float(precios[i])
            )
        
        facturas.append(factura)
        return redirect(url_for('ver_factura', id_pedido=factura.id_pedido))
    
    return render_template('crear.html')

@app.route('/listar')
def listar():
    return render_template('listar.html', facturas=facturas)

@app.route('/ver_factura/<string:id_pedido>')
def ver_factura(id_pedido):
    factura = next((f for f in facturas if f.id_pedido == id_pedido), None)
    if not factura:
        return render_template('error.html',
            error_code="404",
            titulo="Factura no encontrada",
            mensaje="La factura que buscas no existe o ha sido movida"
        ), 404
    return render_template('factura.html', factura=factura)

@app.route('/ver_reporte')
def ver_reporte():
    if not facturas:
        return render_template('error.html',
            error_code="404",
            titulo="No hay facturas registradas",
            mensaje="No hay facturas registradas para mostrar"
        ), 404
    total_general = sum(f.total() for f in facturas)
    return render_template('reporte.html', facturas=facturas, total_general=total_general, now=datetime.now())

@app.template_filter('colombian_currency')
def colombian_currency(value):
    # Formatea con separadores de miles y redondea a entero
    return "{:,.0f}".format(value).replace(',', 'X').replace('.', ',').replace('X', '.')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html',
        error_code="404",
        titulo="Página no encontrada",
        mensaje="La página que buscas no existe o ha sido movida"
    ), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html',
        error_code="500",
        title="Error interno",
        mensaje="Ocurrió un error inesperado en el servidor"
    ), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html',
        error_code="403",
        titulo="Acceso denegado",
        mensaje="No tienes permiso para acceder a este recurso"
    ), 403

if __name__ == '__main__':
    app.run(debug=True)