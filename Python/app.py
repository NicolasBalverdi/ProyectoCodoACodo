from flask import Flask, request, jsonify, render_template
from flask import redirect, url_for

from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
CORS(app)

class Catalogo:
    def __init__(self, host, user, password, database):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")

    def cerrar_conexion(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def ejecutar_consulta(self, query, data=None):
        try:
            self.cursor.execute(query, data)
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error en la consulta SQL: {err}")
            return False

    def agregar_producto(self, codigo, descripcion, cantidad, precio, proveedor):
        query = "INSERT INTO productos (codigo, descripcion, cantidad, precio, proveedor) VALUES (%s, %s, %s, %s, %s);"
        data = (codigo, descripcion, cantidad, precio, proveedor)
        
        if self.ejecutar_consulta(query, data):
            return True
        else:
            return False

    def consultar_producto(self, codigo):
        query = "SELECT * FROM productos WHERE codigo = %s;"
        data = (codigo,)
        
        self.cursor.execute(query, data)
        return self.cursor.fetchone()

    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nuevo_proveedor):
        query = "UPDATE productos SET descripcion = %s, cantidad = %s, precio = %s, proveedor = %s WHERE codigo = %s;"
        data = (nueva_descripcion, nueva_cantidad, nuevo_precio, nuevo_proveedor, codigo)
        
        return self.ejecutar_consulta(query, data)

    def listar_productos(self):
        query = "SELECT * FROM productos;"
        self.cursor.execute(query)
        productos = self.cursor.fetchall()
        return productos

    def eliminar_producto(self, codigo):
        query = "DELETE FROM productos WHERE codigo = %s;"
        data = (codigo,)
        
        return self.ejecutar_consulta(query, data)

catalogo = Catalogo(host='localhost', user='root', password='Rodrigo2023', database='miapp')

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
