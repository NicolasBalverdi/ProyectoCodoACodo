from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'myapp'
}

# Conexión a la base de datos
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Crear una tabla de productos si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        precio FLOAT NOT NULL,
        imagen VARCHAR(255) NOT NULL
    )
''')
conn.commit()

# Ruta para mostrar la lista de productos
@app.route('/')
def mostrar_productos():
    cursor.execute('SELECT * FROM productos')
    productos = [dict(zip(cursor.column_names, row)) for row in cursor.fetchall()]
    return render_template('productos.html', productos=productos)

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')

@app.route('/dulces')
def dulces():
    return render_template('dulces.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/venta')
def venta():
    return render_template('venta.html')

# Ruta para agregar un nuevo producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        imagen = request.form['imagen']

        cursor.execute('INSERT INTO productos (nombre, precio, imagen) VALUES (%s, %s, %s)', (nombre, precio, imagen))
        conn.commit()

        return redirect(url_for('mostrar_productos'))

    return render_template('agregar_producto.html')

# Ruta para ver detalles de un producto
@app.route('/producto/<int:producto_id>')
def ver_producto(producto_id):
    print(producto_id) 
    cursor.execute('SELECT * FROM productos WHERE id = %s', (producto_id,))
    producto = cursor.fetchone()
    print(producto) 
    return render_template('ver_producto.html', producto=producto)

# Ruta para modificar un producto
@app.route('/modificar/<int:producto_id>', methods=['GET', 'POST'])
def modificar_producto(producto_id):
    cursor.execute('SELECT * FROM productos WHERE id = %s', (producto_id,))
    producto = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        imagen = request.form['imagen']

        cursor.execute('UPDATE productos SET nombre=%s, precio=%s, imagen=%s WHERE id=%s', (nombre, precio, imagen, producto_id))
        conn.commit()

        return redirect(url_for('mostrar_productos'))

    return render_template('modificar_producto.html', producto=producto)

# Ruta para eliminar un producto
@app.route('/eliminar/<int:producto_id>')
def eliminar_producto(producto_id):
    cursor.execute('DELETE FROM productos WHERE id = %s', (producto_id,))
    conn.commit()

    return redirect(url_for('mostrar_productos'))

if __name__ == '__main__':
    app.run(debug=True)
