from flask import Flask, request, jsonify, render_template
from flask import redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from productos import Catalogo
import os
import time

app = Flask(__name__)
CORS(app)



catalogo = Catalogo(host='localhost', user='root', password='', database='miapp')

@app.teardown_appcontext
def close_database(error):
    catalogo.cerrar_conexion()

# Manejo de imágenes eliminado

@app.route('/productos', methods=["GET"])
def listar_productos():
    productos = catalogo.listar_productos()
    return jsonify(productos)

@app.route('/productos/<int:codigo>', methods=["GET"])
def mostrar_producto(codigo):
    producto = catalogo.consultar_producto(codigo)
    if producto:
        return jsonify(producto)
    else:
        return "Producto no encontrado", 404

@app.route('/productos', methods=["POST"])
def agregar_producto():
    codigo = request.form.get('codigo')
    descripcion = request.form.get('descripcion')
    cantidad = request.form.get('cantidad')
    precio = request.form.get('precio')
    proveedor = request.form.get('proveedor')  
    
    if catalogo.agregar_producto(codigo, descripcion, cantidad, precio, proveedor):
        return jsonify({"mensaje": "Producto agregado"}), 201
    else:
        return jsonify({"mensaje": "Producto ya existe"}), 400

@app.route('/modificar_producto', methods=['POST'])
def modificar_producto():
    codigo = request.form.get('codigo_modificar')
    nueva_descripcion = request.form.get('nueva_descripcion')
    nueva_cantidad = request.form.get('nueva_cantidad')
    nuevo_precio = request.form.get('nuevo_precio')
    nuevo_proveedor = request.form.get('nuevo_proveedor')

    if catalogo.consultar_producto(codigo):
        if catalogo.modificar_producto(codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nuevo_proveedor):
            return jsonify({'mensaje': 'Producto modificado'}), 201
        else:
            return jsonify({'mensaje': 'Error al modificar el producto'}), 500
    else:
        return jsonify({'mensaje': 'Producto no encontrado'}), 404

@app.route('/borrar_producto', methods=['POST'])
def borrar_producto():
    codigo = request.form.get('codigo_eliminar')
    if codigo:
        producto_existente = catalogo.consultar_producto(codigo)

        if producto_existente:
            if catalogo.eliminar_producto(codigo):
                return jsonify({"mensaje": "Producto eliminado"}), 200
            else:
                return jsonify({"mensaje": "Error al eliminar el producto"}), 500
        else:
            return jsonify({"mensaje": "Producto no encontrado"}), 404
    else:
        return jsonify({"mensaje": "Código no proporcionado"}), 400

if __name__ == "__main__":
    app.run(debug=True)
